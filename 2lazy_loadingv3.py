import csv
from functools import cache,wraps
import time
from typing import Callable, Any

def ttl_cache(seconds: int) -> Callable[[Callable[..., Any]], Callable[...,Any]]:
  def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
    cache_data = {}
    cache_time = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
      key = (args, tuple(kwargs.items()))
      now = time.time()

      #Return cached result if still valid
      if key in cache_data and (now - cache_data[key]) < seconds:
        return cache_data[key]
      
      #Otherwise recompute and store
      result = func(*args, **kwargs)
      cache_data[key] = result
      cache_time[key] = now
      return result

    return wrapper
  
  return decorator

@cache
def load_sales(path:str) -> list[dict[str, str]]:
  """Eagerly load the entire CSV into memory."""
  print("Loading CSV data...")
  with open(path) as f:
    reader = csv.DictReader(f)
    return [row for row in reader]

# @cache #This is not the best option, the conversion change. Here we'll need to restart the app.
@ttl_cache(seconds=60)
def get_conversion_rates() -> dict[str, float]:
  print("fetching conversion rates from remote service...")
  time.sleep(2)
  return {"USD":1.0,"EUR":1.1,"JPY":0.007}

def analyse_sales(sales: list[dict[str, str]], currency:str) -> float:
  total = sum(float(s["amount"]) for s in sales)
  rate = get_conversion_rates().get(currency, 1.0)
  return total * rate

def count_sales(sales: list[dict[str, str]]) -> int:
  return len(sales)

def main() -> None:
  while True:
    print("\nChoose an option:")
    print("1. Analyse sales data")
    print("2. Count total sales records")
    print("3. Quit")

    choice = input("> ")
    
    match choice:
      case "1":
        currency = input("Enter currency (USD/EUR/JPY): ").upper() or "USD"
        sales = load_sales("sales.csv")
        total = analyse_sales(sales=sales,currency=currency)
        print(f"Total sales in currency {currency}: {total:.2f}")
      case "2":
        sales = load_sales("sales.csv")
        count = count_sales(sales=sales)
        print(f"Number of sales: {count:,}")
      case "3":
        print("Goodbye!")
        return
      case _:
        print("Invalid choice, try again.")

if __name__ == "__main__":
  main()