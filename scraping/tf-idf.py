import nltk
import pickle
import pandas as pd
from tqdm import tqdm
import math

# calculates the tf-idf for each term in each course

with open("../courses_df.pkl", "rb") as f:
    courses_df = pickle.load(f)
    
tf_idf_df = pd.DataFrame(columns=courses_df.columns)
for word in tqdm(courses_df.columns, position=0, leave=True):
    for course in tqdm(courses_df.index, position=1, leave=False):
        # smoothed tf-idf
        tf_idf_df.loc[course, word] = (1 + math.log(courses_df.loc[course, word])) * math.log(len(courses_df) / (1 + courses_df[word].astype(bool).sum()))

with open("../tf_idf_df.pkl", "wb") as f:
    pickle.dump(tf_idf_df, f)

# save as csv
tf_idf_df.to_csv("../tf_idf_df.csv")
