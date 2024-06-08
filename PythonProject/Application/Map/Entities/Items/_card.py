from Application.Map._wall import Wall


class Card:
    def __init__(self, wall: Wall):
        self.wall = wall

    def __str__(self):
        return f"Card(wall={self.wall})"