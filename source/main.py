import arcade
import random
from area import Area
from inventory import InventoryView
from interior import InteriorView
from quest import Quest

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640
WIN_SCORE = 7
MOVEMENT_SPEED = 5
TILE_SCALING = 1

RED = 0
BLACK = 1
GREEN = 2
PURPLE = 3
BOOK = 4
YELLOW = 5
BLUE = 6


class WitchGame(arcade.View):
    """ Main application class"""

    def setup(self):
        # create the sprite lists
        self.player_list = arcade.SpriteList()
        self.found_items = arcade.SpriteList()
        self.item_collect_sound = arcade.load_sound("../sounds/fire_spell.wav")
        self.win_sound = arcade.load_sound("../sounds/win_sound.wav")

        self.inventory = InventoryView(self)

        # set up the score
        self.score = 0

        # set up the player
        self.player_sprite = arcade.Sprite(
            "../sprites/Witch_Sprite/witch_front.png", TILE_SCALING)
        self.player_sprite.center_x = 400  # starting position
        self.player_sprite.center_y = 350

        self.player_list.append(self.player_sprite)

        self.area_refs = {}
        self.areas = []
        forest1 = Area(name="forest1", up=None, down=None,
                       left="witch_hut_exterior", right="forest2")
        forest1.setup_area("../maps/forest1.tmx")
        self.areas.append(forest1)
        self.area_refs['forest1'] = 0

        forest2 = Area(name="forest2", up=None, down=None,
                       left="forest1", right=None)
        forest2.setup_area("../maps/forest2.tmx")
        self.areas.append(forest2)
        self.area_refs['forest2'] = 1

        witch_hut_ext = Area(name="witch_hut_exterior", up=None, down=None,
                             left=None, right="forest1")
        witch_hut_ext.setup_area("../maps/witch_hut_exterior.tmx")
        self.areas.append(witch_hut_ext)
        self.area_refs['witch_hut_exterior'] = 2

        self.current_area = 2  # start outside the witch's house

        # set up physics engine
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.areas[self.current_area].tree_list)

        # set up the quests
        items_from_area = self.areas[self.area_refs['forest1']].item_textures
        self.quests = []

        self.bookQuest = Quest(
            text="Find a potion recipe book.", textures=items_from_area, items=[BOOK])
        self.quests.append(self.bookQuest)
        self.ingredientsQuest = Quest(text="Find the ingredients for the potion.",
                                      textures=items_from_area, items=[RED, BLUE, BLACK])
        self.quests.append(self.ingredientsQuest)

    def on_draw(self):
        """Render the screen"""
        arcade.start_render()
        self.areas[self.current_area].background_list.draw()
        self.player_list.draw()
        self.areas[self.current_area].item_list.draw()
        self.areas[self.current_area].tree_list.draw()
        self.areas[self.current_area].door_list.draw()
        if(self.score == WIN_SCORE):
            # arcade.play_sound(self.win_sound)
            arcade.draw_text("You won!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.BLACK, 24,
                             align="center", anchor_x="center", anchor_y="center"
                             )

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here"""
        self.physics_engine.update()
        item_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.areas[self.current_area].item_list)
        for item in item_hit_list:
            print(item.texture)
            self.found_items.append(item)
            self.areas[self.current_area].item_list.remove(item)
            for quest in self.quests:
                quest.updateStatus(item.texture)

            # arcade.play_sound(self.item_collect_sound)
            self.score += 1

        door_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.areas[self.current_area].door_list)
        for item in door_hit_list:
            # the player has walked into the door and should move into the room
            # the witch hut interior
            self.player_sprite.center_x = 450
            self.player_sprite.center_y = 230
            interior = InteriorView(
                self.player_sprite, self, self.inventory)
            self.window.show_view(interior)

        next_room_check = self.areas[self.current_area].get_next_room_name(
            self.player_sprite)
        if next_room_check != None and next_room_check[0] != None:
            next_room = next_room_check[0]
            direction_travelled = next_room_check[1]
            if next_room in self.area_refs:
                self.current_area = self.area_refs[next_room]
                self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                                 self.areas[self.current_area].tree_list)
            if direction_travelled == "right":
                self.player_sprite.center_x = 0
            elif direction_travelled == "left":
                self.player_sprite.center_x = SCREEN_WIDTH
            elif direction_travelled == "up":
                self.player_sprite.center_y = 0
            elif direction_travelled == "down":
                self.player_sprite.center_y = SCREEN_HEIGHT

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed"""
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = MOVEMENT_SPEED

        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -MOVEMENT_SPEED

        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED

        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif key == arcade.key.ESCAPE:
            #inventory = InventoryView(self)
            self.inventory.set_return_view(self)
            self.window.show_view(self.inventory)

    def on_key_release(self, key, modifiers):
        """called whenever user releases a key"""
        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A or key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, 'Witch Game')
    game = WitchGame()
    game.setup()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()
