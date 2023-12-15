import requests
from bs4 import BeautifulSoup
import pickle
from tqdm import tqdm
import random

# scrapes the text from each course page for each term offered

# constants that influence how long this takes to run
MAX_TERMS = 20
MAX_LINKS = 20
TIMEOUT = 10

# scrape each course page in courses_dict
with open("../courses_dict.pkl", "rb") as f:
    courses_dict = pickle.load(f)

def termify(term):
    # convert term to format used in url
    term = term.lower()
    term = term.replace(" ", "")
    term = term.replace("spring", "sp")    
    term = term.replace("summer", "su")
    term = term.replace("fall", "fa")
    term = term.replace("winter", "wi")
    return term


# scrape text from each course page for each term offered
for course in tqdm(courses_dict, position=0, leave=True):
    terms = courses_dict[course]["terms"]

    courses_dict[course]["text"] = []

    # if more than 20 terms, randomly sample 20
    if len(terms) > 20:
        terms = random.sample(terms, MAX_TERMS)

    for term in tqdm(terms, position=1, leave=False):
        url = f"https://courses.grainger.illinois.edu/{course.replace(' ', '')}/{termify(term)}"
        
        # try to get the page
        try:
            page = requests.get(url, timeout = TIMEOUT)
        except:
            continue
        soup = BeautifulSoup(page.content, 'html.parser', from_encoding="iso-8859-1")
        # get all text on the page
        text = soup.get_text()
        # add to courses_dict
        courses_dict[course]["text"].append(text)

        # find other links on the page
        links = soup.find_all("a")

        # if more than 50 links, randomly sample 50
        if len(links) > 20:
            links = random.sample(links, MAX_LINKS)

        # explore links on the page
        for link in tqdm(links, position=2, leave=False):
            # get the link
            link = link.get("href")
            # try to get the page
            try:
                page = requests.get(link, timeout = TIMEOUT)
                soup = BeautifulSoup(page.content, 'html.parser', from_encoding="iso-8859-1")
            except:
                continue
            # get all text on the page
            text = soup.get_text()
            # add to courses_dict
            courses_dict[course]["text"].append(text)

    # pickle the dictionary
    with open(f"../courses_dict.pkl", "wb") as f:
        pickle.dump(courses_dict, f)

# print(courses_dict)
