import json
from bs4 import BeautifulSoup
from experiment import Experiment
from xml_adapter import get_from_bs
from functools import partial

def main() -> None:
  with open("config.json", encoding="utf8") as file:
    config = file.read()
  
  bs = BeautifulSoup(config, "xml")
  get_from_bs_adpater = partial(get_from_bs, bs)

  experiment = Experiment(get_from_bs_adpater)
  experiment.run()

# def main() -> None:
#   with open("config.json", encoding="utf8") as file:
#     config = json.load(file)
  
#   experiment = Experiment(config.get)
#   experiment.run()

if __name__ == "__main__":
  main()