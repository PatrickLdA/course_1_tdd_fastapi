import nltk
from newspaper import Article

from app.models.tortoise import TextSummary


async def generate_summary(summary_id: int, url: str) -> None:
    article = Article(url)  # Creation of article
    article.download()  # Download of the file
    article.parse()  # Extraction of meaningfull content

    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt")
    try:
        nltk.data.find("punkt_tab")
    except LookupError:
        nltk.download('punkt_tab')
    finally:
        article.nlp()  # Extraction of relevant keywords

    summary = article.summary

    await TextSummary.filter(id=summary_id).update(summary=summary)