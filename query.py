import pickle
# get lemmatization and tokenization from sklearn
from sklearn.feature_extraction.text import CountVectorizer
from textblob import TextBlob, Word

# read scraping/courses_dict.pkl
with open("courses_df.pkl", "rb") as f:
    courses_df = pickle.load(f)

SYNONYM_WEIGHT = 0

def BM25(term, course, k1, b):
    # calculates BM25 score for term in course

    # check if term is in course
    if term not in courses_df.columns:
        return 0
    
    # calculate score
    score = courses_df.loc[course, term] * (k1 + 1) / (courses_df.loc[course, term] + k1 * (1 - b + b * courses_df.loc[course, "length"] / courses_df["length"].mean()))

    return score

def query(query_text, k1=1.2, b=0.75):
    # returns top 5 courses that match the query
    query_text = query_text.lower()

    # tokenize query
    query_blob = TextBlob(query_text)
    query_tokens = query_blob.words

    # lemmatize query
    query_lemmas = [Word(token).lemmatize() for token in query_tokens]

    # calculate BM25 scores for each course
    scores = {}
    for course in courses_df.index:
        scores[course] = 0
        for term in query_lemmas:
            scores[course] += BM25(term, course, k1, b)

    # increase the score based on synonyms
    synonym_scores = {}
    for course in courses_df.index:
        synonym_scores[course] = 0
        for term in query_lemmas:
            for synset in Word(term).synsets:
                for synonym in synset.lemmas():
                    if synonym.name() in courses_df.columns:
                        synonym_scores[course] += BM25(synonym.name(), course, k1, b)

    # weigh score based on synonyms
    for term in synonym_scores:
        scores[course] = scores[course] * (1 - SYNONYM_WEIGHT) + synonym_scores[term] * SYNONYM_WEIGHT

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


print(query("text retrieval"))
