from js import document
from pyodide.ffi import create_proxy
from query import query
import numpy as np

def runPython(*args, **kwargs):
    query_text = document.getElementById("query").value
    results = query(query_text)
    document.getElementById("results").innerHTML = ""
    for course, score in results:
        document.getElementById("results").innerHTML += f"<p>{course} ({score})</p>"

# function_proxy = create_proxy(runPython)

# document.getElementById("button").addEventListener("click", function_proxy)








