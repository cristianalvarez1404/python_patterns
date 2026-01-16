import random
import httpx
from typing import Callable, Any
import time
from functools import wraps

#retry pattern => Wrap an operation that might fail and automatically retries it before givingz up.

def retry[T](
    operations: list[Callable[..., T]],
    delay: float = 1.0, 
    backoff:float = 2.0
) -> T:
  for attempt, operation in enumerate(operations):
    try:
      return operations()
    except Exception as e:
      print(f"Attempt {attempt + 1} failed: {e}")
      sleep_time = delay * (backoff ** (attempt - 1))
      print(f"Retrying in {sleep_time:.1f} seconds...")
      time.sleep(sleep_time)
  raise RuntimeError("Retries have failed.")  

def fetch_backup_api() -> str:
  """Fallback if the main API fails."""
  return "Backup API: Chuck Norris can delete the Recycle Bin."

def fetch_joke():
  """Fetch a random Chuck Norris joke from the API."""
  if random.random() < 0.8:
    raise RuntimeError("Chuck Norris is not happy.")

  with httpx.Client() as client:
    response = client.get("https://api.chucknorris.io/jokes/random")
    response.raise_for_status()
    data: dict[str, str] = response.json()
    return data
  
def main() -> None:
  print(retry([fetch_joke] * 3 + [fetch_backup_api]))

if __name__ == "__main__":
  main()