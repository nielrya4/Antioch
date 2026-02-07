from antioch import *
from antioch.macros import Accordion, AccordionPanel
from scripts.examples import pong_game

page = Div(
    H3("This is an interactive toolbar"),
    Accordion(
        [
            AccordionPanel("01. Hello World", Pre(
                """
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
    """
            )),
            AccordionPanel("02. Chaining Elements", Pre(
                """
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
"""
            )),
            AccordionPanel("03. Events", Pre(
                """
from antioch import *

def main():

    DOM.add(
        H2("(03) Events Tutorial")
    )

    # Set up a place to render messages from the buttons
    status = P("Messages will appear here:")

    # Method 1: Defining an event handler function and referencing it
    def display_message(event):
        status.add(P("You clicked Button 1!"))

    button_1 = Button("Button 1",
        events={'click': display_message}
    )


    # Method 2: Using lambda functions
    button_2 = Button("Button 2",
        events={
            'click': lambda event: status.add(
                P("You clicked Button 2!")
            )
        }
    )


    # Add all the elements to the DOM
    DOM.add(
        button_1,
        Br(),
        button_2,
        status
    )

"""
            ))
        ],
        container_style={"width": "100%"},
    )
)
