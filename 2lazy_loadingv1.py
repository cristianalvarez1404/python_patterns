import csv
from functools import cache

@cache
def load_sales(path:str) -> list[dict[str, str]]:
  """Eagerly load the entire CSV into memory."""
  print("Loading CSV data...")
  with open(path) as f:
    reader = csv.DictReader(f)
    return [row for row in reader]

def analyse_sales(sales: list[dict[str, str]]) -> float:
  total = 0.0
  for i, sale in enumerate(sales, start=1):
    total += float(sale["amount"])
  return total

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
        sales = load_sales("sales.csv")
        total = analyse_sales(sales=sales)
        print(f"Total sales: ${total:.2f}")
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