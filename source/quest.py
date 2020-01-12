class Quest():
    def __init__(self, text, textures, items):
        self.complete = False
        self.text = text
        self.textures = textures  # list of textures from the given area
        # list of items needed for the quest e.g. ["red", "blue"]
        self.items = items

    def isComplete(self):
        if (any(item == False for item in requirements)):
            self.complete = False
        else:
            self.complete = True
        return self.complete
