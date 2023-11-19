from js import document
from pyodide.ffi import create_proxy

def runPython(optional_arg=None):
    document.getElementById("button").innerHTML = "Python is running"

function_proxy = create_proxy(runPython)

document.getElementById("button").addEventListener("click", function_proxy)







