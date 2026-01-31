from functools import wraps
from typing import Any, Callable

_registry: list[tuple[str, str, Callable[..., None]]] = []

def register_command(group: str, name: str):
  def decorator(func: Callable[..., None]):
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
      return func(*args, **kwargs)
    
    _registry.append((group, name, wrapper))
    return wrapper
  
  return decorator

def get_registry() -> list[tuple[str, str, Callable[..., None]]]:
  return _registry.copy()