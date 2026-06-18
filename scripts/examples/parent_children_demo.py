"""
Element Parent/Children Demo

Click on any element to see its parent displayed in a modal.
Demonstrates Element.parent and Element.children through interactive nested structure.
"""
from antioch import *
from antioch.macros import Modal


def main():
    DOM.add(
        H1("Element Parent/Children Demo"),
        P("Click on any colored box to see its parent in a modal")
    )

    # Create modal for displaying parent info
    info_modal = Modal(title="Element Parent Info")
    DOM.add(info_modal.element)

    # Helper function to show parent info
    def show_parent_info(element, element_name):
        info_modal.clear_content()

        if element.parent is None:
            info_modal.set_content(
                Div(
                    H3(f"Element: {element_name}"),
                    P(Strong("Parent: "), "None (This is a root element)"),
                    P(Strong("Tag: "), Code(element._tag_name)),
                    style={"padding": "10px"}
                )
            )
        else:
            parent = element.parent
            parent_name = parent.get_attribute("data-name") or "Unknown"

            # Build ancestor chain
            ancestors = []
            current = element
            while current is not None:
                name = current.get_attribute("data-name") or current._tag_name
                ancestors.append(name)
                current = current.parent

            info_modal.set_content(
                Div(
                    H3(f"Element: {element_name}"),
                    P(Strong("Parent: "), parent_name),
                    P(Strong("Parent Tag: "), Code(parent._tag_name)),
                    P(Strong("Parent's Children Count: "), str(len(parent.children))),
                    Hr(),
                    P(Strong("Ancestor Chain:")),
                    P(" → ".join(ancestors), style={
                        "padding": "10px",
                        "background-color": "#f8f9fa",
                        "border-radius": "4px",
                        "font-family": "monospace"
                    }),
                    style={"padding": "10px"}
                )
            )

        info_modal.open()

    # ========== Create Nested Structure ==========

    # Level 1: Container
    container = Div(style={
        "padding": "20px",
        "background-color": "#e3f2fd",
        "border": "3px solid #2196f3",
        "border-radius": "8px",
        "margin": "20px 0",
        "cursor": "pointer"
    })
    container.set_attribute("data-name", "Container")

    @when(container.events.click)
    def handle_container_click(sender, event):
        if event:
            event.stopPropagation()  # Prevent event bubbling
        show_parent_info(sender, "Container")

    # Level 2: Header, Content, Footer
    header = Div(style={
        "padding": "15px",
        "margin": "10px",
        "background-color": "#c5e1a5",
        "border": "2px solid #7cb342",
        "border-radius": "6px",
        "cursor": "pointer"
    })
    header.set_attribute("data-name", "Header")

    @when(header.events.click)
    def handle_header_click(sender, event):
        event.stopPropagation()
        show_parent_info(sender, "Header")

    content = Div(style={
        "padding": "15px",
        "margin": "10px",
        "background-color": "#fff9c4",
        "border": "2px solid #fbc02d",
        "border-radius": "6px",
        "cursor": "pointer"
    })
    content.set_attribute("data-name", "Content")

    @when(content.events.click)
    def handle_content_click(sender, event):
        event.stopPropagation()
        show_parent_info(sender, "Content")

    footer = Div(style={
        "padding": "15px",
        "margin": "10px",
        "background-color": "#f8bbd0",
        "border": "2px solid #e91e63",
        "border-radius": "6px",
        "cursor": "pointer"
    })
    footer.set_attribute("data-name", "Footer")

    @when(footer.events.click)
    def handle_footer_click(sender, event):
        event.stopPropagation()
        show_parent_info(sender, "Footer")

    # Level 3: Header children
    header_title = Div("Header Title", style={
        "padding": "10px",
        "margin": "5px",
        "background-color": "#aed581",
        "border": "2px solid #558b2f",
        "border-radius": "4px",
        "cursor": "pointer"
    })
    header_title.set_attribute("data-name", "Header Title")

    @when(header_title.events.click)
    def handle_header_title_click(sender, event):
        event.stopPropagation()
        show_parent_info(sender, "Header Title")

    header_subtitle = Div("Header Subtitle", style={
        "padding": "10px",
        "margin": "5px",
        "background-color": "#aed581",
        "border": "2px solid #558b2f",
        "border-radius": "4px",
        "cursor": "pointer"
    })
    header_subtitle.set_attribute("data-name", "Header Subtitle")

    @when(header_subtitle.events.click)
    def handle_header_subtitle_click(sender, event):
        event.stopPropagation()
        show_parent_info(sender, "Header Subtitle")

    header.add(header_title, header_subtitle)

    # Level 3: Content children
    content_section1 = Div("Content Section 1", style={
        "padding": "10px",
        "margin": "5px",
        "background-color": "#fff59d",
        "border": "2px solid #f57f17",
        "border-radius": "4px",
        "cursor": "pointer"
    })
    content_section1.set_attribute("data-name", "Content Section 1")

    @when(content_section1.events.click)
    def handle_content_section1_click(sender, event):
        event.stopPropagation()
        show_parent_info(sender, "Content Section 1")

    content_section2 = Div(style={
        "padding": "10px",
        "margin": "5px",
        "background-color": "#fff59d",
        "border": "2px solid #f57f17",
        "border-radius": "4px",
        "cursor": "pointer"
    })
    content_section2.set_attribute("data-name", "Content Section 2")

    @when(content_section2.events.click)
    def handle_content_section2_click(sender, event):
        event.stopPropagation()
        show_parent_info(sender, "Content Section 2")

    # Level 4: Nested content
    nested_item1 = Div("Nested Item 1", style={
        "padding": "8px",
        "margin": "3px",
        "background-color": "#ffecb3",
        "border": "1px solid #ff6f00",
        "border-radius": "3px",
        "cursor": "pointer"
    })
    nested_item1.set_attribute("data-name", "Nested Item 1")

    @when(nested_item1.events.click)
    def handle_nested_item1_click(sender, event):
        event.stopPropagation()
        show_parent_info(sender, "Nested Item 1")

    nested_item2 = Div("Nested Item 2", style={
        "padding": "8px",
        "margin": "3px",
        "background-color": "#ffecb3",
        "border": "1px solid #ff6f00",
        "border-radius": "3px",
        "cursor": "pointer"
    })
    nested_item2.set_attribute("data-name", "Nested Item 2")

    @when(nested_item2.events.click)
    def handle_nested_item2_click(sender, event):
        event.stopPropagation()
        show_parent_info(sender, "Nested Item 2")

    content_section2.add("Section 2 Label: ", nested_item1, nested_item2)
    content.add(content_section1, content_section2)

    # Level 3: Footer children
    footer_links = Div(style={
        "padding": "10px",
        "margin": "5px",
        "background-color": "#f48fb1",
        "border": "2px solid #c2185b",
        "border-radius": "4px",
        "cursor": "pointer"
    })
    footer_links.set_attribute("data-name", "Footer Links")

    @when(footer_links.events.click)
    def handle_footer_links_click(sender, event):
        event.stopPropagation()
        show_parent_info(sender, "Footer Links")


    # Level 4: Individual links
    link1 = Div("Link 1", style={
        "display": "inline-block",
        "padding": "5px 10px",
        "margin": "3px",
        "background-color": "#fce4ec",
        "border": "1px solid #880e4f",
        "border-radius": "3px",
        "cursor": "pointer"
    })
    link1.set_attribute("data-name", "Link 1")

    @when(link1.events.click)
    def handle_link1_click(sender, event):
        event.stopPropagation()
        show_parent_info(sender, "Link 1")

    link2 = Div("Link 2", style={
        "display": "inline-block",
        "padding": "5px 10px",
        "margin": "3px",
        "background-color": "#fce4ec",
        "border": "1px solid #880e4f",
        "border-radius": "3px",
        "cursor": "pointer"
    })
    link2.set_attribute("data-name", "Link 2")

    @when(link2.events.click)
    def handle_link2_click(sender, event):
        event.stopPropagation()
        show_parent_info(sender, "Link 2")

    link3 = Div("Link 3", style={
        "display": "inline-block",
        "padding": "5px 10px",
        "margin": "3px",
        "background-color": "#fce4ec",
        "border": "1px solid #880e4f",
        "border-radius": "3px",
        "cursor": "pointer"
    })
    link3.set_attribute("data-name", "Link 3")

    @when(link3.events.click)
    def handle_link3_click(sender, event):
        event.stopPropagation()
        show_parent_info(sender, "Link 3")

    footer_links.add(link1, link2, link3)
    footer.add("Footer: ", footer_links)
    # Assemble the tree
    container.add(header, content, footer)

    DOM.add(container)

    # ========== Legend ==========
    DOM.add(
        Hr(style={"margin": "30px 0"}),
        H2("How it Works"),
        Ul(
            Li("Click on ", Strong("any colored box"), " to see its parent"),
            Li("The modal shows the parent element's name, tag, and number of children"),
            Li("The ", Strong("ancestor chain"), " shows the path from the clicked element to the root"),
            Li("Notice how ", Code("element.parent"), " automatically tracks relationships")
        ),
        Div(
            P(Strong("Structure:"), style={"margin-bottom": "10px"}),
            Pre("""Container (blue)
├── Header (green)
│   ├── Header Title
│   └── Header Subtitle
├── Content (yellow)
│   ├── Content Section 1
│   └── Content Section 2
│       ├── Nested Item 1
│       └── Nested Item 2
└── Footer (pink)
    └── Footer Links
        ├── Link 1
        ├── Link 2
        └── Link 3""", style={
                "background-color": "#f5f5f5",
                "padding": "15px",
                "border-radius": "4px",
                "font-size": "13px",
                "font-family": "monospace",
                "white-space": "pre",
                "overflow-x": "auto",
                "margin": "0"
            })
        , style={
            "padding": "15px",
            "background-color": "#f8f9fa",
            "border-radius": "4px",
            "margin-top": "20px"
        })
    )


if __name__ == "__main__":
    main()
