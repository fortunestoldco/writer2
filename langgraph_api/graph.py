import os
import importlib
import logging

logger = logging.getLogger(__name__)

def collect_graphs_from_env(strict: bool = False):
    graphs = {}
    for key, value in os.environ.items():
        if key.startswith("LANGGRAPH_"):
            try:
                if isinstance(value, dict):
                    module = value.get("module")
                    function = value.get("function")
                else:
                    module = value.split(":")[0]
                    function = value.split(":")[1]
                mod = importlib.import_module(module)
                func = getattr(mod, function)
                graphs[key] = func
            except Exception as e:
                if strict:
                    raise
                logger.error(f"Failed to import {key}: {e}")
    return graphs
