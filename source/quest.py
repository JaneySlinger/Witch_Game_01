class Quest():
    def __init__(self, text, textures, items):
        self.complete = False
        self.text = text
        self.textures = textures  # list of textures from the given area
        # list of indexes needed for the quest e.g. [0,1,2]
        self.items = items
        self.requirements = []  # list of textures representing the items that are needed
        for item in items:
            self.requirements.append(self.textures[item])
        self.status = len(self.requirements)

    def updateStatus(self, new_item):
        # called from main when an item is picked up
        # check if the item is needed for the quest and if it is decrement the number of items found
        if new_item in self.requirements:
            self.status -= 1
        if self.status == 0:
            self.complete = True
