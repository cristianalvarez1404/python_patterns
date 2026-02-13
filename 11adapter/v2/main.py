import json
from bs4 import BeautifulSoup
from experiment import Experiment
from xml_adapter import XMLConfig

def main() -> None:
  with open("config.xml", encoding="utf8") as file:
    config = file.read()
  bs = BeautifulSoup(config, "xml")
  adapter = XMLConfig(bs=bs)
  experiment = Experiment(adapter)
  experiment.run()

if __name__ == "__main__":
  main()