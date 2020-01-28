import arcade
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640
TILE_SCALING = 1


class Area:
    """Information about different 'rooms' in the game"""

    def __init__(self, name, up, down, left, right):
        self.name = name
        # lists for coins, walls, monsters, etc
        self.tree_list = None
        self.item_list = None
        # holds backgrounds images. Can delete if don't want changing backgrounds.
        self.background = None
        self.item_textures = []
        # set up which areas are to the top, bottom, left, and right of the current area
        self.up = up
        self.down = down
        self.left = left
        self.right = right

        self.wall_layer = "walls"
        self.items_layer = "items"
        self.background_layer = "background"

    def setup_area(self, map_name):
        self.tree_list = arcade.SpriteList()
        self.item_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.door_list = arcade.SpriteList()

        # load in tiled map
        map = arcade.tilemap.read_tmx(map_name)
        self.tree_list = arcade.tilemap.process_layer(
            map, self.wall_layer, TILE_SCALING)

        self.background_list = arcade.tilemap.process_layer(
            map, self.background_layer, TILE_SCALING)

        if (arcade.tilemap.get_tilemap_layer(map, self.items_layer) != None):
            self.item_list = arcade.tilemap.process_layer(
                map, self.items_layer, TILE_SCALING)
            for item in self.item_list:
                self.item_textures.append(item.texture)
            print(self.item_textures)
        if (arcade.tilemap.get_tilemap_layer(map, "door") != None):
            # the map in question has a door on it
            self.door_list = arcade.tilemap.process_layer(
                map, "door", TILE_SCALING)

    def get_next_room_name(self, player_sprite):
        # Do some logic here to figure out what room we are in, and if we need to go
        # to a different room.
        if player_sprite.center_x > SCREEN_WIDTH:  # you need to go right
            return (self.right, "right")
        elif player_sprite.center_x < 0:
            return (self.left, "left")
        elif player_sprite.center_y > SCREEN_HEIGHT:
            return (self.up, "up")
        elif player_sprite.center_y < 0:
            return (self.down, "down")
