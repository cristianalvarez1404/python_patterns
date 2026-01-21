import json
from typing import Any, Callable, Protocol

type Data = list[dict[str, Any]]

class InMemoryLoader:
  def load(self) -> Data:
      # Simulate reading from CSV
      return [
        {"name":"Arjan", "age": 37},
        {"name":"Jane", "age": None},
        {"name":"Bob", "age": 45},
      ]    

class CleanMissingFields:
  def transform(self, data: Data) -> Data:
    return [row for row in data if row["age"] is not None]
      
class JSONExporter:
  def __init__(self, filename: str) -> None:
    self.filename = filename

  def export(self, data: Data) -> None:
    with open(self.filename, "w") as f:
      json.dump(data, f, indent = 2)

class DataPipeline:
  def __init__(
      self, 
      loader:InMemoryLoader, 
      transformer: CleanMissingFields, 
      exporter:JSONExporter
  ) -> None:
    self.loader = loader
    self.transformer = transformer
    self.exporter = exporter

  def run(self) -> None:
    data = self.loader.load()
    transformed = self.transformer.transform(data)
    self.exporter.export(transformed)

def main() -> None:
  loader = InMemoryLoader()
  transformer = CleanMissingFields()
  exporter = JSONExporter("output.json")

  pipeline = DataPipeline(loader,transformer,exporter)
  pipeline.run()
  print("Pipeline completed. Output written to output.json")

if __name__ == "__main__":
  main()