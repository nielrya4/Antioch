from antioch import *
from antioch.macros import Accordion, AccordionPanel, CodeBlock
from scripts.examples import pong_game
import js

# Load tutorial code from files synchronously using XMLHttpRequest
def load_tutorial(filename):
    """Load tutorial code from file using synchronous XMLHttpRequest."""
    url = f'scripts/webpage/tutorials/{filename}'
    try:
        xhr = js.XMLHttpRequest.new()
        xhr.open('GET', url, False)  # False = synchronous
        xhr.send(None)

        if xhr.status == 200:
            return xhr.responseText
        else:
            print(f"Error loading {filename}: HTTP {xhr.status}")
            return f"# Tutorial not found: {filename}\n# HTTP Status: {xhr.status}"
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return f"# Tutorial not found: {filename}\n# Error: {str(e)}"

# Load all tutorials synchronously at module level
def load_all_tutorials():
    """Load all tutorial files."""
    tutorials = {}

    # Try to load tutorials by number
    for i in range(1, 10):  # Support up to 9 tutorials for now
        key = f'{i:02d}'
        filename = f'tutorial_{key}.py'
        content = load_tutorial(filename)

        # Only add if it doesn't contain error message
        if not content.startswith('# Tutorial not found'):
            tutorials[key] = content
        else:
            # Stop when we hit the first missing tutorial
            break

    return tutorials

tutorials = load_all_tutorials()
TUTORIAL_01 = tutorials.get('01', '# Tutorial 01 not found')
TUTORIAL_02 = tutorials.get('02', '# Tutorial 02 not found')
TUTORIAL_03 = tutorials.get('03', '# Tutorial 03 not found')

page = Div(
    H3("This is an interactive toolbar"),
    Accordion(
        [
            AccordionPanel("01. Hello World", CodeBlock(
                content=TUTORIAL_01,
                language="python",
                editable=False,
                line_numbers=True,
                height="300px",
                lazy_init=True
            )),
            AccordionPanel("02. Chaining Elements", CodeBlock(
                content=TUTORIAL_02,
                language="python",
                editable=False,
                line_numbers=True,
                height="450px",
                lazy_init=True
            )),
            AccordionPanel("03. Events", CodeBlock(
                content=TUTORIAL_03,
                language="python",
                editable=False,
                line_numbers=True,
                height="400px",
                lazy_init=True
            ))
        ],
        container_style={"width": "100%"},
    )
)
