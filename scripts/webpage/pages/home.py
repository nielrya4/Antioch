from antioch import *

page = Div(style={
    "font-family": "ubuntu",
}).add(
    H3("Antioch: A Python-Based Frontend Development Ecosystem"),
    P(
        "Antioch provides the framework of tools necessary to build web apps entirely in Python. It allows developers",
        "to use the intuitive nature of Python (via Pyodide and WebAssembly, the Document Object Model (DOM) standard",
        "elements, and the genius of existing Python and JavaScript libraries/APIs together in one place."
    ),
    P(
        "Many Python-in-the-browser solutions require significant effort to implement in any kind of usable way.",
        "Antioch is different. Declaration of elements, creating and using interactive macros, styling, and ",
        "manipulation of the DOM come naturally and can all happen in the same file."
    )
)