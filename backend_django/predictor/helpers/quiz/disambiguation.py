from predictor.helpers.quiz.corpus import wn, info_content


# Checks similarity of the domain a given synset belongs to
def domainSimilarity(synset, compare_synset):
    highest = 0
    domains = synset.topic_domains()

    if not domains:
        # The word may have to be converted into another form
        for lemma in synset.lemmas():
            forms = lemma.derivationally_related_forms()
            
            for lemma_obj in forms:
                # Get the synset of the lemma to find topic domains
                derived_synset = wn.synset_from_sense_key(lemma_obj.key())
                domains += derived_synset.topic_domains()

        # The hypernym of the word may belong to a domain
        hypernyms = synset.hypernyms()
        for hypernym in hypernyms:
            domains += hypernym.topic_domains()
    
    # Check similarity between domain and the synset to be compared with (course) 
    if domains:
        for topic in domains:
            similarity = topic.path_similarity(compare_synset)
            if similarity > highest:
                highest = similarity
    
    return highest
    

# Checks position of speech and calculates similarity for 2 synsets
def posSimilarity(synset1, synset2):
    similarity = 0
    same_pos = synset1.pos() == synset2.pos()
    if same_pos:
        similarity = synset1.jcn_similarity(synset2, info_content)
    else:
        similarity = synset1.wup_similarity(synset2)
    similarity = round(similarity, 5)
    
    return same_pos, similarity


# Calculates average
def averageSimilarity(total, length):
    if length == 0:
        return 0
        
    total /= length
    total = round(total, 5)
    return total


# Calculate similarities between a hypernyms list and hyponyms of a synset
def derivedComparison(hypernyms_list, synset):
    length = len(hypernyms_list)
    hyper_synset_similarity = 0
    hyper_hypo_similarity = 0
    hypo_counter = 0
    
    for hypernym in hypernyms_list:
        similarity = hypernym.path_similarity(synset)
        hyper_synset_similarity += round(similarity, 5)
    
        # Check similarity with the blanked word synset and the hyponyms of the given course
        hyponyms = synset.hyponyms()
        hypo_counter += len(hyponyms)
        for hyponym in hyponyms:
            similarity = hypernym.wup_similarity(hyponym)
            hyper_hypo_similarity += round(similarity, 5)
    
    # Average similarity between the hypernyms of the word and the course synset
    hyper_synset_similarity = averageSimilarity(hyper_synset_similarity, length)
    hyper_hypo_similarity = averageSimilarity(hyper_hypo_similarity, hypo_counter)

    return hyper_synset_similarity, hyper_hypo_similarity


# All possible senses of a word and their similarities to a course
def allSenses(word, course):
    word_synsets = wn.synsets(word)
    course_synsets = wn.synsets(course)
    data = []
    
    # Iterate through each possible sense of the blanked word
    for i in range(len(word_synsets)):
        word_synset = word_synsets[i]
        synset_data = {
            "word_synset_name": word_synset.name(),
            "related_courses": []
        }
        
        course_similarities = []
        blanked_hypernyms = word_synset.hypernyms()
        for course_synset in course_synsets:
            course_data = {
                "course_synset_name": course_synset.name(),
                "same_pos": True,
                "domain": 0,
                "word_course": 0,
                "hyper_course": 0,
                "hyper_course_hypo": 0
            }

            # Find the domain of the word and its similarity to the course
            domain = domainSimilarity(word_synset, course_synset)
            course_data.update({"domain": domain})
            
            # Check if the two synsets have the same POS
            same_pos, word_course_similarity = posSimilarity(word_synset, course_synset)
            if not same_pos:
                course_data.update({"same_pos": False})
            course_data.update({"word_course": word_course_similarity})
            
            # Average similarities between word hypernyms and course + its hyponyms
            hyper_course, hyper_course_hypo = derivedComparison(blanked_hypernyms, course_synset)
            
            course_data.update({"hyper_course": hyper_course})
            course_data.update({"hyper_course_hypo": hyper_course_hypo})
            course_similarities.append(course_data)
    
        synset_data.update({"related_courses": course_similarities})
        data.append(synset_data)
        
    return data


# Returns a max of 3 synsets that have the highest similarity from a given dict list
def findSense(sense_dict):
    priority = []
    different_pos = []
    for synset in sense_dict:
        name = synset.get('word_synset_name')
        course_data = synset.get('related_courses')
        for course in course_data:
            course_name = course.get('course_synset_name')
            term_score = (10*course.get('hyper_course')) + course.get('hyper_course_hypo')
            score = (course.get('word_course') * term_score) + (100*course.get('domain'))
            score = round(score, 5)

            dict = {"word": name, "course": course_name, "score": score}
            if course.get('same_pos'):
                if dict not in priority:
                    priority.append(dict)
            else:
                if dict not in different_pos:
                    different_pos.append(dict)
    filtered = []
    
    # Check if the lists are not empty
    if priority:
        priority.sort(key=lambda x: x['score'], reverse=True)
        if len(priority) > 1:
            filtered += priority[:2] # First 2 items
        else:
            filtered += priority
            
    if different_pos:
        different_pos.sort(key=lambda x: x['score'], reverse=True)
        filtered += different_pos
    else:
        filtered = priority

    if len(filtered) > 3:
        filtered = filtered[:3]
        
    return filtered


# Get the sense of a word that has the highest similarity to a course
def getSense(word, course):
    sense_dict = allSenses(word, course)
    possible_senses = findSense(sense_dict)
    return possible_senses
