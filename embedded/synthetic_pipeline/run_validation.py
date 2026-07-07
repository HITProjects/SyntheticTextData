"""
Run strategies_validator on all component types.
Does NOT need Ollama — only the engineering generation layer.
Usage: python -m synthetic_pipeline.run_validation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from synthetic_pipeline.logic import DatasheetGenerator
from synthetic_pipeline.strategies import UNIFIED_COMPONENT_DB

from synthetic_pipeline.resistor_strategy import ResistorStrategy
from synthetic_pipeline.capacitor_strategy import CapacitorStrategy
from synthetic_pipeline.diode_strategy import DiodeStrategy
from synthetic_pipeline.mosfet_strategy import MosfetStrategy
from synthetic_pipeline.voltage_Regulator_strategy import VoltageRegulatorStrategy
from synthetic_pipeline.inductor_strategy import InductorStrategy
from synthetic_pipeline.bjt_strategy import BJTStrategy
from synthetic_pipeline.opamp_strategy import OpampStrategy

from synthetic_pipeline.strategies_validator import run_validation, validate_param

STRATEGIES = {
    "RESISTOR": ResistorStrategy(),
    "CAPACITOR": CapacitorStrategy(),
    "DIODE": DiodeStrategy(),
    "MOSFET": MosfetStrategy(),
    "VOLTAGE_REGULATOR": VoltageRegulatorStrategy(),
    "INDUCTOR": InductorStrategy(),
    "BJT": BJTStrategy(),
    "OPAMP": OpampStrategy(),
}

SAMPLES_PER_TYPE = 3  # Generate N samples per component for coverage


def main():
    generator = DatasheetGenerator(UNIFIED_COMPONENT_DB)
    all_results = []

    print("Generating samples for all component types...\n")
    for comp_type, strategy in STRATEGIES.items():
        ok_count = 0
        fail_count = 0
        for i in range(SAMPLES_PER_TYPE):
            try:
                result = generator.generate(comp_type, strategy)
                all_results.append(result)
                ok_count += 1
            except Exception as e:
                fail_count += 1
                print(f"  [GENERATE ERROR] {comp_type} sample {i+1}: {e}")
        status = "OK" if fail_count == 0 else f"{fail_count} failed"
        print(f"  {comp_type:20s}  {ok_count} samples  [{status}]")

    print(f"\nTotal results: {len(all_results)}\n")
    print("=" * 50)

    # Per-component breakdown before full validation
    print("\nPer-component error preview:\n")
    comp_errors: dict = {}
    for result in all_results:
        comp = result.context.component_type
        for param in result.parameters:
            errs = validate_param(param)
            if errs:
                if comp not in comp_errors:
                    comp_errors[comp] = []
                comp_errors[comp].append((param.key, errs))

    if comp_errors:
        for comp, problems in comp_errors.items():
            print(f"\n  [{comp}]  {len(problems)} param(s) with errors:")
            for key, errs in problems[:10]:   # cap at 10 per component
                print(f"    {key}:")
                for e in errs:
                    print(f"      [ERR] {e}")
            if len(problems) > 10:
                print(f"    ... and {len(problems)-10} more")
    else:
        print("  (none)")

    print()
    ok = run_validation(all_results)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
