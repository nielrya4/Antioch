"""
Themes Showcase Demo
Demonstrates all 6 built-in Antioch themes with interactive theme switcher

Available Themes:
- Diorite: Modern dark theme
- Marble: Clean light theme
- Rhyolite: Earthy eastern Oregon theme
- Quartzite: Alpine Idaho mountain theme
- Jasper: Rich earthy theme with warm colors
- Basalt: Pacific Northwest coastal theme
"""

from antioch import DOM, when
from antioch.elements import Option
from antioch.themes import *


def main():
    """Main demo function."""

    # Start with Diorite theme
    set_theme('diorite')

    # Create state to preserve across theme changes
    state = {
        "count": 0,
        "text_input": "",
        "textarea": "",
        "select": "1"
    }

    def render_page(theme_name):
        """Render the complete page with the selected theme"""
        # Clear the page
        DOM.clear()

        # Set the selected theme
        set_theme(theme_name)

        # Get theme info
        theme_info = get_theme_info()[theme_name]

        # Set body background
        from antioch import js
        js.document.body.style.backgroundColor = COLORS['background']
        js.document.body.style.margin = "0"
        js.document.body.style.padding = "0"

        # Create main container
        container = Container()
        DOM.add(container)

        # Header Section
        container.add(
            H1(theme_info['name']),
            P(theme_info['description'], style={"color": COLORS['text_secondary']})
        )

        # Theme Selector
        selector_card = Card()
        container.add(selector_card)

        selector_card.add(H2("Theme Selector"))

        # Get all available themes
        themes = get_available_themes()

        # Create theme selector dropdown
        from antioch.elements import Select as BaseSelect, Option as BaseOption
        theme_select = BaseSelect(style={
            "background-color": COLORS['surface'],
            "color": COLORS['text'],
            "border": f"1px solid {COLORS['border']}",
            "border-radius": "4px",
            "padding": "8px 12px",
            "font-family": FONTS['family'],
            "font-size": FONTS['size'],
            "cursor": "pointer",
            "min-width": "200px"
        })

        for theme in themes:
            info = get_theme_info()[theme]
            option = BaseOption(info['name'], value=theme)
            if theme == theme_name:
                option.set_attribute("selected", True)
            theme_select.add(option)

        @when(theme_select.events.change)
        def handle_theme_change(sender, event):
            selected_theme = sender.value
            render_page(selected_theme)

        selector_card.add(theme_select)

        container.add(Hr())

        # Typography Section
        typography_card = Card()
        container.add(typography_card)

        typography_card.add(
            H2("Typography"),
            H3("Heading Level 3"),
            H4("Heading Level 4"),
            H5("Heading Level 5"),
            H6("Heading Level 6"),
            P("This is a paragraph with standard text. It uses the theme's default text color and font family."),
            P("You can also use ", Code("inline code"), " like this."),
            Pre("# This is preformatted text\nfor code in blocks:\n    print('Hello, World!')")
        )

        # Interactive Elements Section
        interactive_card = Card()
        container.add(interactive_card)

        interactive_card.add(H2("Interactive Elements"))

        # Counter Example
        counter_display = H3(f"Count: {state['count']}")
        interactive_card.add(counter_display)

        increment_btn = Button("Increment")
        decrement_btn = Button("Decrement")
        reset_btn = Button("Reset")

        @when(increment_btn.events.click)
        def increment(sender, event):
            state['count'] += 1
            counter_display.set_text(f"Count: {state['count']}")

        @when(decrement_btn.events.click)
        def decrement(sender, event):
            state['count'] -= 1
            counter_display.set_text(f"Count: {state['count']}")

        @when(reset_btn.events.click)
        def reset(sender, event):
            state['count'] = 0
            counter_display.set_text(f"Count: {state['count']}")

        button_container = Div(
            increment_btn,
            decrement_btn,
            reset_btn,
            style={"display": "flex", "gap": "8px", "margin": "12px 0"}
        )
        interactive_card.add(button_container)

        # Forms Section
        forms_card = Card()
        container.add(forms_card)

        forms_card.add(H2("Form Elements"))

        # Text input
        text_label = P("Text Input:")
        text_input = Input(type="text", placeholder="Enter some text...")
        if state['text_input']:
            text_input.value = state['text_input']

        @when(text_input.events.input)
        def handle_text_input(sender, event):
            state['text_input'] = sender.value

        forms_card.add(text_label, text_input)

        # Textarea
        textarea_label = P("Textarea:")
        textarea = Textarea(placeholder="Enter multiple lines...")
        textarea.set_attribute("rows", 4)
        if state['textarea']:
            textarea.value = state['textarea']

        @when(textarea.events.input)
        def handle_textarea(sender, event):
            state['textarea'] = sender.value

        forms_card.add(textarea_label, textarea)

        # Select dropdown
        select_label = P("Select:")
        select = Select()

        from antioch.elements import Option as BaseOption
        for i in range(1, 4):
            opt = BaseOption(f"Option {i}", value=str(i))
            if str(i) == state['select']:
                opt.set_attribute("selected", True)
            select.add(opt)

        @when(select.events.change)
        def handle_select(sender, event):
            state['select'] = sender.value

        forms_card.add(select_label, select)

        # Links Section
        links_card = Card()
        container.add(links_card)

        links_card.add(
            H2("Links & Text Formatting"),
            P("Visit ", A("Antioch Documentation", href="#", title="Documentation"), " for more info."),
            P("This is ", Code("inline code"), " and this is a ", A("link", href="#"), "."),
        )

        # Color Palette Section
        colors_card = Card()
        container.add(colors_card)

        colors_card.add(H2("Theme Color Palette"))

        color_grid = Div(style={
            "display": "grid",
            "grid-template-columns": "repeat(auto-fit, minmax(150px, 1fr))",
            "gap": "12px",
            "margin-top": "12px"
        })

        for color_name, color_value in COLORS.items():
            color_box = Div(
                Div(style={
                    "background-color": color_value,
                    "height": "60px",
                    "border-radius": "4px",
                    "border": f"1px solid {COLORS['border']}"
                }),
                P(color_name, style={
                    "margin": "4px 0 0 0",
                    "font-size": "12px",
                    "color": COLORS['text_secondary']
                }),
                Code(color_value, style={"font-size": "11px"}),
                style={"text-align": "center"}
            )
            color_grid.add(color_box)

        colors_card.add(color_grid)

        # Cards Section
        cards_section = Div(style={"margin": "20px 0"})
        container.add(cards_section)

        cards_section.add(H2("Card Layouts"))

        card_grid = Div(style={
            "display": "grid",
            "grid-template-columns": "repeat(auto-fit, minmax(250px, 1fr))",
            "gap": "16px",
            "margin-top": "12px"
        })

        for i in range(1, 4):
            card = Card(
                H3(f"Card {i}"),
                P(f"This is card number {i} demonstrating the Card component."),
                Button(f"Action {i}")
            )
            card_grid.add(card)

        cards_section.add(card_grid)

        # Instructions
        instructions = Card()
        container.add(instructions)

        instructions.add(
            H2("About This Demo"),
            P("This showcase demonstrates all the themed components available in Antioch."),
            P("Use the theme selector at the top to switch between different themes."),
            P("All form inputs and counters preserve their state when switching themes."),
            Hr(),
            H3("Available Themes:"),
        )

        # List all themes with descriptions
        from antioch.elements import Ul as BaseUl, Li as BaseLi
        theme_list = BaseUl(style={
            "color": COLORS['text'],
            "line-height": "1.8"
        })

        for theme in themes:
            info = get_theme_info()[theme]
            item = BaseLi(
                style={"color": COLORS['text']}
            )
            item.add(
                Code(theme, style={"margin-right": "8px"}),
                f" - {info['description']}"
            )
            theme_list.add(item)

        instructions.add(theme_list)

    # Initial render
    render_page('diorite')


if __name__ == "__main__":
    main()
