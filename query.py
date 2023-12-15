import pickle

# read scraping/courses_dict.pkl
with open("courses_dict.pkl", "rb") as f:
    courses_dict = pickle.load(f)

# given a query, return a list of courses that match the query

def listify(query):
    # remove punctuation and split query into words
    if type(query) != str:
        query = str(query)
    query = query.lower()
    for i in range(len(query)):
        # filter by alphanumeric characters or "-"
        if not query[i].isalnum() and query[i] != "-":
            query = query[:i] + " " + query[i+1:]
    query = query.split()
    return query

def query(query):
    TITLE_WEIGHT = 5
    DESC_WEIGHT = 2

    query = listify(query)

    # listify all the course titles and descriptions
    for course in courses_dict:
        courses_dict[course]["title"] = listify(courses_dict[course]["title"])
        courses_dict[course]["description"] = listify(courses_dict[course]["description"])

    # assign a score to each course
    scores = {}
    for course in courses_dict:
        scores[course] = 0
        for word in query:
            if word in courses_dict[course]["title"]:
                scores[course] += TITLE_WEIGHT
        for word in query:
            if word in courses_dict[course]["description"]:
                scores[course] += DESC_WEIGHT

    # sort the courses by score
    sorted_courses = sorted(scores, key=scores.get, reverse=True)

    # return the top 5 courses and their scores (if they have a score > 0)
    return [(course, scores[course]) for course in sorted_courses if scores[course] > 0][:5]

