import json
from typing import Any,Callable

type Data = list[dict[str, Any]]

def load_data_from_csv() -> Data:
    # Simulate reading from CSV
    return [
      {"name":"Arjan", "age": 37},
      {"name":"Jane", "age": None},
      {"name":"Bob", "age": 45},
    ]    

def export_to_json(data: Data) -> None:
  with open("output.json", "w") as f:
    json.dump(data, f, indent = 2)

def clean_data(data: Data) -> Data:
  return [row for row in data if row["age"] is not None]
    
class DataPipeline:
  def run(self, loader_fn:Callable[[], Data]) -> None:
    data = loader_fn()
    cleaned = clean_data(data)
    export_to_json(cleaned)

def main() -> None:
  pipeline = DataPipeline()
  pipeline.run(loader_fn=load_data_from_csv)
  print("Pipeline completed. Output written to output.json")

if __name__ == "__main__":
  main()