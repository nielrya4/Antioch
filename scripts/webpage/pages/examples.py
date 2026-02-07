from antioch import *
from antioch.macros import Accordion, AccordionPanel
from scripts.examples import pong_game

page = Div(
    H3("This is an interactive toolbar"),
    Accordion(
        [
            AccordionPanel("Canvas-Based Pong Game", "pong_content"),
            AccordionPanel("Chart.js Integration", "chartjs_content"),
            AccordionPanel("Callbacks and Interactivity", "callback_content")
        ],
        container_style={"width": "100%"},
    )
)
