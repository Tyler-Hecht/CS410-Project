import requests
from bs4 import BeautifulSoup

catalog_url = "http://catalog.illinois.edu/courses-of-instruction/cs/"

# Get the HTML of the page
page = requests.get(catalog_url)
# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(page.content, 'html.parser')

# get div with class = courseblock
course_blocks = soup.find_all("div", class_="courseblock")

course_dict = {}

# get the course name and description
for block in course_blocks:
    course_head = block.find("p", class_="courseblocktitle").text
    # extract course name and title
    course_name = course_head.split()[0] + " " + course_head.split()[1]
    course_title = " ".join(course_head.split()[2:]).split("credit")[0]

    course_desc = block.find("p", class_="courseblockdesc").text
    if course_desc.startswith("\nSame as") and "See" in course_desc:
        crosslist = course_desc.split("See ")[-1].split(".")[0]
        crosslist_url = "http://catalog.illinois.edu/search/?P=" + crosslist
        # crosslist_url = crosslist_url.replace(" ", "%20")
        crosslist_page = requests.get(crosslist_url)
        crosslist_soup = BeautifulSoup(crosslist_page.content, 'html.parser')
        course_desc = crosslist_soup.find("p", class_="courseblockdesc").text

    # print(course_name + ": " + course_title)
    # print(course_desc)
    # print()

    course_dict[course_name] = {"title": course_title, "description": course_desc, "text": []}

# pickle the dictionary
import pickle
with open("scraping/courses_dict.pkl", "wb") as f:
    pickle.dump(course_dict, f)
