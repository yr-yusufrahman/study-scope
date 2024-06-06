from predictor.helpers.blankWords import multipleBlank
from predictor.helpers.createOptions import generateOptions
from rake_nltk import Rake

# Have a global content dictionary

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


# Returns a the quiz as an array
def createQuiz(cards):
    rake = Rake()
    quiz_content = []
    
    for card in cards:
        quiz_obj = {
            'multiple_choice': True,
            'blanked': [],
            'options': []
        }
        keywords, blanked_words = getBlanks(rake, card['answer'])
        
        # If keywords are found in the answer, generate options
        if keywords:
            question_words = extractKeywords(rake, card['question'])
            all_keywords = question_words + keywords           

            choices = generateOptions(all_keywords, blanked_words)

            if len(choices) == 0:
                card['multiple_choice'] = False
            else:
                card['multiple_choice'] = True
                card['blanked'] = blanked_words
                card['options'] = choices
        else:
            card['multiple_choice'] = False

        quiz_content.append(card)

    return quiz_content


