from js import document, fetch
from pyodide.ffi import create_proxy
import pickle
from query import query

def runPython(*args, **kwargs):
    query_text = document.getElementById("query").value
    results = query(query_text)
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








