import arcade
TILE_SCALING = 1
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640
NUMBER_OF_QUESTS = 3


class InventoryView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def set_return_view(self, return_view):
        self.return_view = return_view

    def on_draw(self):
        arcade.start_render()
        items = self.game_view.found_items
        arcade.set_background_color(arcade.color.ASH_GREY)

        inv_map = "../maps/inventory.tmx"
        inventory_layer_name = 'target'

        inv_map = arcade.tilemap.read_tmx(inv_map)

        target_list = arcade.tilemap.process_layer(
            inv_map, inventory_layer_name, TILE_SCALING)

        # set items to dim if they haven't been collected and bright if they have been collected
        for item in target_list:
            item.intensity = 'dim'
            item.alpha = 64

        for item in target_list:
            for found_item in items:
                if item.texture == found_item.texture:
                    item.intensity = 'bright'
                    item.alpha = 255

        arcade.draw_text("QUESTS:", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50, arcade.color.BLACK, 24,
                         align="left", anchor_x="left", anchor_y="center"
                         )

        x_variable = (SCREEN_WIDTH / 2) + 50
        quests = self.game_view.quests
        if quests[0].complete:
            text_colour = arcade.color.GREEN
            icon = "X "
        else:
            text_colour = arcade.color.BLACK
            icon = "- "
        arcade.draw_text(icon + quests[0].text, x_variable, SCREEN_HEIGHT - 100, text_colour, 20,
                         align="left", anchor_x="left", anchor_y="center"
                         )
        if quests[1].complete:
            text_colour = arcade.color.GREEN
            icon = "X "
        else:
            text_colour = arcade.color.BLACK
            icon = "- "
        arcade.draw_text(icon + quests[1].text, x_variable, SCREEN_HEIGHT - 200, text_colour, 20,
                         align="left", anchor_x="left", anchor_y="center"
                         )
        arcade.draw_text("Add the ingredients to the cauldron", x_variable, SCREEN_HEIGHT - 300, arcade.color.BLACK, 20,
                         align="left", anchor_x="left", anchor_y="center"
                         )

        target_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.return_view)
