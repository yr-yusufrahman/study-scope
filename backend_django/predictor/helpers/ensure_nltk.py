import nltk


def ensure_nltk_data():
    """Download tokenizer data needed by rake-nltk for quiz generation."""
    packages = ("punkt_tab", "punkt", "stopwords")
    for package in packages:
        resource = f"tokenizers/{package}" if package.startswith("punkt") else f"corpora/{package}"
        try:
            nltk.data.find(resource)
        except LookupError:
            nltk.download(package, quiet=True)
