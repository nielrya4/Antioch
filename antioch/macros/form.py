"""
Form macro - A reusable form component with validation and field management.
Uses unique IDs and safe event handling for multiple instances.
"""
import uuid
import re
from .base import Macro
from ..elements import Div, Form as BaseForm, Label, Input, Textarea, Button, Span, P


class FormField:
    """Represents a single form field with validation."""
    
    def __init__(self, name, field_type="text", label=None, placeholder=None, 
                 required=False, validators=None, default_value="", **kwargs):
        """
        Initialize a form field.
        
        Args:
            name: Field name (used as key in form data)
            field_type: Input type (text, email, password, textarea, etc.)
            label: Display label for field
            placeholder: Placeholder text
            required: Whether field is required
            validators: List of validation functions
            default_value: Default field value
            **kwargs: Additional attributes for input element
        """
        self.name = name
        self.field_type = field_type
        self.label = label or name.title()
        self.placeholder = placeholder
        self.required = required
        self.validators = validators or []
        self.default_value = default_value
        self.kwargs = kwargs
        self._element = None
        self._error_element = None
        self._container = None
        self.is_valid = True
        self.error_message = ""
        
        # Add required validator if needed
        if required and not any(isinstance(v, RequiredValidator) for v in self.validators):
            self.validators.insert(0, RequiredValidator())
    
    def create_element(self, form_id):
        """Create the DOM elements for this field."""
        field_id = f"{form_id}_{self.name}_{str(uuid.uuid4())[:8]}"
        
        # Container
        self._container = Div(style={
            "margin_bottom": "15px"
        })
        
        # Label
        if self.label:
            label_element = Label(self.label, style={
                "display": "block",
                "margin_bottom": "5px",
                "font_weight": "bold",
                "color": "#333"
            })
            if self.required:
                required_mark = Span(" *", style={"color": "#dc3545"})
                label_element.add(required_mark)
            label_element.set_attribute("for", field_id)
            self._container.add(label_element)
        
        # Input element
        input_style = {
            "width": "100%",
            "padding": "8px 12px",
            "border": "1px solid #ddd",
            "border_radius": "4px",
            "font_size": "14px",
            "box_sizing": "border-box"
        }
        
        if self.field_type == "textarea":
            self._element = Textarea(self.default_value, style=input_style, **self.kwargs)
        else:
            self._element = Input(self.field_type, style=input_style, **self.kwargs)
            if self.default_value:
                self._element.value = self.default_value
        
        self._element.set_attribute("id", field_id)
        self._element.set_attribute("name", self.name)
        
        if self.placeholder:
            self._element.set_attribute("placeholder", self.placeholder)
        
        # Validation on input
        self._element.on_blur(lambda e: self.validate())
        
        self._container.add(self._element)
        
        # Error message container
        self._error_element = Span("", style={
            "color": "#dc3545",
            "font_size": "12px",
            "display": "none",
            "margin_top": "5px"
        })
        self._container.add(self._error_element)
        
        return self._container
    
    def validate(self):
        """Validate this field's value."""
        value = self.get_value()
        self.is_valid = True
        self.error_message = ""
        
        for validator in self.validators:
            try:
                if not validator.validate(value):
                    self.is_valid = False
                    self.error_message = validator.error_message
                    break
            except Exception as e:
                self.is_valid = False
                self.error_message = f"Validation error: {e}"
                break
        
        self._update_ui()
        return self.is_valid
    
    def _update_ui(self):
        """Update UI based on validation state."""
        if not self._element or not self._error_element:
            return
            
        if self.is_valid:
            self._element.style.border_color = "#ddd"
            self._error_element.style.display = "none"
        else:
            self._element.style.border_color = "#dc3545"
            self._error_element.set_text(self.error_message)
            self._error_element.style.display = "block"
    
    def get_value(self):
        """Get the field's current value."""
        return self._element.value if self._element else self.default_value
    
    def set_value(self, value):
        """Set the field's value."""
        if self._element:
            self._element.value = value
    
    def clear(self):
        """Clear the field's value."""
        self.set_value("")


class RequiredValidator:
    """Validator for required fields."""
    
    def __init__(self, message="This field is required"):
        self.error_message = message
    
    def validate(self, value):
        return bool(str(value).strip())


class EmailValidator:
    """Validator for email format."""
    
    def __init__(self, message="Please enter a valid email address"):
        self.error_message = message
        self.pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    def validate(self, value):
        return bool(self.pattern.match(str(value).strip()))


class MinLengthValidator:
    """Validator for minimum length."""
    
    def __init__(self, min_length, message=None):
        self.min_length = min_length
        self.error_message = message or f"Must be at least {min_length} characters"
    
    def validate(self, value):
        return len(str(value)) >= self.min_length


class CustomValidator:
    """Custom validator with user-defined function."""
    
    def __init__(self, validate_func, message="Invalid value"):
        self.validate_func = validate_func
        self.error_message = message
    
    def validate(self, value):
        return self.validate_func(value)


class Form(Macro):
    """A form component with validation and field management."""
    
    def __init__(self, fields=None, submit_text="Submit", reset_text="Reset",
                 show_reset=True, form_style=None, button_style=None, **kwargs):
        """
        Initialize a form component.
        
        Args:
            fields: List of FormField objects
            submit_text: Text for submit button
            reset_text: Text for reset button
            show_reset: Whether to show reset button
            form_style: Custom styles for form container
            button_style: Custom styles for buttons
        """
        # Initialize base macro
        super().__init__(macro_type="form", **kwargs)
        
        # Set up form-specific state
        self._set_state(
            fields={field.name: field for field in (fields or [])},
            submit_text=submit_text,
            reset_text=reset_text,
            show_reset=show_reset
        )
        
        # Add callback types
        self._add_callback_type('submit')
        self._add_callback_type('reset')
        self._add_callback_type('change')
        
        # Default styles
        default_form_style = {
            "max_width": "500px",
            "margin": "0 auto",
            "padding": "20px",
            "border": "1px solid #ddd",
            "border_radius": "8px",
            "background_color": "#fff"
        }
        
        default_button_style = {
            "padding": "10px 20px",
            "border": "none",
            "border_radius": "4px",
            "cursor": "pointer",
            "font_size": "14px",
            "margin_right": "10px"
        }
        
        # Merge with user styles using base class method
        self._form_style = self._merge_styles(default_form_style, form_style)
        self._button_style = self._merge_styles(default_button_style, button_style)
        
        # Initialize macro
        self._init_macro()
    
    def _create_elements(self):
        """Create the form UI elements."""
        # Main container using base class helper
        container = self._create_container(self._form_style)
        
        # Form element
        form_element = self._register_element('form_element', BaseForm())
        form_element.on_submit(self._handle_submit)
        
        # Fields container
        fields_container = self._register_element('fields_container', Div())
        
        # Create field elements
        fields = self._get_state('fields')
        for field in fields.values():
            field_element = field.create_element(self._id)
            fields_container.add(field_element)
            
            # Listen for field changes
            field._element.on_input(lambda e, f=field: self._handle_field_change(f))
        
        # Buttons container
        buttons_container = self._register_element('buttons_container', Div(style={
            "margin_top": "20px",
            "text_align": "right"
        }))
        
        # Submit button
        submit_style = {
            **self._button_style,
            "background_color": "#007bff",
            "color": "white"
        }
        submit_btn = self._register_element('submit_btn', Button(self._get_state('submit_text'), style=submit_style))
        submit_btn.set_attribute("type", "submit")
        buttons_container.add(submit_btn)
        
        # Reset button
        if self._get_state('show_reset'):
            reset_style = {
                **self._button_style,
                "background_color": "#6c757d", 
                "color": "white"
            }
            reset_btn = self._register_element('reset_btn', Button(self._get_state('reset_text'), style=reset_style))
            reset_btn.set_attribute("type", "button")
            reset_btn.on_click(self._handle_reset)
            buttons_container.add(reset_btn)
        
        # Assemble form
        form_element.add(fields_container, buttons_container)
        container.add(form_element)
        
        return container
    
    def _handle_submit(self, event):
        """Handle form submission."""
        event.preventDefault()
        
        # Validate all fields
        is_valid = self.validate()
        
        if is_valid:
            data = self.get_data()
            self._trigger_callbacks('submit', data)
        
        return False
    
    def _handle_reset(self, event):
        """Handle form reset."""
        self.reset()
        self._trigger_callbacks('reset')
    
    def _handle_field_change(self, field):
        """Handle field value change."""
        self._trigger_callbacks('change', field.name, field.get_value(), field)
    
    
    def add_field(self, field):
        """Add a field to the form."""
        fields = self._get_state('fields')
        if field.name in fields:
            # Remove existing field
            self.remove_field(field.name)
        
        fields[field.name] = field
        self._set_state(fields=fields)
        
        # Create and add field element
        fields_container = self._get_element('fields_container')
        field_element = field.create_element(self._id)
        fields_container.add(field_element)
        
        # Listen for changes
        field._element.on_input(lambda e, f=field: self._handle_field_change(f))
        
        return self
    
    def remove_field(self, field_name):
        """Remove a field from the form."""
        fields = self._get_state('fields')
        if field_name in fields:
            field = fields[field_name]
            if field._container:
                field._container.remove()
            del fields[field_name]
            self._set_state(fields=fields)
        return self
    
    def get_field(self, field_name):
        """Get a field by name."""
        fields = self._get_state('fields')
        return fields.get(field_name)
    
    def get_data(self):
        """Get all form data as a dictionary."""
        fields = self._get_state('fields')
        return {name: field.get_value() for name, field in fields.items()}
    
    def set_data(self, data):
        """Set form data from a dictionary."""
        fields = self._get_state('fields')
        for name, value in data.items():
            if name in fields:
                fields[name].set_value(value)
        return self
    
    def validate(self):
        """Validate all fields in the form."""
        fields = self._get_state('fields')
        is_valid = True
        for field in fields.values():
            if not field.validate():
                is_valid = False
        return is_valid
    
    def reset(self):
        """Reset all fields to their default values."""
        fields = self._get_state('fields')
        for field in fields.values():
            field.set_value(field.default_value)
        return self
    
    def clear(self):
        """Clear all field values."""
        fields = self._get_state('fields')
        for field in fields.values():
            field.clear()
        return self
    
    def on_submit(self, callback):
        """Register callback for form submission.
        
        Args:
            callback: Function that takes (form_instance, form_data)
        """
        return self.on('submit', callback)
    
    def on_reset(self, callback):
        """Register callback for form reset."""
        return self.on('reset', callback)
    
    def on_change(self, callback):
        """Register callback for field changes.
        
        Args:
            callback: Function that takes (form_instance, field_name, field_value, field_instance)
        """
        return self.on('change', callback)
    
    # element property is inherited from base class
    
    @property
    def fields(self):
        """Get current fields dictionary for backward compatibility."""
        return self._get_state('fields')