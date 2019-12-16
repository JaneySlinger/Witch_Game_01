from sprite import Sprite
import arcade


class Witch(Sprite):
    def __init__(self, img, scale, start_x, start_y, speed):
        super().__init__(self, img, scale, start_x, start_y)
        self.movement_speed = speed

    def move(self, direction):
        if direction == "UP":
            self.player_sprite.change_y = self.movement_speed
        elif direction == "DOWN":
            self.player_sprite.change_y = -self.movement_speed
        elif direction == "LEFT":
            self.player_sprite.change_x = -self.movement_speed
            print(self.player_sprite._get_position())
        elif direction == "RIGHT":
            self.player_sprite.change_x = self.movement_speed
