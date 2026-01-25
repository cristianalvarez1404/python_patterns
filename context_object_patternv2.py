import logging
from db import Article, Session, db_session, init_db
from dataclasses import dataclass
from typing import Any

@dataclass
class AppContext:
  user_id: int
  db: Session
  logger: logging.Logger
  config: dict[str, Any]

# ------------------------------------
# Application Logic
# ------------------------------------

def render_article(
   article_id: int , context: AppContext 
) -> str:
  article = context.db.query(Article).filter(Article.id == article_id).first()

  if not article:
    context.logger.error(f"Article {article_id} not found.")
    return "<p>Article not found.</p>"

  context.logger.info(f"Rendering article {article_id} using API key {context.config['api_key'][:4]}...")
  html = f"<h1>{article.title}</h1><p>{article.body}</p>"
  return html

def send_to_external_service(html: str, context: AppContext):
  api_key = context.config["api_key"]
  print(f"Sending to API with key {api_key[:4]}... Content: {html[:30]}...")

def publish_article(article_id: int, context: AppContext):
  if context.user_id != 42:
    context.logger.error(f"Unauthorized access by user {context.user_id}.")
    return "<p>Unauthorized</p>"
  html = render_article(article_id, context)
  send_to_external_service(html, context)


def main() -> None:
  logging.basicConfig(level=logging.INFO)
  logger = logging.getLogger("app")

  init_db()

  with db_session() as session:
    api_key = "abcdef123456"

    context = AppContext(
      user_id = 42,
      db = session,
      logger = logger,
      config = {"api_key":api_key} 
    )

    publish_article(1, context)
    publish_article(999, context)

if __name__ == "__main__":
  main()