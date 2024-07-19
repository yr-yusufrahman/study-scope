'''
content = {
     questions: [q1, q2, q3],  --> the questions from flashcards of this topic
     answers: [a1, a2, a3],  --> corresponding answers
     blanked: [[b1], [], [b1, b2, b3]],  --> the chosen keywords that should be blanked from each answer
     options: [
        [[o1, o2, o3, answer]], 
        [[]], 
        [[o1, o2, o3, answer], [o1, o2, o3, answer], [o1, o2, o3, answer]]
        ], --> options for each keyword
}
'''
# Numpy could improve efficiency?


# Needed to download punkt and stopwords from nltk
from rake_nltk import Rake
import random


# Blank words by examining a unique set of all keywords
def multipleBlank(answer, ranked):
    position = []
    length = 0 # the length of blanked list
    keywords_length = len(ranked)

    if keywords_length != 0:
        limit = 0
        word_count = len(answer.split())
        if word_count < 16:
            limit = 1
        elif word_count < 24:
            limit = 2
        elif word_count < 34:
            limit = 3
        elif word_count < 42:
            limit = 4
        else:
            limit = 5

        # Adds the right number of blanked words to the list, if limit is higher than words is considered
        if keywords_length < limit:
            while length != keywords_length:
                index = random.randint(0, len(ranked)-1)
                if index not in position:
                    position.append(index)
                    length += 1   
        else:
            while length != limit:
                index = random.randint(0, len(ranked)-1)
                if index not in position:
                    position.append(index)
                    length += 1               
    
    position = sorted(position)
    blanked = [ranked[x] for x in position]
    return blanked


# Returns a list of blanked keywords after extracting all keywords
def keywords(answers):
    rake = Rake(max_length=2, include_repeated_phrases=False)
    extracted = []
    for answer in answers:
        rake.extract_keywords_from_text(answer)
        
        # Stores a list of keywords
        extracted_words = list(set(rake.get_ranked_phrases()))

        # Check if all keywords are valid english words
        valid_words = [word for word in extracted_words if any(c.isalpha() for c in word)]

        # Create a dictionary to store the position of each keyword in the text
        keyword_positions = {keyword: answer.find(keyword) for keyword in valid_words}

        # Sort the list of keywords based on their positions in the text
        sorted_keywords = sorted(valid_words, key=lambda x: keyword_positions[x])

        # Return a list of blanked words from 
        blanked = multipleBlank(answer, sorted_keywords)
        extracted.append(blanked)
    return extracted


# Instead of storing the actual words, store the index of the words



# Print answers with blanked answers
def printAnswers():
    # For a given topic or chapter
    content = {
        'questions': ['What is differentiation?', 'What is integration?', 'Probs empty?'],
        'answers': ['The gradient function. gradient function.', 
                    'The process of finding the area underneath a curve. It is really useful in mechanics to anaylze scenarios for the area underneath.',
                    'It is the...'
                    ]
    }
    content["extracted"] = keywords(content["answers"])
    for i in range(len(content["questions"])):
        raw = content['answers'][i]
        blanked = raw
        words = content['extracted'][i]

        if len(words) != 0:
            # Blank the words from the raw answer
            for word in words:
                blanked = blanked.replace(word, "_______", 1)
                
        else:
            blanked = "NO BLANKS"

        mistakes = 0
        print(f"Question 1: {content['questions'][i]}")
        print(blanked)
        for option in content['extracted'][i]:        
            print(f"Option (1): Distractor, Option (2): {option}")
            user = int(input("Choose... "))
            if user == 2:
                print("Correct!")
                blanked = blanked.replace("_______", option, 1)
                print(f"{blanked}\n")
            else:
                print("Wrong\n")
                mistakes += 1
        
        print()

# Edit the program by hard-coding your own options to check if the program displays the right options for the...
# right blanked words for each question 
