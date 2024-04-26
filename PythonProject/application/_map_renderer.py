from map import Map, Tile

class MapRenderer:
    def __init__(self, game_engine):
        self.game_engine = game_engine

    def render(self):
        map = self.game_engine.get_map()
        for vector, tile in map.tiles_dictionary.items():
            print(f"Tile at {vector} has {len(tile.cells_dict)} cells")