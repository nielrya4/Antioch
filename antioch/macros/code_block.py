"""
CodeBlock macro - Syntax-highlighted code viewer/editor using CodeMirror.
Supports multiple programming languages, themes, and optional editing.
"""
import js
from pyodide.ffi import create_proxy, to_js
from .base import Macro
from ..elements import Div
from ..lib.loader import inject_script, inject_stylesheet

# Ensure CodeMirror is loaded when this module is imported
inject_stylesheet('https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/codemirror.min.css')
inject_script('https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/codemirror.min.js')

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


class CodeBlock(Macro):
    """
    Syntax-highlighted code viewer/editor component powered by CodeMirror.

    Supports multiple programming languages, themes, and optional editing capabilities.
    Can load content from strings, VFS files, or server files.

    Usage:
        # Basic usage with string
        code = CodeBlock(
            content="def hello():\\n    print('Hello, world!')",
            language="python",
            editable=False
        )
        DOM.add(code.element)

        # Editable with custom theme
        editor = CodeBlock(
            content="const x = 42;",
            language="javascript",
            editable=True,
            theme="monokai",
            line_numbers=True
        )
        editor.on_change(lambda text: print(f"New content: {text}"))

        # Load from file
        from pyodide.http import pyfetch
        import asyncio
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(pyfetch("scripts/main.py"))
        content = loop.run_until_complete(response.string())
        code = CodeBlock(content=content, language="python")
    """

    def __init__(self, content=None, language="python",
                 editable=False, theme="default", line_numbers=True,
                 width="100%", height="400px", container_style=None,
                 lazy_init=False, **kwargs):
        """
        Initialize CodeBlock component.

        Args:
            content: String content to display
            language: Programming language for syntax highlighting
                     Options: python, javascript, html, css, markdown, json, etc.
            editable: Whether the code can be edited (default: False)
            theme: CodeMirror theme name (default, monokai, dracula, material, etc.)
            line_numbers: Show line numbers (default: True)
            width: Width of editor container (default: "100%")
            height: Height of editor container (default: "400px")
            container_style: Custom container styles
            lazy_init: Delay initialization until ensure_initialized() is called
            **kwargs: Additional Macro base class arguments
        """
        super().__init__(macro_type="code_block", **kwargs)

        # Set up state
        self._set_state(
            content=content or "",
            language=language,
            editable=editable,
            theme=theme,
            line_numbers=line_numbers,
            width=width,
            height=height,
            editor_instance=None,
            initialized=False,
            initializing=False,
            init_retry_count=0,
            mode_loaded=False,
            theme_loaded=(theme == "default"),
            lazy_init=lazy_init
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

        # Callback types
        self._add_callback_type('ready')
        self._add_callback_type('change')
        self._add_callback_type('focus')
        self._add_callback_type('blur')

        # Load language mode and theme if needed
        if language in LANGUAGE_MODES:
            inject_script(LANGUAGE_MODES[language])

        if theme != "default" and theme in THEMES:
            inject_stylesheet(THEMES[theme])

        # Initialize macro
        self._init_macro()

    def _create_elements(self):
        """Create the editor container element."""
        # Create container with unique ID for CodeMirror
        container = self._register_element('container',
                                          self._create_container(self._container_style))

        # Create textarea element (CodeMirror will replace this)
        textarea = Div()
        textarea.set_attribute("id", f"editor_{self._id}")
        textarea.style.height = "100%"
        container.add(textarea)

        # Initialize CodeMirror after DOM ready (unless lazy)
        if not self._get_state('lazy_init'):
            init_proxy = create_proxy(lambda: self._initialize_editor())
            js.setTimeout(init_proxy, 100)

        return container

    def _initialize_editor(self):
        """Initialize CodeMirror instance with retry mechanism."""
        import js
        from pyodide.ffi import create_proxy

        if self._get_state('initialized'):
            return

        retry_count = self._get_state('init_retry_count')
        if retry_count > 50:  # Max 50 retries (5 seconds)
            print(f"CodeMirror initialization failed after {retry_count} attempts")
            print("Make sure CodeMirror is loaded in the HTML page")
            return

        try:
            # Check if CodeMirror is loaded
            if not hasattr(js, 'CodeMirror') or not js.CodeMirror:
                # Not loaded yet, retry
                self._set_state(init_retry_count=retry_count + 1)
                init_proxy = create_proxy(lambda: self._initialize_editor())
                js.setTimeout(init_proxy, 100)
                return

            # Get the container element
            textarea_element = js.document.getElementById(f"editor_{self._id}")
            if not textarea_element:
                # Element not ready
                self._set_state(init_retry_count=retry_count + 1)
                init_proxy = create_proxy(lambda: self._initialize_editor())
                js.setTimeout(init_proxy, 100)
                return

            # Build CodeMirror options
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

            # Convert to JS object
            js_config = to_js(config, dict_converter=js.Object.fromEntries)

            # Create CodeMirror instance
            # CodeMirror replaces the element, so we create it directly
            editor_instance = js.CodeMirror(textarea_element, js_config)

            # Set CodeMirror size to fill container
            width = self._get_state('width')
            height = self._get_state('height')
            editor_instance.setSize(width, height)

            # Store instance
            self._set_state(editor_instance=editor_instance, initialized=True, initializing=False)

            # Set up change listener if editable
            if editable:
                change_proxy = create_proxy(lambda *args: self._on_content_change(args[0] if args else None))
                editor_instance.on('change', change_proxy)

            # Set up focus/blur listeners
            focus_proxy = create_proxy(lambda *args: self._trigger_callbacks('focus', self))
            blur_proxy = create_proxy(lambda *args: self._trigger_callbacks('blur', self))
            editor_instance.on('focus', focus_proxy)
            editor_instance.on('blur', blur_proxy)

            # Trigger ready callback
            self._trigger_callbacks('ready', self)

            # If this was lazy init, do an initial refresh
            if self._get_state('lazy_init'):
                refresh_proxy = create_proxy(lambda: self.refresh())
                js.setTimeout(refresh_proxy, 50)
                js.setTimeout(refresh_proxy, 150)

        except Exception as e:
            print(f"CodeMirror initialization error: {e}")
            # Retry with longer delay on error
            self._set_state(init_retry_count=retry_count + 1)
            init_proxy = create_proxy(lambda: self._initialize_editor())
            js.setTimeout(init_proxy, 200)

    def _on_content_change(self, cm):
        """Handle content change events."""
        new_content = cm.getValue()
        self._set_state(content=new_content)
        self._trigger_callbacks('change', new_content)

    def get_content(self):
        """
        Get current editor content.

        Returns:
            str: Current content in the editor
        """
        editor = self._get_state('editor_instance')
        if editor:
            return editor.getValue()
        return self._get_state('content')

    def set_content(self, content):
        """
        Set editor content.

        Args:
            content: New content string

        Returns:
            Self for method chaining
        """
        self._set_state(content=content)
        editor = self._get_state('editor_instance')
        if editor:
            editor.setValue(content)
        return self

    def load_file(self, file_path):
        """
        Load content from VFS file.

        Args:
            file_path: Path to file in virtual filesystem

        Returns:
            Self for method chaining
        """
        content = self._load_from_file(file_path)
        self._set_state(file_path=file_path)
        return self.set_content(content)

    def set_language(self, language):
        """
        Change the language/mode.

        Args:
            language: New language (python, javascript, etc.)

        Returns:
            Self for method chaining
        """
        self._set_state(language=language)
        editor = self._get_state('editor_instance')

        if editor:
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
            editor.setOption('mode', mode)

        return self

    def set_theme(self, theme):
        """
        Change the editor theme.

        Args:
            theme: Theme name (monokai, dracula, material, etc.)

        Returns:
            Self for method chaining
        """
        # Load theme stylesheet if needed
        if theme != "default" and theme in THEMES:
            inject_stylesheet(THEMES[theme])

        self._set_state(theme=theme)
        editor = self._get_state('editor_instance')

        if editor:
            editor.setOption('theme', theme)

        return self

    def set_editable(self, editable):
        """
        Toggle editable mode.

        Args:
            editable: True to enable editing, False to disable

        Returns:
            Self for method chaining
        """
        self._set_state(editable=editable)
        editor = self._get_state('editor_instance')

        if editor:
            editor.setOption('readOnly', not editable)

        return self

    def ensure_initialized(self):
        """
        Ensure the editor is initialized (for lazy init).

        Returns:
            Self for method chaining
        """
        import js
        from pyodide.ffi import create_proxy

        if not self._get_state('initialized') and not self._get_state('initializing'):
            # Mark as initializing to prevent multiple calls
            self._set_state(initializing=True)
            # Call async to allow DOM to be ready
            init_proxy = create_proxy(lambda: self._initialize_editor())
            js.setTimeout(init_proxy, 10)
        return self

    def refresh(self):
        """
        Refresh the editor (useful after visibility changes).

        Returns:
            Self for method chaining
        """
        import js

        # Ensure initialized first (for lazy init)
        self.ensure_initialized()

        editor = self._get_state('editor_instance')
        if editor:
            # Force size recalculation and refresh
            width = self._get_state('width')
            height = self._get_state('height')

            # Scroll to top first
            editor.scrollTo(0, 0)

            # Set size on CodeMirror instance
            editor.setSize(width, height)

            # Force height on wrapper and scroller elements
            wrapper = editor.getWrapperElement()
            if wrapper:
                wrapper.style.height = height
                # Find and set scroller height and scroll position
                scroller = wrapper.querySelector('.CodeMirror-scroll')
                if scroller:
                    scroller.style.height = height
                    scroller.style.maxHeight = height
                    scroller.scrollTop = 0  # Force scroll to top

            # Force refresh
            editor.refresh()
        return self

    def focus(self):
        """
        Focus the editor.

        Returns:
            Self for method chaining
        """
        editor = self._get_state('editor_instance')
        if editor:
            editor.focus()
        return self

    def on_change(self, callback):
        """
        Register callback for content changes.

        Args:
            callback: Function(new_content) called when content changes

        Returns:
            Self for method chaining
        """
        return self.on('change', callback)

    def on_ready(self, callback):
        """
        Register callback for when editor is ready.

        Args:
            callback: Function(self) called when editor is initialized

        Returns:
            Self for method chaining
        """
        return self.on('ready', callback)

    def destroy(self):
        """Destroy editor instance and clean up."""
        editor = self._get_state('editor_instance')
        if editor:
            # CodeMirror doesn't have a destroy method, but we can clear it
            editor.toTextArea()  # Restore original textarea
            self._set_state(editor_instance=None, initialized=False)

        super().destroy()

    @property
    def editor(self):
        """
        Access native CodeMirror instance for advanced usage.

        Returns:
            JavaScript CodeMirror object or None if not initialized
        """
        return self._get_state('editor_instance')

    @property
    def is_ready(self):
        """Check if editor is initialized."""
        return self._get_state('initialized')

    @property
    def content(self):
        """Get current content."""
        return self.get_content()