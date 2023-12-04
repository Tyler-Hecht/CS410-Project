import requests
from bs4 import BeautifulSoup
import pickle

# scrape each course page in courses_dict
with open("courses_dict.pkl", "rb") as f:
    courses_dict = pickle.load(f)

# for course in courses_dict:
#     course = course.replace(" ", "")
#     url = "https://courses.grainger.illinois.edu/" + course + "/"
#     page = requests.get(url)
#     soup = BeautifulSoup(page.content, 'html.parser')
#     print(url)

print(courses_dict)
