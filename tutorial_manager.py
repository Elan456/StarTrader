"""
Tutorial objectives that the player can complete.
1. Put a container on your ship
2. Put a weapon on your ship
"""

class Objective:
    def __init__(self, name, check_func):
        self.name = name
        self.check_func = check_func
        self.completed = False

class Tutorial:
    def __init__(self, Viewer, ps, mode):
        self.Viewer = Viewer
        self.ps = ps

        self.objectives = [
        ]

    def update(self):
        pass