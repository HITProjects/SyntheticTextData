"""Run extraction pipeline on the 8 benchmark PDFs (one per component type)."""
import sys, json, shutil
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

_HERE = Path(__file__).parent
sys.path.insert(0, str(_HERE / 'extraction_engine'))

from pdf_inference_pipeline import PDFInferencePipeline

BASE        = _HERE
SRC_DIR     = BASE / 'example_datasheets'
OUTPUT_DIR  = BASE / 'output_results_benchmark'
MODEL_PATH  = BASE / 'models' / 'checkpoints'
ALIGNER_DIR = BASE / 'extraction_engine'

BENCHMARK_FILES = {
    "RESISTOR":          "GP-1671375.pdf",
    "CAPACITOR":         "e-hd.pdf",
    "INDUCTOR":          "ds_inductors.pdf",
    "MOSFET":            "infineon-irf3205-datasheet-en.pdf",
    "DIODE":             "1662528.pdf",
    "BJT":               "2SC5994-D.PDF",
    "OPAMP":             "lm741.pdf",
    "VOLTAGE_REGULATOR": "tps7a02.pdf",
}

# Build a temp input dir with only the 8 files
TEMP_INPUT = BASE / '_benchmark_input'
if TEMP_INPUT.exists():
    shutil.rmtree(str(TEMP_INPUT))
TEMP_INPUT.mkdir()

for comp_type, fname in BENCHMARK_FILES.items():
    src = SRC_DIR / fname
    if src.exists():
        shutil.copy(str(src), str(TEMP_INPUT / fname))
        print(f"  Copied [{comp_type:20s}] {fname}")
    else:
        print(f"  MISSING: {fname}")

if OUTPUT_DIR.exists():
    shutil.rmtree(str(OUTPUT_DIR))
OUTPUT_DIR.mkdir()

print(f"\nRunning pipeline on {len(BENCHMARK_FILES)} files...\n")

pipeline = PDFInferencePipeline(
    input_dir   = TEMP_INPUT,
    output_dir  = OUTPUT_DIR,
    aligner_dir = ALIGNER_DIR,
    model_path  = MODEL_PATH,
    ner_mode    = 'auto',
)
pipeline.run()

# Cleanup temp dir
shutil.rmtree(str(TEMP_INPUT))

# Quality report
COMP_MAP = {v.lower().replace('.pdf','').replace('.PDF',''): k for k, v in BENCHMARK_FILES.items()}

print("\n" + "="*70)
print("BENCHMARK QUALITY REPORT")
print("="*70)
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

    comp_type = COMP_MAP.get(pdf_dir.name.lower(), '?')
    print(f"\n[{comp_type}] {pdf_dir.name}")
    print(f"  Pages: {fstat.get('kept_pages','?')}/{fstat.get('total_pages','?')}")
    print(f"  Params: {len(params)} total | {len(named)} named | {len(vals)} with values")
    print(f"  Sample parameters:")
    for p in named[:6]:
        name = (p.get('parameter') or '')[:38]
        mn   = str(p.get('min') or '—')[:8]
        typ  = str(p.get('typ') or '—')[:8]
        mx   = str(p.get('max') or '—')[:8]
        unit = str(p.get('unit') or '')[:6]
        cond = str(p.get('condition') or '')[:25]
        print(f"    {name:38s}  {mn:8} {typ:8} {mx:8} {unit:6}  {cond}")
