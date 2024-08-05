#from nltk.corpus import wordnet31 as wn
#from nltk.corpus import wordnet as wn
#from nltk.corpus import wordnet_ic as info_content
from nltk.data import find
from nltk.corpus import WordNetCorpusReader


english_wordnet_dir = find('corpora/english-wordnet-2023')
wn = WordNetCorpusReader(english_wordnet_dir, r'.*')

# Information content
info_content = wn.ic(wn, False)

