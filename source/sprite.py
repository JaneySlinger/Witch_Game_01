import arcade


class Sprite:
    def __init__(self, img, scale, start_x, start_y):
        self.image = img
        self.scale_factor = scale
        self.x_position = start_x
        self.y_position = start_y

    def setupSprite(self):
        self.player_sprite = arcade.Sprite(
            self.image, self.scale_factor)
        self.player_sprite.center_x = self.x_position  # starting position
        self.player_sprite.center_y = self.y_position
