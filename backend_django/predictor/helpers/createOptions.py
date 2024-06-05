from nltk.corpus import wordnet as wn
import random

# 1: Find the synset for each keyword that is the most closely related - Done
# 1: Find all hypernyms for the chosen synsets - Not needed, the sense becomes lost
# 2: Find co-hyponyms and lemmas - Done


# Returns list of synsets based on keywords and formats blanked words by splitting
def getSynsets(keywords, blanked):
    sets = []
    format_blanked = [] # Checks which blanked keywords have synsets, they may need to be splitted
    for keyword in keywords:
        adjusted = keyword.replace(" ", "_") # Synsets only recognize underscores
        synsets = wn.synsets(adjusted)
        if synsets:
            sets.append(synsets)
            if keyword in blanked:
                format_blanked.append(keyword)
        else:
            format = keyword.split()
            for word in format:
                synsets = wn.synsets(word)
                if synsets:
                    sets.append(synsets)
                    if keyword in blanked:
                        format_blanked.append(word)
    
    return sets, format_blanked
# END getSynsets


# Returns list of hyponyms for a synset
def getHyponyms(synset):
    hyponyms_set = set()
    hyponyms = synset.hyponyms()
    for hyponym in hyponyms:
        hyponyms_set.update(hyponym.lemma_names())

    return list(hyponyms_set)
# END getHyponyms


# Computes avaergae similarity between corresponding synsets 
def averageSimilarity(synsets1, synsets2):
    mean = 0.0
    length = 0
    average_list = []
    for i in range(len(synsets1)):
        synset1 = synsets1[i]
        average_comparison = 0.0 # Average between examined synset and all other synset
        comparison_length = 0
        for synset2 in synsets2:
            similarity = synset1.path_similarity(synset2)    
            #print(f'Similarity between {synset1.lemma_names()} and {synset2.lemma_names()}: {round(similarity, 4)}')
            if similarity is not None:
                average_comparison += similarity
                comparison_length +=1
                mean += similarity
                length += 1

        average_comparison = round(average_comparison/comparison_length, 4)
        average_list.append(average_comparison)

        #print(f"Average for examined synset and all other synsets: {average_comparison}\n")
    mean = round(mean/length, 4)
    return mean, average_list
# END averageSimilarity


# Counts the number of times each synset is regarded as similar based on significance level
def voteSimilarity(synsets1, synsets2, significance, averages):
    votes = [0] * len(synsets2)
    for i in range(len(synsets1)):
        synset1 = synsets1[i]
        threshold = averages[i] * significance
        for j in range(len(synsets2)):
            synset2 = synsets2[j]
            similarity = synset1.path_similarity(synset2)
            if similarity > threshold:
                votes[j] += 1
            else:
                votes[j] -= 1
    return votes
# END voteSimilarity


# Returns a list of the most similar synsets between 2 words
def similarity(synsets1, synsets2):
    if not synsets1 or not synsets2:
        if not synsets1:
            return synsets2
        else:
            return synsets1

    # Calculates average similarity for each synset1 across all synsets2
    mean, average_list = averageSimilarity(synsets1, synsets2)
    
    # Identifies most similar synsets by using a 5% significance level and noting frequency of similar synsets
    SIGNIFICANCE = 1.05
    frequency = voteSimilarity(synsets1, synsets2, SIGNIFICANCE, average_list)
    similar = []

    #print(f"Limits: {[round(x*significance, 4) for x in average_list]}")
    #print(f"Votes for each synset in synsets2: {frequency}")

    # Populates similar list based on similarity and frequency/votes
    for i in range(len(synsets1)):
        synset1 = synsets1[i]
        threshold = average_list[i] * SIGNIFICANCE
        for j in range(len(synsets2)):
            synset2 = synsets2[j]
            similarity = synset1.path_similarity(synset2)
            if (similarity > threshold) and frequency[j] > -1:
                if synset1 not in similar:
                    similar.append(synset1)
                if synset2 not in similar:
                    similar.append(synset2)

    # Use average across all synsets
    if not similar:
        for i in range(len(synsets1)):
            synset1 = synsets1[i]
            for synset2 in synsets2:
                similarity = synset1.path_similarity(synset2)
                if similarity > mean:
                    if synset1 not in similar:
                        similar.append(synset1)
                    if synset2 not in similar:
                        similar.append(synset2)
    
    return similar
# END similarity


# Returns 2 lists, a prioritised list based on blanked words' synsets and a list of other extra synsets
def prioritise(synsets, blanked):
    priority = []
    other = []
    for ss in synsets:
        name = ss.name().split('.')[0]
        for blank in blanked:
            if (name in blank) and (ss not in priority):
                priority.append(ss)

    for ss in synsets:
        if (ss not in priority) and (ss not in other):
            other.append(ss)

    return priority, other


# Returns a list of possible answer options by randomly choosing related words
def getOptionsOld(blanked, priority, extra, NUMBER_OPTIONS):
    options = []
    while len(options) < NUMBER_OPTIONS:
        synsets = priority

        # Biased coin toss
        collection = random.randint(1, 10)
        if (collection > 7):
            synsets = extra

        set = random.randint(0, len(synsets)-1)
        synset = synsets[set]
        hyponyms_list = getHyponyms(synset)    
        
        # Randomly look for hyponyms first then synonyms
        if hyponyms_list:
            chosen = random.randint(0, len(hyponyms_list)-1)
            hyponym = hyponyms_list[chosen].replace("_", " ")
            if hyponym not in options and hyponym not in blanked:
                options.append(hyponym)
        else:
            synonyms_list = synset.lemma_names()
            if synonyms_list:
                chosen = random.randint(0, len(synonyms_list)-1)
                synonym = synonyms_list[chosen].replace("_", " ")
                if synonym not in options and synonym not in blanked:
                    options.append(synonym)
    
    return options
# END getOptions


# This might be less efficient but it allows for error checking incase there are not enough options generated
# Returns a list of possible answer options by randomly choosing related words - finds all possible words first
def getOptions(blanked, priority, extra, NUMBER_OPTIONS):
    options = []
    priority_list = []
    extra_list = []

    for synset in priority:
        hyponyms_list = getHyponyms(synset)    

        # Randomly look for hyponyms first then synonyms
        if hyponyms_list:
            for i in hyponyms_list:
                hyponym = i.replace("_", " ")
                if hyponym not in priority_list and hyponym not in blanked:
                    priority_list.append(hyponym)
        else:
            synonyms_list = synset.lemma_names()
            if synonyms_list:
                for i in synonyms_list:
                    synonym = i.replace("_", " ")
                    if synonym not in priority_list and synonym not in blanked:
                        priority_list.append(synonym)
    
    for synset in extra:
        hyponyms_list = getHyponyms(synset)    
        
        # Randomly look for hyponyms first then synonyms
        if hyponyms_list:
            for i in hyponyms_list:
                hyponym = i.replace("_", " ")
                if hyponym not in extra_list and hyponym not in blanked:
                    extra_list.append(hyponym)
        else:
            synonyms_list = synset.lemma_names()
            if synonyms_list:
                for i in synonyms_list:
                    synonym = i.replace("_", " ")
                    if synonym not in extra_list and synonym not in blanked:
                        extra_list.append(synonym)

    # Ensures there are enough options to choose from
    if (len(priority_list) >= NUMBER_OPTIONS) or (len(extra_list) >= NUMBER_OPTIONS):
        while len(options) < NUMBER_OPTIONS:
            # Biased coin toss, by default pick from prioritised but check if it is empty
            chosen = priority_list
            collection = random.randint(1, 10)
            if (collection > 7):
                chosen = extra_list

            if not extra_list:
                chosen = priority_list
            elif not priority_list:
                chosen = extra_list

            index = random.randint(0, len(chosen)-1)
            word = chosen[index]
            if word not in options:
                options.append(word)
                
    return options
# END getOptions
                   
                    

# Generates MCQ options to choose from based on keywords and blanked words within the answer
def generateOptions(keywords, blanked):
    all_sets, format_blanked = getSynsets(keywords, blanked)

    if len(all_sets) == 0:
        return []
    
    elif len(all_sets) > 1:
        synsets1 = all_sets[0] # Has 3 ss
        synsets2 = all_sets[1] # 2 ss
        merged = similarity(synsets1, synsets2)

        # merged is already filtered, you are just adding to it by examining the next synset
        for i in range(2, len(all_sets)):
            new_set = all_sets[i]
            merged = similarity(merged, new_set)
    else:
        merged = all_sets
    #print(f'{merged}\n')
    priority, extra = prioritise(merged, format_blanked)

    options = []
    for blanked_word in blanked:
        NUMBER_OF_OPTIONS = 3
        generated = getOptions(blanked_word, priority, extra, NUMBER_OF_OPTIONS)
        options.append(generated)
    return options
# END generateOptions



''' Main run '''

# Blank words was already identified
#blanked1 = ['gradient function']

# Keywords has already been extracted by RAKE, they are needed for using the right sense
#keywords1 = ['differentiation', 'gradient function']


#blanked2 = ['area', 'curve']
#keywords2 = ['process', 'finding', 'area', 'underneath', 'curve', 'useful', 'mechanics', 'analyze', 'scenarios']

#options = generateOptions(keywords2, blanked2)
#print(options)

# Efficiency needs improving, this takes 4 seconds minimum to generate 3 options for a single question!
# You have used loads of loops and nested loops, try thinking in parallel?




