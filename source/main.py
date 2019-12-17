import arcade
import random
# import witch
# from sprite import Sprite

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640
HERB_COUNT = 10
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
        # holds backgrounds images. Can delete if don't want changing backgrounds.
        self.background = None


def setup_area_1():
    """create and return room 1."""
    area = Area()

    """ set up the game and initialise the variables"""
    # sprite lists
    area.tree_list = arcade.SpriteList()

    # load in tiled map
    map_name = "../maps/map1.tmx"
    # name of the layer in the file that has platforms/walls
    platforms_layer_name = 'walls2'

    # read in the tiled map
    my_map = arcade.tilemap.read_tmx(map_name)

    # platforms
    area.tree_list = arcade.tilemap.process_layer(
        my_map, platforms_layer_name, TILE_SCALING)

    # # set up the 'walls'
    # for y in (0, SCREEN_HEIGHT - SPRITE_SIZE_TREE):
    #     for x in range(0, SCREEN_WIDTH, SPRITE_SIZE_TREE):
    #         tree = arcade.Sprite(
    #             "../sprites/Witch_Sprite/tree.png", SPRITE_SCALING_TREE)
    #         tree.left = x
    #         tree.bottom = y
    #         area.tree_list.append(tree)
    # if my_map.background_color:
    #     arcade.set_background_color(my_map.background_color)
    return area


class WitchGame(arcade.Window):
    """ Main application class"""

    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.MOSS_GREEN)

    def setup(self):
        # set up game here...

        # create the sprite lists
        self.player_list = arcade.SpriteList()
        self.herb_list = arcade.SpriteList()
        # self.tree_list = arcade.SpriteList()

        # set up the score
        self.score = 0

        # set up the player

        self.player_sprite = arcade.Sprite(
            "../sprites/Witch_Sprite/witch_front.png", SPRITE_SCALING_WITCH)
        self.player_sprite.center_x = 100  # starting position
        self.player_sprite.center_y = 150

        self.player_list.append(self.player_sprite)

        # create the coins
        for i in range(HERB_COUNT):
            # create herb instance
            herb = arcade.Sprite(
                "../sprites/Shikashi's_Fantasy_Icons_Pack/SingleSprites/herb1.png", SPRITE_SCALING_HERB)
            # position the herb
            herb.center_x = random.randrange(SCREEN_WIDTH)
            herb.center_y = random.randrange(SCREEN_HEIGHT)

            # add herb to the list
            self.herb_list.append(herb)

        # set up trees
        # for i in range(TREE_COUNT):
        #     # create tree instance
        #     tree = arcade.Sprite(
        #         "../sprites/Witch_Sprite/tree.png", SPRITE_SCALING_TREE)
        #     # position the tree
        #     tree.center_x = random.randrange(SCREEN_WIDTH)
        #     tree.center_y = random.randrange(SCREEN_HEIGHT)
        #
        #     # add tree to the list
        #     self.tree_list.append(tree)

        self.areas = []
        area = setup_area_1()
        self.areas.append(area)

        self.current_area = 0

        # set up physics engine
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.areas[self.current_area].tree_list)
        # self.physics_engine = arcade.PhysicsEngineSimple(
        #     self.player_sprite, self.tree_list)

    def on_draw(self):
        """Render the screen"""
        arcade.start_render()
        # drawing code goes here
        self.player_list.draw()
        self.herb_list.draw()
        self.areas[self.current_area].tree_list.draw()
        # self.tree_list.draw()
        if(self.score == HERB_COUNT):
            arcade.draw_text("You won!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.BLACK, 24,
                             align="center", anchor_x="center", anchor_y="center"
                             )

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here"""
        # generate list of all herb sprites that collided with the player
        herbs_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.herb_list)

        # loop through each colliding sprite, remove it, and add to the score
        for herb in herbs_hit_list:
            herb.kill()
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
