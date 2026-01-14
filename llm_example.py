import json
import os
import time
from functools import wraps
from typing import Any, Callable
from dotenv import load_dotenv
from openia import OpenAI

load_dotenv()

def retry_decorator[T](
    retries:int = 3, delay: float = 1.0, backoff:float = 2.0
) -> Callable[[Callable[...,T]], Callable[..., T]]:
  """A decorator that retries the wrapped function on failure."""

  def decorator(func:Callable[...,T])-> Callable[...,T]:
    @wraps(func)
    def wrapper(*args:Any, **kwargs:Any) -> T:
      for attemp in range(1, retries + 1):
        try:
          return func(*args,**kwargs)
        except Exception as e:
          print(f"Attemp {attemp} failed: {e}")
          if attemp == retries:
            raise 
          sleep_time = delay * (backoff ** (attemp - 1))
          print(f"Retrying in {sleep_time:.1f} seconds...")
          time.sleep(sleep_time)
      raise RuntimeError("All retries failed")
    return wrapper
  return decorator

@retry_decorator(retries=3, delay=1.0, backoff=2.0)
def get_user_info_with_retry(text:str, api_key:str) -> dict:
  client = OpenAI(api_key=api_key)

  response = client.responses.create(
    model= "gpt-4.1-nano",
    instructions = (
      "You are helpful assistant that extracts information and returns it "
      "as a valid JSON object. Always return valid JSON with keys 'name' and 'age'"
    ),
    input = f"Extract the user's name and age from this text: {text}" 
  )

  content = response.output_text
  return json.loads(content)

def main() -> None:
  """Example main function to demostrate retrying invalid JSON responses """
  api_key = os.getenv("OPEN_API_KEY","")
  
  text = "Hi, my name is Alice and I'm 30 years old."

  print("Requesting user info from the LLM...\n")
  try:
    user_info = get_user_info_with_retry(text, api_key)
    print("✅ Successfully parsed JSON: ")
    print(user_info)
  except json.JSONDecodeError as e:
    print("❌ The LLM returned invalid JSON after several retries:")
    print(e)
  except Exception as e:
    print("❌ An unexpected error occurred: ")
    print(e)

if __file__ == "__main__":
  main()