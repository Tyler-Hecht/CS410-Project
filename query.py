import pickle
import pandas as pd

K1_DEFAULT = 1.2
B_DEFAULT = 0.75

with open("stopwords.txt", "r") as f:
    stopwords = f.read().splitlines()

# read scraping/courses_dict.pkl
with open("courses_df.pkl", "rb") as f:
    courses_df = pickle.load(f)

def lemmatize(word):
    return word

def tokenize(text):
    # tokenize text, removing punctuation
    text = text.lower()
    punctuation = "!\"#$%&'()*+,./:;<=>?@[\\]^_`{|}~"
    for char in punctuation:
        text = text.replace(char, " ")
    return text.split()

def BM25(term, course, k1=K1_DEFAULT, b=B_DEFAULT):
    # calculates BM25 score for term in course

    # check if term is in course
    if term not in courses_df.columns:
        return 0
    
    # calculate score
    score = courses_df.loc[course, term] * (k1 + 1) / (courses_df.loc[course, term] + k1 * (1 - b + b * courses_df.loc[course, "length"] / courses_df["length"].mean()))

    return score

def query(query_text, k1=K1_DEFAULT, b=B_DEFAULT, data = courses_df, tokenize=tokenize, lemmatize=lemmatize):
    # returns top 5 courses that match the query
    query_text = query_text.lower()

    # tokenize and lemmatize query
    query_lemmas = []
    for word in tokenize(query_text):
        query_lemmas.append(lemmatize(word))

    print(query_lemmas)

    # calculate BM25 scores for each course
    scores = {}
    for course in courses_df.index:
        scores[course] = 0
        for term in query_lemmas:
            scores[course] += BM25(term, course, k1, b)

    # sort courses by score
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # return top 5 courses with scores above 0
    top_courses = []
    for course in sorted_scores:
        if course[1] > 0:
            top_courses.append(course[0])
        if len(top_courses) == 5:
            break

    return top_courses

if __name__ == "__main__":
    import nltk
    nltk.download("wordnet")
    from nltk.stem import WordNetLemmatizer
    from nltk.corpus import wordnet
    # ask for input
    with open("courses_df_lemmatized.pkl", "rb") as f:
        courses_df_lemmatized = pickle.load(f)
    lemmatizer = WordNetLemmatizer()
    while True:
        query_text = input("Enter query: ")
        results = query(query_text, lemmatize=lemmatizer.lemmatize, data=courses_df_lemmatized, tokenize=nltk.word_tokenize)
        print(results)
