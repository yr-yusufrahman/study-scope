from predictor.helpers.blankWords import multipleBlank
from predictor.helpers.quiz.choices import generateOptions
from predictor.helpers.ensure_nltk import ensure_nltk_data

from rake_nltk import Rake
import random

ensure_nltk_data()


# First, iterate through content and for each question/answer:
# Extract keywords, blank some words, generate options


# Gets letter-only keywords from a given text
def extractKeywords(rake, text):
    rake.extract_keywords_from_text(text)
    extracted_words = list(set(rake.get_ranked_phrases()))

    # Remove symbols, numbers and leading/trailing spaces from keywords
    valid_words = ["".join(c for c in word if c.isalpha() or c.isspace()) for word in extracted_words if any(c.isalpha() or c.isspace() for c in word)]
    keywords = [word.strip() for word in valid_words]

    return keywords


# Finds keywords in a answer and chooses which words are blanked
def getBlanks(rake, answer):
    valid_words = extractKeywords(rake, answer)

    # Dictionary to store the position keywords by appearence order in the text
    keyword_positions = {keyword: answer.find(keyword) for keyword in valid_words}
    sorted_keywords = sorted(valid_words, key=lambda x: keyword_positions[x])

    # Return a list of blanked words from 
    blanked = multipleBlank(answer, sorted_keywords)
    return sorted_keywords, blanked


# Inserts blanked words along side the corresponding options
def insertBlankChoice(choices, blanked_words):
    # Randomly insert blanked words into the choices
    for i in range(len(blanked_words)):
        blank = blanked_words[i]
        index = random.randint(0, 3)
        choices[i].insert(index, blank)

    #print(f"Choices: {choices}\n")
    return choices


# Returns a tuple with the multiple choice question, total mark and input history template
def createChoiceQuestion(card, keywords, blanked_words, course_name):
    NUMBER_OF_ANSWERS = 1
    NUMBER_OF_CHOICES = 3
    choices, adjusted_blanks, blanks_changed = generateOptions(blanked_words, course_name, keywords, NUMBER_OF_CHOICES)

    # If no options are found for any blanked words, change question type
    if len(adjusted_blanks) == 0:
        change_type = random.randint(1, 2)
        if change_type == 1:
            return createFillQuestion(card, blanked_words)
        else:
            return createRevealQuestion(card)
    
    # If some blanked words were removed
    elif blanks_changed:
        card['blanked'] = adjusted_blanks
    else:
        card['blanked'] = blanked_words

    card['type'] = 'multiple_choice'
    card['options'] = insertBlankChoice(choices, card['blanked'])

    # Template for recording answer for blanked term: -1 for unanswered, 0 for wrong, 1 for correct
    ANSWER_TEMPLATE = [-1] * (NUMBER_OF_CHOICES + NUMBER_OF_ANSWERS)
    QUESTION_TOTAL = len(card.get('blanked'))

    # Template for recording all answers for the question, each blanked term has 4 slots: 1 for correct, 3 for wrong
    history = [ANSWER_TEMPLATE] * QUESTION_TOTAL

    return card, QUESTION_TOTAL, history


# Returns a tuple with the fill in blank question, total mark and input history template
def createFillQuestion(card, blanked_words):   
    adjusted_blanks = []

    # Check if each blanked phrase is a single word (verbs, nouns)
    for word in blanked_words:
        split = word.split()
        if len(split) > 1:
            # Ideally, we would want to choose a word that is a noun or verb
            chosen = random.choice(split)
            adjusted_blanks.append(chosen)
        else:
            adjusted_blanks.append(word)

    card['type'] = 'fill_in_blank'        
    card['blanked'] = adjusted_blanks
    card['options'] = []

    question_total = len(blanked_words)
    history = [-1]*len(blanked_words)
    return card, question_total, history


def createRevealQuestion(card):
    card['type'] = 'reveal'
    card['blanked'] = []
    card['options'] = []

    question_total = 1
    history = [-1]
    return card, question_total, history


# Returns a the quiz as an array when given an array of card objects
def createQuiz(cards, course_name):
    rake = Rake()
    quiz_content = []
    total = 0
    history = [] # Template for recording user answers: -1 for unanswered, 0 for wrong, 1 for correct
    
    for card in cards:
        keywords, blanked_words = getBlanks(rake, card['answer']) # Only blank verbs, nouns or phrases
        # If keywords are found in the answer, generate options
        if keywords:
            #question_words = extractKeywords(rake, card['question'])
            all_keywords = keywords
            #+ question_words           

            # Choose the question type - 0: MCQ, 1: Fill in blank, 2: Reveal
            question_type = 0 #random.choices([0, 1, 2], weights=[0.4, 0.3, 0.3])[0]
            question = []
            match question_type:
                # MCQ
                case 0:
                    question = createChoiceQuestion(card, all_keywords, blanked_words, course_name)
            
                # Fill in blank
                case 1:
                    question = createFillQuestion(card, blanked_words)

                # Reveal
                case 2:
                    question = createRevealQuestion(card)
            
            card = question[0]
            total += question[1]
            history.append(question[2])
    
        else:
            question = createRevealQuestion(card)
            card = question[0]
            total += question[1]
            history.append(question[2])

        quiz_content.append(card)

    quiz = {
        'quiz_content': quiz_content,
        'total': total,
        'history': history,
    }
    return quiz

