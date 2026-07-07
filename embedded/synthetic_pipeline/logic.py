from typing import Dict, Any, List, Optional

from synthetic_pipeline.data_types import (
    GenerationContext,
    GeneratedParameter,
    DatasheetResult,
    SpecType,
    EngineeringClass,
)

from synthetic_pipeline.strategy_base import ComponentStrategy


class DatasheetGenerator:
    """
    The Engine: Orchestrates data generation.
    Updated to support MULTIPLE SCENARIOS per parameter AND Strategy Hooks.
    """
    def __init__(self, db_schema: Dict[str, Any]):
        self.db = db_schema

    def generate(self, component_type: str, strategy: ComponentStrategy, 
                 process_corner: Optional[str] = None) -> DatasheetResult:
        
        if component_type not in self.db:
            raise ValueError(f"Unknown component: {component_type}")
        
        # 1. Create Context
        schema = self.db[component_type]
        context = strategy.create_context(schema, process_corner)
        
        parameters: List[GeneratedParameter] = []

        # ✅ Step 2A: Process resistance FIRST (if exists)
        resistance_param = None
        for section_name, params_config in schema.items():
            if section_name == "archetypes": 
                continue
                
            for config in params_config:
                key = config["key"]
                
                if key == "resistance":
                    custom_param = strategy.create_custom_parameter(key, context, config)
                    if custom_param is not None:
                        resistance_param = custom_param
                    break
            
            if resistance_param:
                break
        
        # Add resistance to list
        if resistance_param:
            parameters.append(resistance_param)
        
        # ✅ Step 2B: Process all OTHER parameters
        for section_name, params_config in schema.items():
            if section_name == "archetypes": 
                continue
            
            for config in params_config:
                key = config["key"]
                
                # Skip resistance (already processed)
                if key == "resistance":
                    continue
                
                # Check Hook
                custom_param = strategy.create_custom_parameter(key, context, config)
                if custom_param is not None:
                    parameters.append(custom_param)
                    continue
                
                # Fallback logic
                param_results = self._process_parameter(config, section_name, context, strategy)
                if param_results:
                    parameters.extend(param_results) 
        
        # 3. Finalize
        result = DatasheetResult(context=context, parameters=parameters)
        strategy.apply_correlations(result)
        return result

    def _process_parameter(self, config: Dict, section: str, 
                           ctx: GenerationContext, strategy: ComponentStrategy) -> List[GeneratedParameter]:
        """
        מעבד פרמטר ומחזיר רשימה של תוצאות - אחת לכל תרחיש (Scenario) רלוונטי.
        """
        results = []
        
        # A. Get all relevant scenarios
        scenarios = self._filter_scenarios(config.get("scenarios", []), ctx.package)
        
        if not scenarios: return []

        # B. Metadata Extraction
        formal_name = config.get("llm_context", {}).get("formal_name")
        if not formal_name:
            formal_name = config.get("label", config["key"])
        symbol = config.get("symbol", "")
        
        try: s_type = SpecType(config.get("spec_type", "nominal"))
        except: s_type = SpecType.NOMINAL
        
        try: e_class = EngineeringClass(config.get("engineering_class", "PERFORMANCE"))
        except: e_class = EngineeringClass.PERFORMANCE

        # Loop over all scenarios
        for scenario in scenarios:
            
            # 1. Engineering Calculation
            base_val = strategy.calculate_base_value(config["key"], scenario["limits"], ctx)
            if base_val is None: continue 

            # 2. Calculate Limits using Strategy Logic
            # התיקון: מעבירים את ה-strategy לפונקציה
            min_v, typ_v, max_v = self._calculate_smart_limits(
                base_val, s_type, ctx.tolerance, config["std_unit"], config["key"], strategy
            )

            # 3. Create Parameter Object
            param_obj = GeneratedParameter(
                key=config["key"],
                label=formal_name,
                symbol=symbol,
                section=section,
                value_min=min_v,
                value_typ=typ_v,
                value_max=max_v,
                unit=config["std_unit"],
                condition=scenario.get("condition", ""),
                spec_type=s_type,
                engineering_class=e_class
            )
            
            results.append(param_obj)
        
        return results

    # --- Helpers ---

    def _filter_scenarios(self, scenarios, package):
        return scenarios 

    def _calculate_smart_limits(self, val, spec_type, tol, unit, key, strategy: ComponentStrategy):
        """
        פונקציית עזר המרכזת את לוגיקת ה-Atomic Rounding.
        תיקון: שימוש במתודות של strategy במקום globals.
        """
        if not isinstance(val, (int, float)):
            return None, val, None

        min_v, typ_v, max_v = None, None, None
        tol_decimal = tol / 100.0 

        # קריאה לפונקציית העיגול מתוך האסטרטגיה
        if spec_type == SpecType.MAX_RATING or spec_type == SpecType.MAX_LIMIT:
            max_v = val
            _, _, max_v = strategy.apply_final_rounding_atomic((None, None, max_v), tol, unit, key)
            
        elif spec_type == SpecType.MIN_LIMIT:
            min_v = val
            min_v, _, _ = strategy.apply_final_rounding_atomic((min_v, None, None), tol, unit, key)
            
        else: # NOMINAL
            typ_v = val
            min_v, typ_v, max_v = strategy.apply_final_rounding_atomic((None, typ_v, None), tol, unit, key)
            
            # Fallback Logic (רק אם האסטרטגיה החזירה None לטווח)
            if min_v is None and max_v is None and typ_v is not None:
                typ_v = round(val, 2)
                min_v = typ_v * (1 - tol_decimal)
                max_v = typ_v * (1 + tol_decimal)

        return min_v, typ_v, max_v
