"""
evaluate.py — Evaluation script for JointNERRE model
------------------------------------------------------
FIX: הוספת Negative Sampling להערכה ריאליסטית של RE.
     המודל נבחן גם על זוגות ישויות ללא קשר (NEGATIVE),
     בדיוק כמו שאומן.
"""

import argparse
import json
import os
import random
import warnings
from collections import defaultdict

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from transformers import DebertaV2Model, DebertaV2TokenizerFast
from seqeval.metrics import classification_report as seq_classification_report
from sklearn.metrics import classification_report as sk_classification_report, confusion_matrix
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import seaborn as sns
import numpy as np

warnings.filterwarnings("ignore", category=UserWarning, module="seqeval")

IGNORE_INDEX = -100

NER_LABEL2ID = {
    "O": 0,
    "B-PARAMETER": 1, "I-PARAMETER": 2,
    "B-VALUE":     3, "I-VALUE":     4,
    "B-MIN":       5, "I-MIN":       6,
    "B-MAX":       7, "I-MAX":       8,
    "B-TYP":       9, "I-TYP":       10,
    "B-UNIT":     11, "I-UNIT":      12,
    "B-CONDITION":13, "I-CONDITION": 14,
}
NER_ID2LABEL = {v: k for k, v in NER_LABEL2ID.items()}

REL_LABEL2ID = {
    "NEGATIVE":       0,
    "has_value":      1,
    "has_unit":       2,
    "has_min":        3,
    "has_max":        4,
    "has_typ":        5,
    "has_condition":  6,
}
REL_ID2LABEL = {v: k for k, v in REL_LABEL2ID.items()}

MAX_TOKENS    = 512
MAX_REL_PAIRS = 64


class JointNERRE(nn.Module):
    def __init__(self, model_name, num_ner_labels, num_rel_labels,
                 dropout=0.1, alpha=1.0, beta=0.5):
        super().__init__()
        self.alpha, self.beta = alpha, beta
        self.encoder     = DebertaV2Model.from_pretrained(model_name)
        hidden_size      = self.encoder.config.hidden_size
        self.ner_dropout = nn.Dropout(dropout)
        self.ner_head    = nn.Linear(hidden_size, num_ner_labels)
        self.re_dropout  = nn.Dropout(dropout)
        self.re_head     = nn.Linear(hidden_size * 2, num_rel_labels)

    @staticmethod
    def _mean_pool_span(hidden_states, spans):
        B, num_rels, _ = spans.shape
        H      = hidden_states.size(-1)
        pooled = torch.zeros(B, num_rels, H, device=hidden_states.device)
        for b in range(B):
            for r in range(num_rels):
                start = spans[b, r, 0].item()
                end   = spans[b, r, 1].item() + 1
                if end > start:
                    pooled[b, r] = hidden_states[b, start:end].mean(dim=0)
        return pooled

    def forward(self, input_ids, attention_mask, token_type_ids,
                ner_labels=None, head_spans=None, tail_spans=None,
                rel_labels=None, rel_mask=None):
        outputs         = self.encoder(input_ids=input_ids,
                                       attention_mask=attention_mask,
                                       token_type_ids=token_type_ids)
        sequence_output = outputs.last_hidden_state.float()
        ner_logits      = self.ner_head(self.ner_dropout(sequence_output))

        re_logits = None
        if head_spans is not None and tail_spans is not None and head_spans.size(1) > 0:
            head_repr = self._mean_pool_span(sequence_output, head_spans)
            tail_repr = self._mean_pool_span(sequence_output, tail_spans)
            re_logits = self.re_head(
                self.re_dropout(torch.cat([head_repr, tail_repr], dim=-1))
            )

        return {"ner_logits": ner_logits, "re_logits": re_logits}


def span_to_start_end(token_indices):
    return (min(token_indices), max(token_indices))


# ==============================================================================
# FIX: build_rel_tensors עם Negative Sampling
# ==============================================================================
def build_rel_tensors(relations, seq_len, ner_tags_subword,
                      max_pairs=MAX_REL_PAIRS, neg_ratio=1.0):
    """
    בונה tensors לקשרים כולל negative pairs.

    FIX: הוספת negative pairs — זוגות ישויות שאין ביניהן קשר.
    זה חיוני כדי שהמדדים ישקפו את ביצועי המודל בעולם האמיתי,
    שם רוב הזוגות אינם בעלי קשר.

    Args:
        relations:        רשימת קשרים חיוביים מה-ground truth
        seq_len:          אורך הרצף בפועל (לא כולל padding)
        ner_tags_subword: תגיות NER ברמת subword לזיהוי ישויות
        max_pairs:        מקסימום זוגות בסך הכל
        neg_ratio:        יחס negatives לפוזיטיביות (1.0 = שווה)
    """
    head_spans = torch.zeros(max_pairs, 2, dtype=torch.long)
    tail_spans = torch.zeros(max_pairs, 2, dtype=torch.long)
    rel_labels = torch.zeros(max_pairs, dtype=torch.long)
    rel_mask   = torch.zeros(max_pairs, dtype=torch.bool)

    positive_pairs = set()
    filled = 0

    # --- קשרים חיוביים ---
    for rel in relations:
        if filled >= max_pairs:
            break
        h_start, h_end = span_to_start_end(rel["head"])
        t_start, t_end = span_to_start_end(rel["tail"])
        if h_end < seq_len and t_end < seq_len:
            head_spans[filled] = torch.tensor([h_start, h_end])
            tail_spans[filled] = torch.tensor([t_start, t_end])
            rel_labels[filled] = REL_LABEL2ID.get(rel["type"], 0)
            rel_mask[filled]   = True
            positive_pairs.add((h_start, t_start))
            positive_pairs.add((t_start, h_start))
            filled += 1

    num_positives = filled

    # --- FIX: Negative pairs ---
    # מציאת כל ישויות ה-B- ברצף (ראשי entities)
    entity_starts = [
        i for i, tag_id in enumerate(ner_tags_subword[:seq_len])
        if tag_id != IGNORE_INDEX and NER_ID2LABEL.get(tag_id, "O").startswith("B-")
    ]

    num_negatives_target = max(1, int(num_positives * neg_ratio))
    candidate_pairs = [
        (i, j)
        for i in entity_starts
        for j in entity_starts
        if i != j and (i, j) not in positive_pairs
    ]
    random.shuffle(candidate_pairs)

    for h_start, t_start in candidate_pairs[:num_negatives_target]:
        if filled >= max_pairs:
            break
        head_spans[filled] = torch.tensor([h_start, h_start])
        tail_spans[filled] = torch.tensor([t_start, t_start])
        rel_labels[filled] = REL_LABEL2ID["NEGATIVE"]
        rel_mask[filled]   = True
        filled += 1

    return head_spans, tail_spans, rel_labels, rel_mask


class DatasheetDataset(Dataset):
    def __init__(self, data, tokenizer, max_len=MAX_TOKENS):
        self.samples   = data
        self.tokenizer = tokenizer
        self.max_len   = max_len

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        sample = self.samples[idx]
        tokens = sample["tokens"]
        tags   = sample["ner_tags"]

        encoding = self.tokenizer(
            tokens,
            is_split_into_words=True,
            max_length=self.max_len,
            truncation=True,
            padding="max_length",
            return_tensors="pt",
        )

        input_ids      = encoding["input_ids"].squeeze(0)
        attention_mask = encoding["attention_mask"].squeeze(0)
        token_type_ids = encoding.get("token_type_ids",
                         torch.zeros_like(input_ids)).squeeze(0)
        word_ids       = encoding.word_ids(batch_index=0)

        ner_labels = torch.full((self.max_len,), IGNORE_INDEX, dtype=torch.long)
        prev_word  = None
        for i, wid in enumerate(word_ids):
            if wid is None:
                continue
            if wid != prev_word:
                label_str     = tags[wid] if wid < len(tags) else "O"
                ner_labels[i] = NER_LABEL2ID.get(label_str, 0)
            prev_word = wid

        word_to_first_subword = {}
        prev_word = None
        for i, wid in enumerate(word_ids):
            if wid is not None and wid != prev_word:
                word_to_first_subword[wid] = i
            prev_word = wid

        remapped_relations = []
        for rel in sample.get("relations", []):
            head_sw = [word_to_first_subword[t] for t in rel["head"]
                       if t in word_to_first_subword]
            tail_sw = [word_to_first_subword[t] for t in rel["tail"]
                       if t in word_to_first_subword]
            if head_sw and tail_sw:
                remapped_relations.append({
                    "head": head_sw,
                    "tail": tail_sw,
                    "type": rel["type"],
                })

        seq_len = attention_mask.sum().item()

        # FIX: מעביר ner_labels לבניית negative pairs
        head_spans, tail_spans, rel_labels, rel_mask = build_rel_tensors(
            remapped_relations,
            seq_len,
            ner_tags_subword=ner_labels.tolist(),  # FIX: חדש
            neg_ratio=1.0,                          # FIX: 1:1 pos/neg
        )

        return {
            "input_ids":      input_ids,
            "attention_mask": attention_mask,
            "token_type_ids": token_type_ids,
            "ner_labels":     ner_labels,
            "head_spans":     head_spans,
            "tail_spans":     tail_spans,
            "rel_labels":     rel_labels,
            "rel_mask":       rel_mask,
        }


def decode_ner_predictions(all_preds, all_labels):
    pred_seqs, true_seqs = [], []
    for preds, labels in zip(all_preds, all_labels):
        pred_seq, true_seq = [], []
        for p, l in zip(preds, labels):
            if l == IGNORE_INDEX:
                continue
            pred_seq.append(NER_ID2LABEL.get(p, "O"))
            true_seq.append(NER_ID2LABEL.get(l, "O"))
        pred_seqs.append(pred_seq)
        true_seqs.append(true_seq)
    return pred_seqs, true_seqs


def plot_confusion_matrix(cm, labels, title, save_path):
    fig, ax = plt.subplots(figsize=(max(8, len(labels)), max(7, len(labels) - 1)))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=labels, yticklabels=labels, ax=ax)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("True")
    ax.set_title(title)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"  Saved: {save_path}")


@torch.no_grad()
def run_evaluation(model, loader, device):
    model.eval()

    all_ner_preds, all_ner_labels = [], []
    all_rel_preds, all_rel_labels = [], []

    for batch in loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        out   = model(
            input_ids      = batch["input_ids"],
            attention_mask = batch["attention_mask"],
            token_type_ids = batch["token_type_ids"],
            head_spans     = batch["head_spans"],
            tail_spans     = batch["tail_spans"],
        )

        ner_preds = out["ner_logits"].argmax(dim=-1).cpu().tolist()
        ner_labs  = batch["ner_labels"].cpu().tolist()
        all_ner_preds.extend(ner_preds)
        all_ner_labels.extend(ner_labs)

        if out["re_logits"] is not None:
            re_preds = out["re_logits"].argmax(dim=-1)
            rel_mask = batch["rel_mask"]
            rel_labs = batch["rel_labels"]
            all_rel_preds.extend(re_preds[rel_mask].cpu().tolist())
            all_rel_labels.extend(rel_labs[rel_mask].cpu().tolist())

    return all_ner_preds, all_ner_labels, all_rel_preds, all_rel_labels


def main(args):
    os.makedirs(args.output_dir, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\n{'='*60}")
    print(f"  Device : {device}")
    print(f"  Model  : {args.model_path}")
    print(f"  Data   : {args.val_path}")
    print(f"{'='*60}\n")

    with open(args.val_path, encoding="utf-8") as f:
        raw = json.load(f)
    print(f"Loaded {len(raw)} validation samples.")

    tokenizer = DebertaV2TokenizerFast.from_pretrained(args.model_name)
    dataset   = DatasheetDataset(raw, tokenizer)
    loader    = DataLoader(dataset, batch_size=args.batch_size, shuffle=False)

    model = JointNERRE(
        model_name     = args.model_name,
        num_ner_labels = len(NER_LABEL2ID),
        num_rel_labels = len(REL_LABEL2ID),
    ).to(device)

    state = torch.load(args.model_path, map_location=device)
    if isinstance(state, dict) and "model_state_dict" in state:
        state = state["model_state_dict"]
    model.load_state_dict(state, strict=False)
    print("Model loaded successfully.\n")

    ner_preds, ner_labels, rel_preds, rel_labels = run_evaluation(
        model, loader, device
    )

    pred_seqs, true_seqs = decode_ner_predictions(ner_preds, ner_labels)

    print("=" * 60)
    print("  NER — Entity-Level Report (seqeval)")
    print("=" * 60)
    ner_report = seq_classification_report(true_seqs, pred_seqs, digits=4)
    print(ner_report)

    ner_report_path = os.path.join(args.output_dir, "ner_report.txt")
    with open(ner_report_path, "w") as f:
        f.write(ner_report)
    print(f"  Saved: {ner_report_path}\n")

    flat_true = [l for sublist in ner_labels
                 for l in sublist if l != IGNORE_INDEX]
    flat_pred = [p for plist, llist in zip(ner_preds, ner_labels)
                 for p, l in zip(plist, llist) if l != IGNORE_INDEX]
    used_ids  = sorted(set(flat_true + flat_pred))
    used_lbls = [NER_ID2LABEL[i] for i in used_ids]
    cm_ner    = confusion_matrix(flat_true, flat_pred, labels=used_ids)
    plot_confusion_matrix(
        cm_ner, used_lbls,
        "NER Confusion Matrix (token-level)",
        os.path.join(args.output_dir, "ner_confusion_matrix.png"),
    )

    if rel_preds:
        print("=" * 60)
        print("  Relation Extraction Report (with Negatives)")
        print("=" * 60)

        # הוספת הערה על negative sampling
        neg_count = rel_labels.count(REL_LABEL2ID["NEGATIVE"])
        pos_count = len(rel_labels) - neg_count
        print(f"  Positive pairs: {pos_count}  |  Negative pairs: {neg_count}\n")

        rel_label_names = [REL_ID2LABEL[i]
                           for i in sorted(set(rel_labels + rel_preds))]
        re_report = sk_classification_report(
            rel_labels, rel_preds,
            target_names=rel_label_names,
            digits=4,
            zero_division=0,
        )
        print(re_report)

        re_report_path = os.path.join(args.output_dir, "re_report.txt")
        with open(re_report_path, "w") as f:
            f.write(f"Positive pairs: {pos_count}  |  Negative pairs: {neg_count}\n\n")
            f.write(re_report)
        print(f"  Saved: {re_report_path}\n")

        used_rel_ids  = sorted(set(rel_labels + rel_preds))
        used_rel_lbls = [REL_ID2LABEL[i] for i in used_rel_ids]
        cm_re         = confusion_matrix(rel_labels, rel_preds,
                                         labels=used_rel_ids)
        plot_confusion_matrix(
            cm_re, used_rel_lbls,
            "RE Confusion Matrix (with Negatives)",
            os.path.join(args.output_dir, "re_confusion_matrix.png"),
        )
    else:
        print("No relation predictions found — skipping RE report.\n")

    print("=" * 60)
    print("  Qualitative Examples (first 3 samples)")
    print("=" * 60)
    qual_path = os.path.join(args.output_dir, "qualitative_examples.txt")
    with open(qual_path, "w", encoding="utf-8") as f:
        for sample, pred_seq, true_seq in zip(raw[:3], pred_seqs[:3], true_seqs[:3]):
            f.write(f"\n{'─'*50}\n")
            f.write(f"ID: {sample['id']}\n")
            f.write(f"{'TOKEN':<25} {'PREDICTED':<18} {'GROUND TRUTH'}\n")
            f.write(f"{'─'*60}\n")
            tokens = [t for t in sample["tokens"] if t.strip()]
            for tok, pred, true in zip(tokens, pred_seq, true_seq):
                marker = "  ✗" if pred != true else ""
                f.write(f"{tok:<25} {pred:<18} {true}{marker}\n")
    print(f"  Saved: {qual_path}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", required=True,
                        help="Path to best_model.pt")
    parser.add_argument("--val_path",   required=True,
                        help="Path to validation JSON file")
    parser.add_argument("--model_name", default="microsoft/deberta-v3-base",
                        help="HuggingFace model name (must match training)")
    parser.add_argument("--output_dir", default="./eval_results",
                        help="Directory to save reports and plots")
    parser.add_argument("--batch_size", type=int, default=8)
    args = parser.parse_args()
    main(args)
