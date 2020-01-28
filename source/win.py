import arcade
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640


class WinView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(arcade.color.ASH_GREY)

        arcade.draw_text("You win!", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50, arcade.color.BLACK, 24,
                         align="left", anchor_x="left", anchor_y="center"
                         )
        self.win_sound = arcade.load_sound("../sounds/win_sound.wav")
        arcade.play_sound(self.win_sound)
