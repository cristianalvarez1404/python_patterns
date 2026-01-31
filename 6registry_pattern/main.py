import importlib
import pkgutil

import typer
from registry import get_registry

app = typer.Typer()

def load_text_commands() -> None:
  import commands.text

  for _, module_name, _ in pkgutil.iter_modules(commands.text.__path__):
    importlib.import_module(f"commands.text.{module_name}")

def load_plugins() -> None:
  import plugins

  for _, module_name, _ in pkgutil.iter_modules(plugins.__path__):
    importlib.import_module(f"plugins.text.{module_name}")

