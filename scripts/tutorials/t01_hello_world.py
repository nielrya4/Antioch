from antioch import *

def main():
    DOM.add(
        H2("(01) Hello World Tutorial")
    )

    content = Div(
        H1("Hello World!"),
        P("This is a webpage made entirely in Python.")
    )
    DOM.add(content)