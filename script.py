from js import document, fetch
from pyodide.ffi import create_proxy
import pickle
from query import query

def runPython(*args, **kwargs):
    query_text = document.getElementById("query").value
    k1 = document.getElementById("k1").value
    b = document.getElementById("b").value
    # check that k1 and b are valid
    try:
        k1 = float(k1)
    except:
        k1 = 1.2
    try:
        b = float(b)
    except:
        b = 0.75
    # excluded courses
    excluded_courses = document.getElementById(f"exclude").value
    excluded_courses = excluded_courses.split(",")
    excluded_courses = [course.strip().upper() for course in excluded_courses]
    # query
    results = query(query_text, excluded_courses, k1, b)
    document.getElementById("results").innerHTML = ""
    output = ""
    for course in results:
        url = f"https://cs.illinois.edu/academics/courses/{course.split()[0]}{course.split()[1]}"
        output += f"{course}<br>"
        # url in smaller font
        output += f"<a href=\"{url}\" style=\"font-size: 0.8em;\">{url}</a><br>"
    if output:
        document.getElementById("results").innerHTML = output
    else:
        document.getElementById("results").innerHTML = "<p>No results found.</p>"


# function_proxy = create_proxy(runPython)

# document.getElementById("button").addEventListener("click", function_proxy)








