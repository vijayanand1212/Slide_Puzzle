class Tile:
    def __init__(self, image, rectangle, pos, slicedImageSize,tileNumber):
        self.image = image
        self.rectangle = rectangle
        self.pos = pos
        self.slicedImageSize = slicedImageSize
        self.tileNumber = tileNumber
    def change_pos(self,newpos,move):
        i,j = newpos
        x = j * self.IMAGE_HEIGHT + (j * 5) + 10
        y = i * self.IMAGE_WIDTH + (i * 5) + 10
        if move == 'up':
            self.rectangle[x][y].y -= self.IMAGE_HEIGHT + 5
        if move == 'down':
            self.rectangle[x][y].y += self.IMAGE_HEIGHT + 5
        if move == 'left':
            self.rectangle[x][y].y -= self.IMAGE_WIDTH + 5
        if move == 'right':
            self.rectangle[x][y].y += self.IMAGE_WIDTH + 5
        self.pos = newpos

