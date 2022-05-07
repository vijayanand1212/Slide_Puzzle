import pygame
import cv2
import random


opencvImage = cv2.imread('./images/iornMan.jpg')
clock = pygame.time.Clock()
# pygame init
pygame.init()
SCREEN_WIDTH = 500
SCREE_HEIGHT = 500
IMAGE_WIDTH = 125
IMAGE_HEIGHT =125
screen = pygame.display.set_mode((SCREEN_WIDTH + 35,SCREE_HEIGHT + 35))
pygame.display.set_caption("Slide Puzzle")


col = int(SCREEN_WIDTH / IMAGE_WIDTH)
row = int(SCREE_HEIGHT / IMAGE_HEIGHT)
puzzleList = []
imageList = []
puzzleRectList = []
selectedTile = [0,0]
def sliceImage(image):
    global imageList

    for i in range(0,row):
        imageRow = []
        for j in range(0,col):
            imageCrop = image[i * IMAGE_HEIGHT: (i+1) * IMAGE_HEIGHT, j * IMAGE_WIDTH :(j+1) * IMAGE_WIDTH]
            pyImage = pygame.image.frombuffer(imageCrop.tobytes(),imageCrop.shape[1::-1],'BGR')
            imageRow.append(pyImage)
        imageList.append(imageRow)

    imageListL = imageList.pop(-1)
    imageListL = imageListL[:-1]
    imageListL.append(None)
    imageList.append(imageListL)

def shuffle2dArray(list):
    global puzzleList
    ls = []
    rectls = []
    for i,ii in enumerate(list):
        for j,jj in enumerate(ii):
            ls.append(jj)


    random.shuffle(ls)
    imagelsMain = []


    imagelsMain.append(ls[0:4])
    imagelsMain.append(ls[4:8])
    imagelsMain.append(ls[8:12])
    imagelsMain.append(ls[12:])

    for i,ii in enumerate(imagelsMain):
        for j,jj in enumerate(ii):
            if jj != None:
                x = j * IMAGE_HEIGHT + (j * 5) + 10
                y = i * IMAGE_WIDTH + (i * 5) + 10
                rect = pygame.Rect(x,y,IMAGE_WIDTH,IMAGE_HEIGHT)
                rectls.append(rect)
            else:
                rectls.append(None)

    puzzleRectList.append(rectls[0:4])
    puzzleRectList.append(rectls[4:8])
    puzzleRectList.append(rectls[8:12])
    puzzleRectList.append(rectls[12:])

    puzzleList = imagelsMain

def blitImage():
    for i,ii in enumerate(puzzleList):
        for j,jj in enumerate(ii):
            if jj == None or puzzleRectList[i][j] == None:
                pass
            else:

                screen.blit(jj,puzzleRectList[i][j])

def findClicked(pos):
    x,y = pos
    global selectedTile
    for i, ii in enumerate(puzzleRectList):

        for j, jj in enumerate(ii):
            if jj==None:
                pass

            elif jj.collidepoint(pos) == True:
                selectedTile = [i,j]
                return i,j

    return False

def checkMove(pos,move,list):
    global selectedTile
    x, y = pos

    if move == 'up' and list[x - 1][y] == None:
        puzzleRectList[x][y].y -= IMAGE_WIDTH + 5
        puzzleList[x-1][y] = puzzleList[x][y]
        puzzleRectList[x-1][y] = puzzleRectList[x][y]
        puzzleRectList[x][y] = None
        puzzleList[x][y] = None
        print(puzzleList)
        selectedTile = [x-1,y]
        return True
    elif move == 'down' and list[x + 1][y] == None:
        puzzleRectList[x][y].y += IMAGE_WIDTH + 5
        puzzleList[x+1][y] = puzzleList[x][y]
        puzzleRectList[x+1][y] = puzzleRectList[x][y]
        puzzleRectList[x][y] = None
        puzzleList[x][y] = None
        print(puzzleList)
        selectedTile = [x+1,y]
        return True
    elif move == 'left' and list[x][y-1] == None:
        puzzleRectList[x][y].x -= IMAGE_WIDTH + 5
        puzzleList[x][y-1] = puzzleList[x][y]
        puzzleRectList[x][y-1] = puzzleRectList[x][y]
        puzzleRectList[x][y] = None
        puzzleList[x][y] = None
        print(puzzleList)
        selectedTile = [x,y-1]
        return True
    elif move == 'right' and list[x][y+1] == None:
        puzzleRectList[x][y].x += IMAGE_WIDTH + 5
        puzzleList[x][y+1] = puzzleList[x][y]
        puzzleRectList[x][y+1] = puzzleRectList[x][y]
        puzzleRectList[x][y] = None
        puzzleList[x][y] = None
        print(puzzleList)
        selectedTile = [x,y+1]
        return True
    else:
        return False

def checkWin():
    if puzzleList == imageList:
        print("Won~!!!")

sliceImage(opencvImage)
print("Puzzle List=>>",puzzleList)
shuffle2dArray(imageList)
print("PuzzleRect->>",puzzleRectList)
running = True
drag = False
while running:
    clock.tick(60)
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(findClicked(event.pos))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                checkMove(selectedTile,'up',puzzleRectList)


            elif event.key == pygame.K_DOWN:

                checkMove(selectedTile,'down',puzzleRectList)

            elif event.key == pygame.K_LEFT:
                checkMove(selectedTile,'left',puzzleRectList)

            elif event.key == pygame.K_RIGHT:

                checkMove(selectedTile,'right',puzzleRectList)


    blitImage()
    checkWin()
    pygame.display.update()