from nltk.corpus import WordNetCorpusReader
from nltk.data import find

english_wordnet_dir = find('corpora/english-wordnet-2023')
wn = WordNetCorpusReader(english_wordnet_dir, r'.*')

# Information content
info_content = wn.ic(wn, False)

