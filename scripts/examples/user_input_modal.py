"""
User Input Modal Example
Demonstrates a modal with text input and alert feedback.
"""
from antioch import *
from antioch.macros import Modal, Alert


def main():
    DOM.add(
        H2("User Input Modal Example"),
        P("Click the button below to open a modal that asks for your input.")
    )

    # Create an alert for showing the result
    alert = Alert(
        message="",
        alert_type="success",
        dismissible=True
    )
    DOM.add(alert.element)
    alert.dismiss()  # Start hidden (properly sets internal state)

    # Create the modal
    modal = Modal(
        title="Enter Your Name",
        closable=True,
        escape_key_close=True,
        backdrop_click_close=True
    )

    # Create the input field
    name_input = Input(
        input_type="text",
        placeholder="Enter your name...",
        style={
            "width": "100%",
            "padding": "10px",
            "border": "1px solid #ddd",
            "border-radius": "4px",
            "font-size": "14px",
            "box-sizing": "border-box"
        }
    )

    # Add content to modal
    modal.set_content(
        Div(
            P("Please enter your name below:", style={"margin-bottom": "10px"}),
            name_input
        )
    )

    # Create submit button
    def handle_submit(event):
        user_name = name_input.value.strip()

        if user_name:
            # Show alert with user input
            alert.set_message(f"Hello, {user_name}! Nice to meet you!")
            alert.set_type("success")
            alert.show()

            # Close the modal
            modal.close()

            # Clear the input for next time
            name_input.value = ""
        else:
            # Show warning if input is empty
            alert.set_message("Please enter your name before submitting.")
            alert.set_type("warning")
            alert.show()

    submit_btn = Button(
        "Submit",
        style={
            "background-color": "#28a745",
            "color": "white",
            "border": "none",
            "padding": "10px 20px",
            "border-radius": "4px",
            "cursor": "pointer",
            "font-size": "14px"
        }
    )
    submit_btn.on_click(handle_submit)

    cancel_btn = Button(
        "Cancel",
        style={
            "background-color": "#6c757d",
            "color": "white",
            "border": "none",
            "padding": "10px 20px",
            "border-radius": "4px",
            "cursor": "pointer",
            "font-size": "14px",
            "margin-right": "10px"
        }
    )
    cancel_btn.on_click(lambda e: modal.close())

    # Add footer buttons
    modal.set_footer(cancel_btn, submit_btn)

    # Add the modal to DOM
    DOM.add(modal.element)

    # Create a button to open the modal
    open_modal_btn = Button(
        "Open Modal",
        style={
            "background-color": "#007bff",
            "color": "white",
            "border": "none",
            "padding": "12px 24px",
            "border-radius": "4px",
            "cursor": "pointer",
            "font-size": "16px",
            "margin-top": "20px"
        }
    )
    open_modal_btn.on_click(lambda e: modal.show())

    DOM.add(
        Div(
            open_modal_btn,
            style={"margin-top": "20px"}
        )
    )

    # Also allow Enter key to submit
    name_input.on_keydown(lambda e: handle_submit(e) if e.key == "Enter" else None)


if __name__ == "__main__":
    main()