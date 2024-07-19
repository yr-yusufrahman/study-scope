from predictor.helpers.quiz.distractors import getRelatedWords
from predictor.helpers.quiz.keywordOptions import optionsFromKeywords
import random


# Pick 3 words from a list of words
def chooseOptions(words_list):
    options = []
    
    if words_list:
        first_list = words_list[0]
        if len(first_list) >= 3:
            options = random.sample(first_list, 3)
        else:
            # Add all elements from the first list
            options.extend(first_list)
            
            # Keep track of the lists and their lengths
            remaining_lists = words_list[1:]
            all_words = [word for sublist in remaining_lists for word in sublist]
            
            # Continue picking until we have 3 words
            while len(options) < 3 and all_words:
                additional_word = random.choice(all_words)
                if additional_word not in options:
                    options.append(additional_word)
                    all_words.remove(additional_word)

        # Replace underscores with spaces in the selected words
        options = [x.replace("_", " ") for x in options]
    
    return options


# Generates 3 options for each word in a list based on a category (course)
def generateOptions(word_list, category, keywords, number_of_options):
    completed_words = []
    options = []
    list_changed = False

    for word in word_list:
        checked_word, all_related = getRelatedWords(word, category)
        chosen_words = chooseOptions(all_related)

        # If a word has options, add its options and the word to the list
        if len(chosen_words) == number_of_options:
            formatted_word = checked_word.replace("_", " ")
            completed_words.append(formatted_word)
            options.append(chosen_words)

            # Check if the phrase was broken down a word
            if word != formatted_word:
                list_changed = True
        else:
            # If 2 options were found, get the third option from the keywords?
            # If no options are found by looking at the course, get options from the keywords
            backup_options = optionsFromKeywords(keywords, [word])
            if backup_options:
                backup_options = backup_options[0]
                if len(backup_options) == number_of_options:
                    formatted_word = checked_word.replace("_", " ")
                    completed_words.append(formatted_word)
                    options.append(backup_options)

                    # Check if the phrase was broken down a word
                    if word != formatted_word:
                        list_changed = True
                    
            else:
                list_changed = True
    
    return options, completed_words, list_changed

