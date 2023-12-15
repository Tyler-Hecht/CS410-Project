from query import query
import pickle
import nltk
from nltk.corpus import words

with open("courses_df.pkl", "rb") as f:
    courses_df = pickle.load(f)

print(query("computer vision"))
