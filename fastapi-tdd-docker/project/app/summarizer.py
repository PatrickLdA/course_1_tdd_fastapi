import nltk
from newspaper import Article


def generate_summary(url: str) -> str:
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

    return article.summary