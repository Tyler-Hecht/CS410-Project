document.getElementById("clearScript").onclick = () => {
  document.getElementById("py-repl").remove();
  const pyRepl = document.createElement("py-repl");
  pyRepl.id = "py-repl";
  document.getElementById("py-repl-parent").appendChild(pyRepl);
}

document.getElementById("clearOutput").onclick = () => {
  document.getElementById("py-terminal").remove();
  const pyTerminal = document.createElement("py-terminal");
  pyTerminal.id = "py-terminal";
  document.getElementById("py-terminal-parent").appendChild(pyTerminal);
}