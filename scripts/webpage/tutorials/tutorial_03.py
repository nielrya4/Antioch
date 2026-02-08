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
