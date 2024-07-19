from predictor.helpers.quiz.disambiguation import getSense
from predictor.helpers.quiz.corpus import wn, info_content


# From a synset, look at its hypernyms and generate hyponyms
def getHyponyms(synset):
    hypernyms = synset.hypernyms()
    all_hyponyms = []
    for hypernym in hypernyms:
        hyponyms = hypernym.hyponyms()
        
        for hyponym in hyponyms:
            if (hyponym not in all_hyponyms) and hyponym.name() != synset.name():
                all_hyponyms.append(hyponym)

    return all_hyponyms


# Gets words from a given list of hyponyms
def deriveWords(hyponyms_list):
    words = []
    for hyponym in hyponyms_list:
        words += hyponym.lemma_names()
        
    return words


# Get co-hyponyms from a given synset
def getCoHyponyms(synset):
    # Get hyponyms from hypernyms of the synset
    co_hyponyms = getHyponyms(synset)

    # Find words from the co-hyponyms
    found_words = deriveWords(co_hyponyms)
    return found_words


# Check if a given phrase has synsets, if not, split the phrase into words
def splitPhrase(phrase):
    phrase = phrase.replace(" ", "_")
    synsets = wn.synsets(phrase)
    if not synsets:
        phrase = phrase.replace("_", " ") # Split separate words
        return phrase.split()
        
    return [phrase] 


# Get related words from a given word
def getRelatedWords(word, course):
    words = []

    # Check if given word/phrase has synsets, if not, split the phrase into words
    phrase_split = splitPhrase(word) #checkPhrase(word)

    highest = 0
    best_senses = []
    chosen_word = ""
    for phrase in phrase_split:
        # Get correct sense
        senses = getSense(phrase, course)
        if senses:
            score = senses[0].get("score") 
            if score > highest:
                highest = score
                best_senses = senses
                chosen_word = phrase

    for dict in best_senses:
        sense = dict.get("word")
        synset = wn.synset(sense)
    
        # Get hyponyms from hypernyms of the synset
        co_hyponyms = getCoHyponyms(synset) #getHyponyms(synset)
    
        # Find words from the co-hyponyms
        #found = deriveWords(co_hyponyms)
        words.append(co_hyponyms)
    
    return chosen_word, words

