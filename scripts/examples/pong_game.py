"""
Paddle Game - Single player game using WebCanvas.
Move the mouse to control the paddle and keep the ball in play!

Loosely based on Microsoft Small Basic Pong example.
"""

import js
from pyodide.ffi import create_proxy
from antioch import DOM, Div, H1, P, Button
from antioch.macros import WebCanvas


class PaddleGame:
    """Simple single-player paddle game."""

    def __init__(self):
        # Canvas dimensions
        self.width = 640
        self.height = 480

        # Create canvas
        self.canvas = WebCanvas(
            width=self.width,
            height=self.height,
            background="#00008B"  # DarkBlue
        )

        # Game state
        self.game_running = True
        self.game_over = False

        # Paddle properties (120x12 like Small Basic)
        self.paddle_width = 120
        self.paddle_height = 12
        self.paddle_x = self.width // 2 - self.paddle_width // 2
        self.paddle_y = self.height - 12

        # Ball properties (16x16 ellipse like Small Basic)
        self.ball_size = 16
        self.ball_x = 0
        self.ball_y = 0
        self.delta_x = 1
        self.delta_y = 1

        # Mouse position
        self.mouse_x = self.width // 2

        # Setup mouse handler
        self._setup_mouse()

        # Animation frame ID
        self.animation_id = None

    def _setup_mouse(self):
        """Setup mouse move handler."""
        canvas_element = self.canvas._get_element('canvas')

        def on_mousemove(event):
            # Get mouse position relative to canvas
            rect = canvas_element._dom_element.getBoundingClientRect()
            self.mouse_x = event.clientX - rect.left

            # Update paddle position - center paddle on mouse
            self.paddle_x = self.mouse_x - self.paddle_width // 2

            # Keep paddle on screen
            if self.paddle_x < 0:
                self.paddle_x = 0
            if self.paddle_x > self.width - self.paddle_width:
                self.paddle_x = self.width - self.paddle_width

        # Attach mousemove handler
        canvas_element.on('mousemove', on_mousemove)

    def update(self):
        """Update game logic - follows Small Basic logic closely."""
        if not self.game_running or self.game_over:
            return

        # Move ball
        self.ball_x = self.ball_x + self.delta_x
        self.ball_y = self.ball_y + self.delta_y

        # Bounce off left and right walls
        if self.ball_x >= self.width - self.ball_size or self.ball_x <= 0:
            self.delta_x = -self.delta_x

        # Bounce off top wall
        if self.ball_y <= 0:
            self.delta_y = -self.delta_y

        # Check paddle collision
        # y = gh - 28 in Small Basic (height - paddle_height - ball_size)
        paddle_collision_y = self.height - self.paddle_height - self.ball_size

        if self.ball_y >= paddle_collision_y:
            # Check if ball is within paddle x range
            if self.ball_x >= self.paddle_x and self.ball_x <= self.paddle_x + self.paddle_width:
                self.delta_y = -self.delta_y

        # Check if ball went off bottom - game over
        if self.ball_y >= self.height:
            self.game_over = True
            self.game_running = False

    def draw(self):
        """Draw the game state."""
        # Clear canvas with dark blue background
        self.canvas.clear("#00008B")

        # Draw paddle (white rectangle)
        self.canvas.rect(
            self.paddle_x,
            self.paddle_y,
            self.paddle_width,
            self.paddle_height,
            fill="#ffffff"
        )

        # Draw ball (white circle - using circle instead of rect)
        self.canvas.circle(
            self.ball_x + self.ball_size // 2,  # Center the circle
            self.ball_y + self.ball_size // 2,
            self.ball_size // 2,
            fill="#ffffff"
        )

        # Draw game over message
        if self.game_over:
            # Show "You Lose" message like Small Basic
            self.canvas.text(
                "You Lose",
                self.width // 2,
                self.height // 2 - 30,
                fill="#ffffff",
                font="bold 48px Arial",
                align="center"
            )

            self.canvas.text(
                "Click 'Restart Game' to play again",
                self.width // 2,
                self.height // 2 + 30,
                fill="#ffffff",
                font="20px Arial",
                align="center"
            )

    def game_loop(self):
        """Main game loop with 5ms delay like Small Basic."""
        self.update()
        self.draw()

        # Continue animation if not game over
        if not self.game_over:
            # Small Basic uses 5ms delay, we'll use requestAnimationFrame
            # which is better but we can throttle it
            self.animation_id = js.setTimeout(
                create_proxy(lambda: self.game_loop()),
                5  # 5ms delay like Small Basic
            )

    def restart(self):
        """Restart the game."""
        self.game_running = True
        self.game_over = False
        self.ball_x = 0
        self.ball_y = 0
        self.delta_x = 1
        self.delta_y = 1
        self.paddle_x = self.width // 2 - self.paddle_width // 2

        # Restart game loop
        self.game_loop()

    def get_element(self):
        """Get the canvas element for adding to DOM."""
        return self.canvas.element


def main():
    """Create and display the Paddle game."""
    container = Div(style={
        "max_width": "700px",
        "margin": "20px auto",
        "padding": "20px",
        "font_family": "Arial, sans-serif",
        "background_color": "#ffffff",
        "border_radius": "8px",
        "box_shadow": "0 2px 8px rgba(0,0,0,0.1)"
    })

    # Title
    title = H1("Paddle Game", style={
        "text_align": "center",
        "color": "#2c3e50",
        "margin_bottom": "10px"
    })

    # Instructions
    instructions = Div(style={
        "background_color": "#ecf0f1",
        "padding": "15px",
        "border_radius": "6px",
        "margin_bottom": "20px"
    })

    instructions.add(
        P("🎮 How to Play:", style={"font_weight": "bold", "margin": "0 0 10px 0"}),
        P("• Move your mouse to control the paddle", style={"margin": "5px 0"}),
        P("• Keep the ball from falling off the bottom", style={"margin": "5px 0"}),
        P("• The ball bounces off walls and the paddle", style={"margin": "5px 0"}),
        P("• Don't miss the ball!", style={"margin": "5px 0", "font_weight": "bold"})
    )

    # Create game
    game = PaddleGame()

    # Restart button
    restart_btn = Button("Restart Game", style={
        "margin_top": "15px",
        "padding": "10px 20px",
        "background_color": "#3498db",
        "color": "white",
        "border": "none",
        "border_radius": "5px",
        "font_size": "16px",
        "font_weight": "bold",
        "display": "block",
        "margin_left": "auto",
        "margin_right": "auto"
    })

    def restart_game(event):
        game.restart()

    restart_btn.on_click(restart_game)

    # Add everything to container
    container.add(title, instructions, game.get_element(), restart_btn)

    # Add to DOM
    DOM.add(container)

    # Start the game loop
    game.game_loop()


# Run when explicitly called from main.py
# (Don't run on import, only when main() is called)
