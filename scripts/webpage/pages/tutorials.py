from antioch import *
from antioch.macros import Accordion, AccordionPanel, CodeBlock
from scripts.examples import pong_game
from pyodide.http import pyfetch as fetch
import asyncio

# Load tutorial code from files using fetch API
async def load_tutorial(filename):
    """Load tutorial code from file using fetch."""
    response = await fetch(f'scripts/webpage/tutorials/{filename}')
    return await response.string()

# Load tutorials synchronously at module level
def load_all_tutorials():
    """Load all tutorial files."""
    loop = asyncio.get_event_loop()
    return {
        '01': loop.run_until_complete(load_tutorial('tutorial_01.py')),
        '02': loop.run_until_complete(load_tutorial('tutorial_02.py')),
        '03': loop.run_until_complete(load_tutorial('tutorial_03.py')),
    }

tutorials = load_all_tutorials()
TUTORIAL_01 = tutorials['01']
TUTORIAL_02 = tutorials['02']
TUTORIAL_03 = tutorials['03']

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
