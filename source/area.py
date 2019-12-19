import arcade
TILE_SCALING = 1


class Area:
    """Information about different 'rooms' in the game"""

    def __init__(self):
        # lists for coins, walls, monsters, etc
        self.tree_list = None
        self.item_list = None
        # holds backgrounds images. Can delete if don't want changing backgrounds.
        self.background = None

    def setup_area(self, map_name, wall_layer, items_layer, background_layer):
        self.tree_list = arcade.SpriteList()
        self.item_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()

        # load in tiled map
        map = arcade.tilemap.read_tmx(map_name)
        self.tree_list = arcade.tilemap.process_layer(
            map, wall_layer, TILE_SCALING)
        self.item_list = arcade.tilemap.process_layer(
            map, items_layer, TILE_SCALING)
        self.background_list = arcade.tilemap.process_layer(
            map, background_layer, TILE_SCALING)
