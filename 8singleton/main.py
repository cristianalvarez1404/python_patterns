import config
# from singlenton import Singleton

def main() -> None:
  if config.debug:
    print(config.db_uri)


# class Config(metaclass = Singleton):
#   def __init__(self):
#     self.db_url = "sqlite:///:memory:"
#     self.debug = True

#   def __str__(self) -> str:
#     return f"Config(db_url={self.db_url}, debug={self.debug})"
  
# def main():
#   s1 = Config()
#   s2 = Config()

#   print(s1 is s2)
#   print(id(s1))
#   print(id(s2))

if __name__ == "__main__":
  main()