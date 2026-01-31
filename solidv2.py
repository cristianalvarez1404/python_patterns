import json
from datetime import datetime
from typing import Protocol, Any
import pandas as pd

class Metric(Protocol):
  def compute(self, df: pd.DataFrame) -> dict[str, Any]:
    ...

class CustomerCountMetric:
  def compute(self, df: pd.DataFrame) -> dict[str, Any]:
    return {"number_of_customers": df["name"].nunique()}

class AverageOrderValueMetric:
  def compute(self, df: pd.DataFrame) -> dict[str, Any]:
    avg_order = (
      df[df["price"] > 0]["price"].mean() if not df[df["price"] > 0].empty else 0
    )
    return {"average_order_value (pre-tax)": round(avg_order, 2)}

class ReturnPercentageMetric:
  def compute(self, df: pd.DataFrame) -> dict[str, Any]:
    returns = df[df["price"] < 0]
    return_pct = (len(returns) / len(df)) * 100 if len(df) > 0 else 0
    return {"percentage_of_returns": round(return_pct, 2)}

class TotalSalesMetric:
  def compute(self, df: pd.DataFrame) -> dict[str, Any]:
    total_sales = df["price"].sum()
    return {"total_sales_in_period (pre-tax)": round(total_sales, 2)}

class MessySalesReport:
  def __init__(self, metrics:list[Metric]) -> None:
    self.metrics = metrics

  def generate(
      self,
      input_file: str,
      ouput_file: str,
      start_date: datetime | None = None,
      end_date: datetime | None = None,
  ) -> None :
    df = pd.read_csv(input_file, parse_dates=["date"])

    if start_date:
      df = df[df["data"] >= pd.Timestamp(start_date)]
    if end_date:
      df = df[df["data"] <= pd.Timestamp(end_date)]

    report_data = {}
    for metric in self.metrics:
      report_data.update(metric.compute(df))

    report = {
      "report_start": start_date.strftime("%Y-%m-%d") if start_date else "N/A",
      "report_end": end_date.strftime("%Y-%m-%d") if end_date else "N/A",
      **report_data
    }

    with open(ouput_file, "w") as f:
      json.dump(report, f, indent=2)

def main() -> None:
  report = MessySalesReport(
    metrics=[
      CustomerCountMetric(),
      AverageOrderValueMetric(),
      ReturnPercentageMetric(),
      TotalSalesMetric()
    ]
  )
  report.generate(
    input_file="sales_data.csv",
    ouput_file="sales_report.json",
    start_date=datetime(2024, 1, 1),
    end_date=datetime(2024, 12, 31)
  )

if __name__ == "__main__":
  main()