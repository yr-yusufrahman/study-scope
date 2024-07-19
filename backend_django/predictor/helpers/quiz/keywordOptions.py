from predictor.helpers.quiz.corpus import wn, info_content
import random

# 1: Find the synset for each keyword that is the most closely related - Done
# 1: Find all hypernyms for the chosen synsets - Not needed, the sense becomes lost
# 2: Find co-hyponyms and lemmas - Done


# Returns list of synsets based on keywords and formats blanked words by splitting
def getSynsets(keywords, blanked):
    sets = []
    format_blanked = [] # Checks which blanked keywords have synsets, they may need to be splitted
    for keyword in keywords:
        formatted_keyword = keyword.replace(" ", "_") # Synsets only recognize underscores
        synsets = wn.synsets(formatted_keyword)

        if synsets:
            sets.append(synsets)
            if keyword in blanked:
                format_blanked.append(keyword)
        else:
            # If no synsets are found for the key term, split into separate words, search for synsets
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
    for ss in synsets: # One of the ss is a list of synsets but the others are single synsets
        #print(f"Synset: {ss}")
        #print(f"Name: {ss.name()},\n")
        name = ss.name().split('.')[0]
        for blank in blanked:
            if (name in blank) and (ss not in priority):
                priority.append(ss)

    for ss in synsets:
        if (ss not in priority) and (ss not in other):
            other.append(ss)

    return priority, other
# END prioritise


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
                   
            

# Generates MCQ options to choose from based on keywords and a blanked word within the answer
def optionsFromKeywords(keywords, blanked):
    # Get a collection of synsets for each keyword and format blanked words - list of lists
    all_sets_collection, format_blanked = getSynsets(keywords, blanked)
    
    # If no synsets are found, no options can be generated
    if len(all_sets_collection) == 0:
        return []

    if len(all_sets_collection) == 1:
        # If there is 1 collection of synsets, use it
        merged = all_sets_collection[0]

    # If there are collections of synsets, compare them and merge them, starting with the first 2
    else:
        synsets1 = all_sets_collection[0]
        synsets2 = all_sets_collection[1]

        merged = similarity(synsets1, synsets2)

        # Examine remaining collections of synsets and merge them with the merged collection
        for i in range(2, len(all_sets_collection)):
            new_set = all_sets_collection[i]
            merged = similarity(merged, new_set)

    # Prioritise synsets based on blanked words and separate the rest
    priority, extra = prioritise(merged, format_blanked)

    options = []
    for blanked_word in blanked:
        NUMBER_OF_OPTIONS = 3
        generated = getOptions(blanked_word, priority, extra, NUMBER_OF_OPTIONS)

        # If there are not enough options
        if len(generated) < NUMBER_OF_OPTIONS:
            return []
        options.append(generated)
    return options
# END generateOptions


# Efficiency needs improving, this takes 4 seconds minimum to generate 3 options for a single question!
# You have used loads of loops and nested loops, try thinking in parallel?

