import json
from typing import Callable, Any

type Data = dict[str, Any]
type ExportFn = Callable[[Data], None]


def export_pdf(data: Data) -> None:
  print(f"Exporting data to PDF: {data}")


def export_csv(data: Data) -> None:
  print(f"Exporting data to CSV: {data}")


def export_json(data: Data) -> None:
  print("Exporting data to JSON:")
  print(json.dumps(data, indent = 2))


def export_data(data: Data, format: str) -> None:
  if format == "pdf":
    export_pdf(data)
  elif format == "csv":
    export_csv(data)
  elif format == "json":
    export_json(data)
  else:
    raise ValueError(f"❌ No exporter found for format: {format}")


def main() -> None:
  sample_data: Data = {"name": "Alice", "age": 30}

  export_data(sample_data, "pdf")
  export_data(sample_data, "csv")
  export_data(sample_data, "json")


if __name__ == "__main__":
  main()