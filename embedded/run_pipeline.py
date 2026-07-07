"""Run the full PDF inference pipeline and print a quality report."""
import sys, json, shutil
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r'C:\Users\nivsa\Generation of Synthetic Training Data\embedded\extraction_engine')

from pathlib import Path
from pdf_inference_pipeline import PDFInferencePipeline

BASE        = Path(r'C:\Users\nivsa\Generation of Synthetic Training Data\embedded')
INPUT_DIR   = BASE / 'example_datasheets'
OUTPUT_DIR  = BASE / 'output_results'
ALIGNER_DIR = BASE / 'extraction_engine'
MODEL_PATH  = BASE / 'models' / 'checkpoints'

# Clean old results
if OUTPUT_DIR.exists():
    shutil.rmtree(str(OUTPUT_DIR))
OUTPUT_DIR.mkdir()

pipeline = PDFInferencePipeline(
    input_dir   = INPUT_DIR,
    output_dir  = OUTPUT_DIR,
    aligner_dir = ALIGNER_DIR,
    model_path  = MODEL_PATH,
    ner_mode    = 'auto',
)
pipeline.run()

# Quality report
print("\n" + "="*60)
print("QUALITY REPORT")
print("="*60)
for pdf_dir in sorted(OUTPUT_DIR.iterdir()):
    if not pdf_dir.is_dir():
        continue
    json_file = pdf_dir / f"{pdf_dir.name}.json"
    if not json_file.exists():
        continue
    d = json.load(open(json_file, encoding='utf-8'))
    params = d.get('parameters', [])
    named  = [p for p in params if (p.get('parameter') or '').strip()]
    vals   = [p for p in named if any(p.get(k) for k in ('min','typ','max'))]
    fstat  = d.get('filter_stats', {})
    print(f"\n{pdf_dir.name}")
    print(f"  Pages: {fstat.get('kept_pages','?')}/{fstat.get('total_pages','?')}")
    print(f"  Params total: {len(params)}  | with name: {len(named)}  | with values: {len(vals)}")
    print(f"  First 8 params:")
    for p in named[:8]:
        name = (p['parameter'] or '')[:40]
        mn   = str(p['min'] or '—')[:7]
        typ  = str(p['typ'] or '—')[:7]
        mx   = str(p['max'] or '—')[:7]
        unit = str(p['unit'] or '')[:6]
        print(f"    {name:40s}  min={mn:7}  typ={typ:7}  max={mx:7}  {unit}")
