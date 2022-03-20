# GameScene: Prototype for Scenes
class GameScene(object):
    def __init__(self, director):
        self.director = director

    # method gets called when director makes this the active scene
    def on_switchto(self, switchtoargs):
        raise NotImplementedError(
            "on_switchto abstract method must be defined in subclass"
        )

    # used to update physics, in-game states
    def on_update(self):
        raise NotImplementedError(
            "on_update abstract method must be defined in subclass"
        )

    # note/respond to incoming control inputs
    def on_event(self, event):
        raise NotImplementedError(
            "on_event abstract method must be defined in subclass"
        )

    # render the whole scene to the screen each frame
    def on_draw(self, screen):
        raise NotImplementedError("on_draw abstract method must be defined in subclass")
