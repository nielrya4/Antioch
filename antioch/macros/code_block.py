"""
CodeBlock macro - Syntax-highlighted code viewer/editor using CodeMirror.
Supports multiple programming languages, themes, and optional editing.
"""
import js
from .js_library import JSLibraryMacro
from ..elements import Div
from ..lib.loader import inject_script, inject_stylesheet

# Common language modes (loaded on demand)
LANGUAGE_MODES = {
    'python': 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/python/python.min.js',
    'javascript': 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/javascript/javascript.min.js',
    'html': 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/htmlmixed/htmlmixed.min.js',
    'css': 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/css/css.min.js',
    'markdown': 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/markdown/markdown.min.js',
    'xml': 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/xml/xml.min.js',
    'json': 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/javascript/javascript.min.js',
    'sql': 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/sql/sql.min.js',
    'shell': 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/shell/shell.min.js',
    'yaml': 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/yaml/yaml.min.js',
    'rust': 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/rust/rust.min.js',
    'go': 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/go/go.min.js',
    'c': 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/clike/clike.min.js',
    'cpp': 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/clike/clike.min.js',
    'java': 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/clike/clike.min.js',
    'ruby': 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/ruby/ruby.min.js',
    'php': 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/php/php.min.js',
    'swift': 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/swift/swift.min.js',
}

# Optional themes (loaded on demand)
THEMES = {
    'monokai': 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/theme/monokai.min.css',
    'dracula': 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/theme/dracula.min.css',
    'material': 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/theme/material.min.css',
    'eclipse': 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/theme/eclipse.min.css',
    'solarized': 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/theme/solarized.min.css',
    'nord': 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/theme/nord.min.css',
}


class CodeBlock(JSLibraryMacro):
    """
    Syntax-highlighted code viewer/editor component powered by CodeMirror.

    Supports multiple programming languages, themes, and optional editing capabilities.

    Usage:
        # Basic usage
        code = CodeBlock(
            content="def hello():\\n    print('Hello!')",
            language="python",
            editable=False
        )
        DOM.add(code.element)

        # Editable with theme
        editor = CodeBlock(
            content="const x = 42;",
            language="javascript",
            editable=True,
            theme="monokai",
            line_numbers=True
        )
        editor.on_change(lambda text: print(f"New: {text}"))
    """

    def __init__(self, content=None, language="python",
                 editable=False, theme="default", line_numbers=True,
                 width="100%", height="400px", container_style=None,
                 lazy_init=False, **kwargs):
        """
        Initialize CodeBlock component.

        Args:
            content: String content to display
            language: Programming language (python, javascript, html, css, etc.)
            editable: Whether code can be edited (default: False)
            theme: CodeMirror theme (default, monokai, dracula, material, etc.)
            line_numbers: Show line numbers (default: True)
            width: Width of editor container
            height: Height of editor container
            container_style: Custom container styles
            lazy_init: Delay initialization until ensure_initialized()
            **kwargs: Additional JSLibraryMacro arguments
        """
        # Initialize base class
        super().__init__(macro_type="code_block", lazy_init=lazy_init, **kwargs)

        # Set up state
        self._set_state(
            content=content or "",
            language=language,
            editable=editable,
            theme=theme,
            line_numbers=line_numbers,
            width=width,
            height=height
        )

        # Default container style
        default_container_style = {
            "width": width,
            "height": height,
            "border": "1px solid #ddd",
            "border_radius": "4px",
            "font_family": "monospace",
            "font_size": "14px"
        }

        self._container_style = self._merge_styles(default_container_style, container_style)

        # Create unified Events for decorator usage
        self._create_event('change')
        self._create_event('focus')
        self._create_event('blur')

        # Initialize macro
        self._init_macro()

    # ========== Required JSLibraryMacro Methods ==========

    def _get_library_dependencies(self):
        """Specify CodeMirror library to load."""
        scripts = ['https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/codemirror.min.js']
        stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/codemirror.min.css']

        # Add language mode script if available
        language = self._get_state('language')
        if language in LANGUAGE_MODES:
            scripts.append(LANGUAGE_MODES[language])

        # Add theme stylesheet if available
        theme = self._get_state('theme')
        if theme != "default" and theme in THEMES:
            stylesheets.append(THEMES[theme])

        return {
            'scripts': scripts,
            'stylesheets': stylesheets
        }

    def _get_library_global_name(self):
        """CodeMirror exposes the 'CodeMirror' global."""
        return 'CodeMirror'

    def _create_elements(self):
        """Create the editor container element."""
        # Create container
        container = self._register_element('container',
                                          self._create_container(self._container_style))

        # Create textarea element (CodeMirror will replace this)
        textarea = Div()
        textarea.set_attribute("id", f"editor_{self._id}")
        textarea.style.height = "100%"
        container.add(textarea)

        return container

    def _create_js_instance(self):
        """Create CodeMirror instance."""
        content = self._get_state('content')
        language = self._get_state('language')
        theme = self._get_state('theme')
        editable = self._get_state('editable')
        line_numbers = self._get_state('line_numbers')

        # Map language to CodeMirror mode
        mode_map = {
            'python': 'python',
            'javascript': 'javascript',
            'json': 'javascript',
            'html': 'htmlmixed',
            'css': 'css',
            'markdown': 'markdown',
            'xml': 'xml',
            'sql': 'sql',
            'shell': 'shell',
            'yaml': 'yaml',
            'rust': 'rust',
            'go': 'go',
            'c': 'text/x-csrc',
            'cpp': 'text/x-c++src',
            'java': 'text/x-java',
            'ruby': 'ruby',
            'php': 'php',
            'swift': 'swift',
        }

        mode = mode_map.get(language, 'python')

        # Get the textarea element
        textarea_element = js.document.getElementById(f"editor_{self._id}")

        # Create CodeMirror configuration
        config = {
            'value': content,
            'mode': mode,
            'theme': theme,
            'lineNumbers': line_numbers,
            'readOnly': not editable,
            'lineWrapping': True,
            'autofocus': False,
        }

        # Create CodeMirror instance
        editor_instance = js.CodeMirror(textarea_element, self._to_js(config))

        # Set up event handlers if editable
        if editable:
            def handle_change(cm, *args):
                new_content = cm.getValue()
                self._set_state(content=new_content)
                self._fire_event('change', new_content)

            def handle_focus(*args):
                self._fire_event('focus', self)

            def handle_blur(*args):
                self._fire_event('blur', self)

            # Add event listeners - CodeMirror uses .on() method
            # Create and store proxies manually
            change_proxy = self._create_proxy(handle_change)
            focus_proxy = self._create_proxy(handle_focus)
            blur_proxy = self._create_proxy(handle_blur)

            editor_instance.on('change', change_proxy)
            editor_instance.on('focus', focus_proxy)
            editor_instance.on('blur', blur_proxy)

        return editor_instance

    def _cleanup_js_instance(self):
        """Clean up CodeMirror instance."""
        if self.js_instance:
            # CodeMirror cleanup
            editor = self.js_instance
            editor.toTextArea()  # Convert back to textarea before destroy

    # ========== Public API Methods ==========

    def get_value(self):
        """
        Get current editor content.

        Returns:
            String content of the editor
        """
        if self.is_initialized:
            return self.js_instance.getValue()
        return self._get_state('content')

    def set_value(self, content):
        """
        Set editor content.

        Args:
            content: New content string

        Returns:
            Self for method chaining
        """
        self._set_state(content=content)

        if self.is_initialized:
            self.js_instance.setValue(content)

        return self

    def set_language(self, language):
        """
        Change the syntax highlighting language.

        Args:
            language: New language mode

        Returns:
            Self for method chaining
        """
        self._set_state(language=language)

        if self.is_initialized:
            # Load mode if needed
            if language in LANGUAGE_MODES:
                inject_script(LANGUAGE_MODES[language])

            # Map to CodeMirror mode
            mode_map = {
                'python': 'python',
                'javascript': 'javascript',
                'json': 'javascript',
                'html': 'htmlmixed',
                'css': 'css',
                'markdown': 'markdown',
                'xml': 'xml',
                'sql': 'sql',
                'shell': 'shell',
                'yaml': 'yaml',
                'rust': 'rust',
                'go': 'go',
                'c': 'text/x-csrc',
                'cpp': 'text/x-c++src',
                'java': 'text/x-java',
                'ruby': 'ruby',
                'php': 'php',
                'swift': 'swift',
            }

            mode = mode_map.get(language, 'python')
            self.js_instance.setOption('mode', mode)

        return self

    def set_theme(self, theme):
        """
        Change the editor theme.

        Args:
            theme: Theme name (monokai, dracula, material, etc.)

        Returns:
            Self for method chaining
        """
        self._set_state(theme=theme)

        # Load theme CSS if needed
        if theme != "default" and theme in THEMES:
            inject_stylesheet(THEMES[theme])

        if self.is_initialized:
            self.js_instance.setOption('theme', theme)

        return self

    def set_editable(self, editable):
        """
        Toggle editable mode.

        Args:
            editable: True to enable editing, False to make read-only

        Returns:
            Self for method chaining
        """
        self._set_state(editable=editable)

        if self.is_initialized:
            self.js_instance.setOption('readOnly', not editable)

        return self

    def refresh(self):
        """
        Refresh the editor display.

        Useful after showing a hidden editor or changing container size.

        Returns:
            Self for method chaining
        """
        if self.is_initialized:
            self.js_instance.refresh()

        return self

    # ========== Callback Helpers ==========

    def on_change(self, callback):
        """
        Register callback for content changes.

        Args:
            callback: Function(new_content) called when content changes

        Returns:
            Self for method chaining
        """
        return self.on('change', callback)

    def on_focus(self, callback):
        """Register callback for focus events."""
        return self.on('focus', callback)

    def on_blur(self, callback):
        """Register callback for blur events."""
        return self.on('blur', callback)

    # ========== Convenience Properties ==========

    @property
    def editor(self):
        """Access native CodeMirror instance."""
        return self.js_instance

    @property
    def value(self):
        """Get/set editor content."""
        return self.get_value()

    @value.setter
    def value(self, content):
        self.set_value(content)