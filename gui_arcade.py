"""
Menu.

Shows the usage of almost every gui widget, switching views and making a modal.
"""
import arcade
import arcade.gui as g


# Screen title and size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Making a Menu"


class MainView(arcade.View):
    """ Main application class."""

    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()

        switch_menu_button = arcade.gui.UIFlatButton(text="Next", width=250)

        # Initialise the button with an on_click event.
        @switch_menu_button.event("on_click")
        def on_click_switch_button(event):
            # Passing the main view into menu view as an argument.
            pass

        # Use the anchor to position the button on the screen.
        self.anchor = self.manager.add(g.UIAnchorLayout())

        self.anchor.add(
            anchor_x="center_x",
            anchor_y="bottom_y",
            child=switch_menu_button,
        )

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

         # Enable the UIManager when the view is showm.
        self.manager.enable()

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()

        # Draw the manager.
        self.manager.draw()
    
    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
    main_view = MainView()
    window.show_view(main_view)
    arcade.run()


if __name__ == "__main__":
    main()