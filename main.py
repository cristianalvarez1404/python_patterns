import random
import httpx
from typing import Callable, Any
import time
from functools import wraps

#retry pattern => Wrap an operation that might fail and automatically retries it before giving up.

def retry_decorator[T](
    retries:int = 3, 
    delay: float = 1.0, 
    backoff:float = 2.0):
  
  def decorator(func:Callable[...,T]) -> Callable[...,T]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
      for attempt in range(1, retries + 1):
        try:
          return func()
        except Exception as e:
          print(f"Attempt {attempt} failed: {e}")
          if attempt == retries:
            raise e
          sleep_time = delay * (backoff ** (attempt - 1))
          print(f"Retrying in {sleep_time:.1f} seconds...")
          time.sleep(sleep_time)

    return wrapper

  return decorator

@retry_decorator()
def fetch_joke():
  """Fetch a random Chuck Norris joke from the API."""
  if random.random() < 0.5:
    raise RuntimeError("Chuck Norris is not happy.")

  with httpx.Client() as client:
    response = client.get("https://api.chucknorris.io/jokes/random")
    response.raise_for_status()
    data: dict[str, str] = response.json()
    return data
  
def main() -> None:
  joke = fetch_joke()
  print(joke)

if __name__ == "__main__":
  main()