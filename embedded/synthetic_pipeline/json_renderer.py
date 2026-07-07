import json
import copy
import html
import re
import random

from typing import Dict, Any, List, Optional
from dataclasses import asdict

from synthetic_pipeline.base_renderer import BaseDatasheetRenderer, RenderingConfig


class DatasheetJSONRenderer(BaseDatasheetRenderer):

    def _generate_relation_triples(self, ground_truth: Dict, metadata: Dict = None) -> List[Dict]:
        """
        ✅ Converts entity-centric ground truth into relation-centric triples for OpenIE evaluation.

        Args:
            ground_truth: Dict of {param_key: {attributes}} from entity-centric GT
            metadata: Optional metadata about the component (manufacturer, package, etc.)

        Returns:
            List of semantic triples in the format:
            [
                {"subject": "param_name", "predicate": "has_min_value", "object": "value"},
                ...
            ]

        Design Decisions:
        - Only generates triples for non-null values
        - Normalizes predicates to canonical relations
        - Includes metadata triples (component-level facts)
        - Preserves data types in objects (strings, numbers, booleans)
        """
        triples = []

        # === Predicate Mapping ===
        # Maps ground truth keys to semantic predicates
        PREDICATE_MAP = {
            "min": "has_min_value",
            "typ": "has_typical_value",
            "max": "has_max_value",
            "unit": "has_unit",
            "condition": "has_condition",
            "spec_type": "has_spec_type",
            "engineering_class": "has_engineering_class",
            "display_mode": "has_display_mode",
            "column_model": "has_column_model"
        }

        # === Component-Level Metadata Triples ===
        # These describe the component itself, not individual parameters
        if metadata:
            component_subject = metadata.get("component_type", "component")

            if metadata.get("package"):
                triples.append({
                    "subject": component_subject,
                    "predicate": "has_package",
                    "object": metadata["package"],
                    "object_type": "string"
                })

            if metadata.get("archetype"):
                triples.append({
                    "subject": component_subject,
                    "predicate": "has_archetype",
                    "object": metadata["archetype"],
                    "object_type": "string"
                })

            if metadata.get("process_corner"):
                triples.append({
                    "subject": component_subject,
                    "predicate": "has_process_corner",
                    "object": metadata["process_corner"],
                    "object_type": "string"
                })

        # === Parameter-Level Triples ===
        # Iterate through each parameter's attributes.
        # Subject is the human-readable parameter_name so the aligner can
        # match it against the actual tokens in the HTML text.
        for param_key, param_data in ground_truth.items():
            param_name = param_data.get("parameter_name") or param_key

            # Attributes that should NOT produce triples:
            # - raw_* debug fields
            # - internal keys (column_model, display_mode, spec_type,
            #   engineering_class) — these are meta-labels, not extractable facts
            # - parameter_name itself (it is the subject, not an object)
            SKIP_ATTRS = {
                "parameter_name", "column_model", "display_mode",
                "spec_type", "engineering_class",
            }

            # FIX Bug 4: structural column-header words are not real test conditions
            _STRUCTURAL_CONDITIONS = {
                "Max", "Min", "Typ", "Maximum", "Minimum", "Typical",
                "Nom", "Nominal", "Value", "Rating", "Limit",
            }

            for attr_key, attr_value in param_data.items():
                # Skip debug / internal fields
                if attr_key.startswith("raw_") or attr_key.startswith("_"):
                    continue
                if attr_key in SKIP_ATTRS:
                    continue

                # Skip null / empty values (no triple for missing data)
                if attr_value is None or attr_value == "":
                    continue

                # FIX: skip non-display attributes that aren't actual facts
                if attr_key not in PREDICATE_MAP:
                    continue

                # FIX Bug 4: skip structural pseudo-conditions (column-header leakage)
                if attr_key == "condition" and str(attr_value) in _STRUCTURAL_CONDITIONS:
                    continue

                predicate = PREDICATE_MAP[attr_key]

                # FIX Bug 2: for numeric predicates (min/typ/max), use the raw numeric
                # string instead of the full display value which may contain the unit suffix
                # (e.g. "493nH").  Using the display value causes the aligner to build a
                # multi-token tail that includes unit tokens, corrupting has_max relations.
                if attr_key in ("min", "typ", "max"):
                    raw_key   = f"_raw_{attr_key}"
                    raw_num   = param_data.get(raw_key)
                    object_val = str(raw_num) if raw_num is not None else str(attr_value)
                else:
                    object_val = str(attr_value)

                object_type = self._infer_object_type(object_val)

                # FIX: never emit a triple where subject == object.
                if param_name == object_val:
                    continue

                triple = {
                    "subject":     param_name,
                    "predicate":   predicate,
                    "object":      object_val,
                    "object_type": object_type,
                }

                # Attach unit context to numeric value triples
                if attr_key in ("min", "typ", "max") and param_data.get("unit"):
                    triple["unit"] = param_data["unit"]

                if attr_key == "condition" and len(object_val) > 50:
                    triple["is_long_condition"] = True

                triples.append(triple)

        return triples

    def _infer_object_type(self, value: Any) -> str:
        """
        ✅ Infers the semantic type of a triple's object.

        This helps OpenIE models understand what kind of entity they're extracting.

        Args:
            value: The object value from the triple

        Returns:
            Type string: "numeric", "string", "boolean", "categorical"
        """
        if isinstance(value, bool):
            return "boolean"

        if isinstance(value, (int, float)):
            return "numeric"

        if isinstance(value, str):
            # Try to detect if it's a numeric string
            try:
                float(value)
                return "numeric"
            except (ValueError, TypeError):
                pass

            # Check for categorical values (known enums)
            categorical_patterns = [
                "max_rating", "min_rating", "typ_rating",
                "electrical", "thermal", "mechanical",
                "table", "text_description"
            ]

            if any(pattern in value.lower() for pattern in categorical_patterns):
                return "categorical"

            # Default to string
            return "string"

        return "unknown"


    def render(self, result: 'DatasheetResult', marketing_data: Dict = None,
               config: RenderingConfig = None, injected_param_keys: List[str] = None) -> Dict[str, Any]:
        """
        ✅ ENHANCED: Now generates both entity-centric AND relation-centric ground truth

        Args:
            result: DatasheetResult (with injected params already removed)
            marketing_data: Marketing content
            config: The SAME RenderingConfig used by HTML renderer
            injected_param_keys: Keys of parameters shown as text

        Returns:
            JSON with:
            - ground_truth: Entity-centric (original format)
            - relation_ground_truth: Relation-centric (new format for OpenIE)
        """
        ground_truth = {}
        display_tables = {}
        seen_labels = set()

        injected_keys = injected_param_keys or []
        hidden_columns = config.hidden_columns if config else []

        for param in result.parameters:
            # Format the row (same as HTML)
            formatted_row = self._format_row(param)

            # Extract values
            visual_min = formatted_row.get("Min")
            visual_typ = formatted_row.get("Typ")
            visual_max = formatted_row.get("Max")
            visual_unit = formatted_row.get("Unit")

            # ✅ CRITICAL FIX: Respect hidden columns from config
            if 'Min' in hidden_columns:
                visual_min = None
            if 'Typ' in hidden_columns:
                visual_typ = None
            if 'Max' in hidden_columns:
                visual_max = None

            # Determine display mode
            display_mode = "text_description" if param.key in injected_keys else "table"

            # Build ground truth entry
            gt_metadata = formatted_row.get("_metadata", {})
            ground_truth[param.key] = {
                "spec_type": self._get_enum_val(param.spec_type).lower(),
                "engineering_class": self._get_enum_val(param.engineering_class),
                "column_model": self._determine_column_model(param),
                "condition": param.condition,
                "display_mode": display_mode,
                "parameter_name": formatted_row["Parameter"],
                # ✅ SYNCHRONIZED VALUES: null if column was hidden
                "unit": visual_unit,
                "min": visual_min,
                "typ": visual_typ,
                "max": visual_max,
                # FIX Bug 2: raw numeric strings (no unit suffix) for relation triple objects.
                # Using the full display string (e.g. "493nH") as the triple object causes the
                # aligner to match a multi-token phrase that includes unit tokens, polluting
                # has_max tails with unit text.  These _raw_* fields contain only the number.
                "_raw_min": gt_metadata.get("raw_min"),
                "_raw_typ": gt_metadata.get("raw_typ"),
                "_raw_max": gt_metadata.get("raw_max"),
                # Debug info
                "raw_value_typ": param.value_typ,
                "raw_unit": param.unit
            }

            # Build display tables
            if param.section not in display_tables:
                display_tables[param.section] = []

            label_key = (param.section, formatted_row["Parameter"], param.condition)
            if label_key not in seen_labels:
                seen_labels.add(label_key)

                # ✅ SYNCHRONIZED: Build display row respecting hidden columns
                display_row = dict(formatted_row)
                if 'Min' in hidden_columns:
                    display_row['Min'] = None
                if 'Typ' in hidden_columns:
                    display_row['Typ'] = None
                if 'Max' in hidden_columns:
                    display_row['Max'] = None

                display_tables[param.section].append(display_row)

        # ✅ NEW: Generate relation-centric ground truth for OpenIE
        metadata = {
            "component_type": result.context.component_type,
            "package": result.context.package,
            "archetype": result.context.archetype,
            "process_corner": getattr(result.context, 'process_corner', "N/A")
        }

        relation_triples = self._generate_relation_triples(ground_truth, metadata)

        return {
            "id": result.context.sample_id,
            "metadata": metadata,
            "rendering_config": {
                "hidden_columns": hidden_columns,
                "injected_param_keys": injected_keys,
                "transposed_sections": config.transposed_sections if config else []
            },
            "ground_truth": ground_truth,  # Entity-centric (original)
            "relation_ground_truth": relation_triples,  # ✅ NEW: Relation-centric for OpenIE
            "display_data": display_tables,
            "marketing_generated": marketing_data if marketing_data else {}
        }

    def _determine_column_model(self, p) -> str:
        has_min = p.value_min is not None
        has_max = p.value_max is not None
        has_typ = p.value_typ is not None
        if has_min and has_max and has_typ:
            return "MIN_TYP_MAX"
        if has_min and has_max:
            return "MIN_MAX"
        if has_typ and has_max:
            return "TYP_MAX"
        if has_typ and has_min:
            return "TYP_MIN"
        if has_max and not has_min and not has_typ:
            return "MAX_ONLY"
        if has_min and not has_max and not has_typ:
            return "MIN_ONLY"
        if has_typ:
            return "TYP_ONLY"
        return "UNKNOWN"
