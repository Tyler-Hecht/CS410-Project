from js import document
from pyodide.ffi import create_proxy

def runPython(optional_arg=None):
    # set the text of the button to "you clicked me"
    document.getElementById("button").innerHTML = "you clicked me"

function_proxy = create_proxy(runPython)

document.getElementById("button").addEventListener("click", function_proxy)
