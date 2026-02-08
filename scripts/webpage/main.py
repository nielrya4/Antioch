from antioch import *
from antioch.macros import Toolbar
from scripts.webpage.pages import home, examples, downloads, tutorials

content_div = Div()

def main():
    add_toolbar()
    DOM.add(content_div)
    set_content(home.page)

def add_toolbar():
    menu_structure = {
        "Home": lambda: set_content(home.page),
        "Examples": lambda: set_content(examples.page),
        "Tutorials": lambda: set_content(tutorials.page),
        "Downloads": lambda: set_content(downloads.page),
        "Test": {
            "test_1": lambda: set_content(home.page),
            "test_2": {
                "test_3": lambda: set_content(tutorials.page),
            },
        }

    }
    toolbar = Toolbar(
        menu_structure=menu_structure,
        toolbar_style={
            "background_color": "#1e272e",
            "box_shadow": "0 2px 6px rgba(0,0,0,0.2)"

        }
    )
    DOM.add(toolbar)

def set_content(content: Element):
    content_div._dom_element.innerHTML = ""
    content_div.add(content)

if __name__ == "__main__":
    main()
