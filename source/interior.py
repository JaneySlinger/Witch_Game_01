import arcade
from win import WinView
TILE_SCALING = 1
MOVEMENT_SPEED = 5
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640


class InteriorView(arcade.View):
    def __init__(self, player, game_view, inventory_view):
        super().__init__()
        self.game_view = game_view
        self.inventory_view = inventory_view
        self.player = player
        int_map = arcade.tilemap.read_tmx("../maps/witch_hut_interior.tmx")

        self.background_list = arcade.tilemap.process_layer(
            int_map, "background", TILE_SCALING)
        self.wall_list = arcade.tilemap.process_layer(
            int_map, "walls", TILE_SCALING)
        self.objects_list = arcade.tilemap.process_layer(
            int_map, "objects", TILE_SCALING)
        self.potion_list = arcade.tilemap.process_layer(
            int_map, "potion", TILE_SCALING)
        self.bubbles_list = arcade.tilemap.process_layer(
            int_map, "bubbles", TILE_SCALING)
        self.door_list = arcade.tilemap.process_layer(
            int_map, "door", TILE_SCALING)
        self.cauldron_list = arcade.tilemap.process_layer(
            int_map, "cauldron", TILE_SCALING)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, self.wall_list)

    def on_draw(self):
        arcade.start_render()
        self.wall_list.draw()
        self.background_list.draw()
        self.objects_list.draw()
        self.potion_list.draw()
        self.cauldron_list.draw()
        self.bubbles_list.draw()
        self.door_list.draw()

        self.player.draw()

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here"""
        self.physics_engine.update()

        door_hit_list = arcade.check_for_collision_with_list(
            self.player, self.door_list)
        for item in door_hit_list:
            # walked into the doormat so need to leave the witch hut
            self.player.center_x = 500
            self.player.center_y = 350
            self.window.show_view(self.game_view)

        cauldron_hit_list = arcade.check_for_collision_with_list(
            self.player, self.cauldron_list)
        for item in cauldron_hit_list:
            if all(quest.complete == True for quest in self.game_view.quests):
                # if the previous quests are complete
                win = WinView()
                self.window.show_view(win)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed"""
        if key == arcade.key.UP or key == arcade.key.W:
            self.player.change_y = MOVEMENT_SPEED

        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y = -MOVEMENT_SPEED

        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -MOVEMENT_SPEED

        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = MOVEMENT_SPEED
        elif key == arcade.key.ESCAPE:
            self.inventory_view.set_return_view(self)
            self.window.show_view(self.inventory_view)

    def on_key_release(self, key, modifiers):
        """called whenever user releases a key"""
        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A or key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = 0
