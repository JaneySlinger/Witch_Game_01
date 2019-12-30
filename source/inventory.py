import arcade
TILE_SCALING = 1


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

        for item in target_list:
            item.intensity = 'dim'
            item.alpha = 64

        for item in target_list:
            for found_item in items:
                if item.texture == found_item.texture:
                    item.intensity = 'bright'
                    item.alpha = 255

        target_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            # how do I know which view to return it to. It could be the interior one.
            # self.window.show_view(self.game_view)
            self.window.show_view(self.return_view)
