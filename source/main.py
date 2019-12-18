import arcade
import random
# import witch
# from sprite import Sprite

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640
HERB_COUNT = 10
WIN_SCORE = 7
TREE_COUNT = 10
SPRITE_SCALING_WITCH = 1.0
SPRITE_SCALING_HERB = 1.0
SPRITE_SCALING_TREE = 2.5
MOVEMENT_SPEED = 5
SPRITE_SIZE_TREE = int(32 * SPRITE_SCALING_TREE)
TILE_SCALING = 1


class Area:
    """Information about different 'rooms' in the game"""

    def __init__(self):
        # lists for coins, walls, monsters, etc
        self.tree_list = None
        self.item_list = None
        # holds backgrounds images. Can delete if don't want changing backgrounds.
        self.background = None


def setup_area_1():
    """create and return area 1."""
    area = Area()

    area.tree_list = arcade.SpriteList()
    area.item_list = arcade.SpriteList()

    # load in tiled map
    map_name = "../maps/map1.tmx"
    platforms_layer_name = 'walls2'
    items_layer_name = 'items'

    my_map = arcade.tilemap.read_tmx(map_name)

    area.tree_list = arcade.tilemap.process_layer(
        my_map, platforms_layer_name, TILE_SCALING)

    area.item_list = arcade.tilemap.process_layer(
        my_map, items_layer_name, TILE_SCALING)

    return area


class WitchGame(arcade.Window):
    """ Main application class"""

    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.MOSS_GREEN)

    def setup(self):
        # create the sprite lists
        self.player_list = arcade.SpriteList()
        self.item_collect_sound = arcade.load_sound("../sounds/fire_spell.wav")
        self.win_sound = arcade.load_sound("../sounds/win_sound.wav")

        # set up the score
        self.score = 0

        # set up the player
        self.player_sprite = arcade.Sprite(
            "../sprites/Witch_Sprite/witch_front.png", SPRITE_SCALING_WITCH)
        self.player_sprite.center_x = 100  # starting position
        self.player_sprite.center_y = 150

        self.player_list.append(self.player_sprite)

        self.areas = []
        area = setup_area_1()
        self.areas.append(area)

        self.current_area = 0

        # set up physics engine
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.areas[self.current_area].tree_list)

    def on_draw(self):
        """Render the screen"""
        arcade.start_render()
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
            item.kill()
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

    def on_key_release(self, key, modifiers):
        """called whenever user releases a key"""
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


def main():
    game = WitchGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
