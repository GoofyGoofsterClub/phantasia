import os
import importlib

models_dir = os.path.dirname(__file__)

for filename in os.listdir(models_dir):
    if filename.endswith(".py") and filename not in {"__init__.py", "__pycache__"}:
        module_name = f"{__package__}.{filename[:-3]}"
        importlib.import_module(module_name)