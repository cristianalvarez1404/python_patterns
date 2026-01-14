import os
import serpapi
from dotenv import load_dotenv

SERP_API_KEY = os.getenv("SERP_API_KEY", "")

def main() -> None:
  client = serpapi.Client(api_key = SERP_API_KEY)
  s = client.search(
    q = "Software design principles Python",
    engine = "google",
    location = "Utrecht",
  )

  print(s["organic_results"][0])


if __name__ == "__main__":
  main()