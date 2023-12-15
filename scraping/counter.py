import pickle
from tqdm import tqdm
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('words')
import nltk.corpus
import random
import pandas as pd
import textblob as TextBlob


# Limits to tokenization and lemmitization, respectively
MAX_TOKENIZER_LEN = 100000000
MAX_WORDS = 20000000

# Weights for title and description
TITLE_WEIGHT = 20
DESCRIPTION_WEIGHT = 20

# organizes the text into one large dataframe with words as columns and courses as rows
# the values represent the number of times the word appears in the course

with open("../courses_dict.pkl", "rb") as f:
    courses_dict = pickle.load(f)

def lemmatize(word):
    # lemmatizes word with TextBlob
    return TextBlob.Word(word).lemmatize()

stopwords = set(nltk.corpus.stopwords.words('english'))

# combine each term's text into one string and add the course title and description
all_words_dict = {}
for course in tqdm(courses_dict, position=0, leave=True):
    all_words_dict[course] = " ".join(courses_dict[course]["text"])

print("done combining text")

# tokenize and lemmatize the words, and remove stopwords
lemmatized_dict = {}
for course in tqdm(all_words_dict, position=0, leave=True):
    words = all_words_dict[course][:MAX_TOKENIZER_LEN]
    if " " not in words: # if there is no space, then don't use text data
        lemmatized_dict[course] = []
        continue
    # go to the last space
    last_space = words.rfind(" ")
    words = words[:last_space]
    words = nltk.word_tokenize(words)
    if len(words) > MAX_WORDS:
        words = random.sample(words, MAX_WORDS)
    lemmatized_words = []
    for word in tqdm(words, position=1, leave=False):
        if word not in stopwords:
            lemmatized_words.append(lemmatize(word))
    lemmatized_dict[course] = lemmatized_words

print("done tokenizing and lemmatizing")

# find unique words
unique_words = set()
for course in tqdm(lemmatized_dict):
    # get valid words from nltk
    valid_words = nltk.corpus.words.words()
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
        if word not in stopwords:
            lemmatized_title_words.append(lemmatize(word))
    for word in tqdm(description_words, position=1, leave=False):
        if word not in stopwords:
            lemmatized_description_words.append(lemmatize(word))
    title_words = lemmatized_title_words
    description_words = lemmatized_description_words
    intersection = set(valid_words).intersection(title_words)
    unique_words = unique_words.union(intersection)
    intersection = set(valid_words).intersection(description_words)
    unique_words = unique_words.union(intersection)

print("done finding unique words")

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
        if word not in stopwords:
            lemmatized_title_words.append(lemmatize(word))
    for word in tqdm(description_words, position=1, leave=False):
        if word not in stopwords:
            lemmatized_description_words.append(lemmatize(word))
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

print(f"done creating dataframe, shape: {courses_df.shape}")

# # convert words to TextBlob lemmas
# new_columns = []
# for word in tqdm(courses_df.columns, position=0, leave=True):
#     new_columns.append(TextBlob.Word(word).lemmatize())
# courses_df.columns = new_columns

# # remove duplicate columns
# courses_df = courses_df.groupby(courses_df.columns, axis=1).sum()

# save courses_df
with open("../courses_df2.pkl", "wb") as f:
    pickle.dump(courses_df, f)
