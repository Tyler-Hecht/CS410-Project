import pickle
from tqdm import tqdm
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('words')
from nltk.corpus import stopwords, words
import random
import pandas as pd

# Limits to tokenization and lemmitization, respectively
MAX_TOKENIZER_LEN = 5000000
MAX_WORDS = 500000

# Weights for title and description
TITLE_WEIGHT = 10
DESCRIPTION_WEIGHT = 10

# organizes the text into one large dataframe with words as columns and courses as rows
# the values represent the number of times the word appears in the course

with open("../courses_dict.pkl", "rb") as f:
    courses_dict = pickle.load(f)


# # combine each term's text into one string and add the course title and description
all_words_dict = {}
for course in tqdm(courses_dict, position=0, leave=True):
    all_words_dict[course] = ""
    for term in tqdm(courses_dict[course]["text"], position=1, leave=False):
        all_words_dict[course] += term + " "
    all_words_dict[course] += courses_dict[course]["title"] + " "
    all_words_dict[course] += courses_dict[course]["description"] + " "

# tokenize and lemmatize the words, and remove stopwords
lemmatizer = nltk.stem.WordNetLemmatizer()
lemmatized_dict = {}
for course in tqdm(all_words_dict, position=0, leave=True):
    words = all_words_dict[course]
    if len(words) > MAX_TOKENIZER_LEN:
        words = words[:MAX_TOKENIZER_LEN]
    # go to last space before MAX_TOKENIZER_LEN
    while words[-1] != " ":
        words = words[:-1]
    words = words[:MAX_TOKENIZER_LEN]
    words = nltk.word_tokenize(words)
    if len(words) > MAX_WORDS:
        words = random.sample(words, MAX_WORDS)
    lemmatized_words = []
    for word in tqdm(words, position=1, leave=False):
        if word not in stopwords.words('english'):
            lemmatized_words.append(lemmatizer.lemmatize(word))
    lemmatized_dict[course] = lemmatized_words

# find unique words
unique_words = set()
for course in tqdm(lemmatized_dict):
    valid_words = words.words()
    course_words = lemmatized_dict[course]
    intersection = set(valid_words).intersection(course_words)
    unique_words = unique_words.union(intersection)
    # add in words from title and description
    title = courses_dict[course]["title"]
    description = courses_dict[course]["description"]
    title_words = nltk.word_tokenize(title)
    description_words = nltk.word_tokenize(description)
    lemmatized_title_words = []
    lemmatized_description_words = []
    for word in tqdm(title_words, position=1, leave=False):
        if word not in stopwords.words('english'):
            lemmatized_title_words.append(lemmatizer.lemmatize(word))
    for word in tqdm(description_words, position=1, leave=False):
        if word not in stopwords.words('english'):
            lemmatized_description_words.append(lemmatizer.lemmatize(word))
    title_words = lemmatized_title_words
    description_words = lemmatized_description_words
    intersection = set(valid_words).intersection(title_words)
    unique_words = unique_words.union(intersection)
    intersection = set(valid_words).intersection(description_words)
    unique_words = unique_words.union(intersection)

# create a dataframe with each course as a row and each word as a column
courses_df = pd.DataFrame(columns=list(unique_words), dtype=int)
# fill it all with 0
for course in tqdm(lemmatized_dict, position=0, leave=True):
    courses_df.loc[course] = 0
for course in tqdm(lemmatized_dict, position=0, leave=True):
    course_dict = {}
    title = courses_dict[course]["title"]
    description = courses_dict[course]["description"]
    title_words = nltk.word_tokenize(title)
    description_words = nltk.word_tokenize(description)
    lemmatized_title_words = []
    lemmatized_description_words = []
    for word in tqdm(title_words, position=1, leave=False):
        if word not in stopwords.words('english'):
            lemmatized_title_words.append(lemmatizer.lemmatize(word))
    for word in tqdm(description_words, position=1, leave=False):
        if word not in stopwords.words('english'):
            lemmatized_description_words.append(lemmatizer.lemmatize(word))
    title_words = lemmatized_title_words
    description_words = lemmatized_description_words
    
    for word in tqdm(list(unique_words), position=1, leave=False):
        course_dict[word] = 0
    for word in tqdm(title_words, position=1, leave=False):
        course_dict[word] = 0
    for word in tqdm(description_words, position=1, leave=False):
        course_dict[word] = 0

    for word in tqdm(lemmatized_dict[course], position=1, leave=False):
        if word in unique_words:
            course_dict[word] += 1
    # add in words from title and description
    for word in tqdm(title_words, position=1, leave=False):
        course_dict[word] += TITLE_WEIGHT
    for word in tqdm(description_words, position=1, leave=False):
        course_dict[word] += DESCRIPTION_WEIGHT
    courses_df.loc[course] = course_dict
    
with open("../courses_df.pkl", "wb") as f:
    pickle.dump(courses_df, f)

