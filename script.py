from js import document
from pyodide.ffi import create_proxy
from query import query

def runPython(*args, **kwargs):
    query_text = document.getElementById("query").value
    results = query(query_text)
    document.getElementById("results").innerHTML = ""
    output = ""
    for course, score in results:
        url = f"https://cs.illinois.edu/academics/courses/{course.split()[0]}{course.split()[1]}"
        # course and score only (no url)
        output += f"{course} ({score})<br>"
        # url in smaller font
        output += f"<a href=\"{url}\" style=\"font-size: 0.8em;\">{url}</a><br>"
    if output:
        document.getElementById("results").innerHTML = output
    else:
        document.getElementById("results").innerHTML = "<p>No results found.</p>"


# function_proxy = create_proxy(runPython)

# document.getElementById("button").addEventListener("click", function_proxy)








