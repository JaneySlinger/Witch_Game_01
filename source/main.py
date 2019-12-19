import arcade
import random
from area import Area
from inventory import InventoryView

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640
WIN_SCORE = 7
MOVEMENT_SPEED = 5
TILE_SCALING = 1


class WitchGame(arcade.View):
    """ Main application class"""

    def setup(self):
        # create the sprite lists
        self.player_list = arcade.SpriteList()
        self.found_items = arcade.SpriteList()
        self.item_collect_sound = arcade.load_sound("../sounds/fire_spell.wav")
        self.win_sound = arcade.load_sound("../sounds/win_sound.wav")

        # set up the score
        self.score = 0

        # set up the player
        self.player_sprite = arcade.Sprite(
            "../sprites/Witch_Sprite/witch_front.png", TILE_SCALING)
        self.player_sprite.center_x = 100  # starting position
        self.player_sprite.center_y = 300

        self.player_list.append(self.player_sprite)

        self.areas = []
        area = Area()
        area.setup_area(map_name="../maps/map1.tmx", wall_layer="walls2",
                        items_layer="items", background_layer="background")
        self.areas.append(area)

        self.current_area = 0

        # set up physics engine
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.areas[self.current_area].tree_list)

    def on_draw(self):
        """Render the screen"""
        arcade.start_render()
        self.areas[self.current_area].background_list.draw()
        self.player_list.draw()
        self.areas[self.current_area].item_list.draw()
        self.areas[self.current_area].tree_list.draw()
        if(self.score == WIN_SCORE):
            arcade.play_sound(self.win_sound)
            arcade.draw_text("You won!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.BLACK, 24,
                             align="center", anchor_x="center", anchor_y="center"
                             )

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here"""
        item_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.areas[self.current_area].item_list)
        for item in item_hit_list:
            self.found_items.append(item)
            self.areas[self.current_area].item_list.remove(item)

            arcade.play_sound(self.item_collect_sound)
            self.score += 1

        self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed"""
        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED

        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED

        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED

        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif key == arcade.key.ESCAPE:
            inventory = InventoryView(self)
            self.window.show_view(inventory)

    def on_key_release(self, key, modifiers):
        """called whenever user releases a key"""
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, 'Witch Game')
    game = WitchGame()
    game.setup()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()
