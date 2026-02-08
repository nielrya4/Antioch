from antioch import *

# The DOM, or Document Object Model, is a Python object that represents the entire webpage. It is an interesting place
# with pre-defined elements that make up webpages. Creating webpages involves nesting these elements together in
# different configurations to convey content and meaning to the user.
#
# The elements used in this tutorial are:
# - Div: A block-level container element.
# - P: A paragraph element.
# - A: An anchor element.
# - Br: A line break element.
# - Button: A button element.
#
# If you are familiar with HTML, JavaScript, and CSS, you will have an advantage in learning the Antioch framework.

def main():

    DOM.add(
        H2("(02) Chaining Elements Tutorial")
    )

    # Method 1: Chaining elements with commas
    DOM.add(
        Div(
            P(
                "Hello World!",
                A("This link goes to Bing.", href="https://bing.com"),
                Br(),
                A("This link goes to Google.", href="https://google.com"),
                Button("This button does nothing.")
            )
        )
    )

    # Method 2: Using the add() method on an existing element
    our_div = Div()
    our_div.add(P("This is a paragraph inside a Div element."))
    DOM.add(our_div)
