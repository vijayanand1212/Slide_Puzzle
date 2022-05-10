import cv2
import random
import os
import pygame
import numpy
import pickle
from Tile import Tile


imagesPath = []
completedImagesPath = []
slicedImage = []
slicedImage1d = []
slicedPuzzleImage = []
slicedPuzzleImage1d = []
slicedImageSize = int(input("Enter Tile Size: "))
inversions = 0
SCREEN_SIZE = 600
selectedTile = []
col = int(SCREEN_SIZE / slicedImageSize)
imagepath = ""
moves = 0

# Pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_SIZE + col*10, SCREEN_SIZE + col*10))
pygame.display.set_caption("Slide Puzzle")
icon = pygame.image.load(r'./icon.png')
pygame.display.set_icon(icon)

def get_images(path):
    for filename in os.listdir(path):
        imagesPath.append(os.path.join(path, filename))


def getinversions(board):
    inversions = 0
    for i, ii in enumerate(slicedImage1d):
        for j, jj in enumerate(slicedImage1d):
            if jj == None or ii == None:
                pass
            elif ii.tileNumber > jj.tileNumber and i < j:
                inversions += 1
    return inversions


def makeBoard(image_size, board_size):
    # Making essentials
    global col
    col = int(SCREEN_SIZE / slicedImageSize)
    image = cv2.imread(imagepath)
    image = cv2.resize(image,(SCREEN_SIZE,SCREEN_SIZE))
    # Slicing the Image
    global slicedImage, slicedImage1d
    tileNumber = 0
    for i in range(0, col):
        imageRow = []
        for j in range(0, col):
            tileNumber += 1
            imageCrop = image[i * slicedImageSize: (i + 1) * slicedImageSize,
                        j * slicedImageSize:(j + 1) * slicedImageSize]
            pyImage = pygame.image.frombuffer(imageCrop.tobytes(), imageCrop.shape[1::-1], 'BGR')
            x = j * slicedImageSize + (j * 5) + 10
            y = i * slicedImageSize + (i * 5) + 10
            rect = pygame.Rect(x, y, slicedImageSize, slicedImageSize)
            tile = Tile(pyImage, rect, [i, j], slicedImageSize, tileNumber)
            imageRow.append(tile)
            slicedImage1d.append(tile)
        slicedImage.append(imageRow)
    global imageLastPiece
    slicedImage1d = slicedImage1d[:-1]
    slicedImage1d.append(None)
    imageListL = slicedImage.pop(-1)
    imageLastPiece = imageListL[-1]
    imageListL = imageListL[:-1]
    imageListL.append(None)
    slicedImage.append(imageListL)

    # Making Correct Shuffled Board
    global inversions,slicedPuzzleImage,slicedPuzzleImage1d
    puzzleCreated = False
    while puzzleCreated == False:


        if col % 2 == 0:
            ls = slicedImage1d
            random.shuffle(ls)
            inversions = getinversions(ls)

            NoneIndex = 0
            for i, ii in enumerate(ls):
                if ii == None:
                    NoneIndex = i // col


            NoneIndex = (col - NoneIndex)


            if NoneIndex % 2 == 0 and inversions % 2 != 0:
                puzzleCreated = True
                slicedPuzzleImage1d = ls
            elif NoneIndex % 2 != 0 and inversions % 2 == 0:
                puzzleCreated = True
                slicedPuzzleImage1d = ls
            else:
                puzzleCreated = False

        else:
            ls = slicedImage1d
            random.shuffle(ls)
            inversions = getinversions(ls)
            if inversions % 2 == 0:
                puzzleCreated = True
                slicedPuzzleImage1d = ls
            else:
                puzzleCreated = False



    nparray = numpy.array(slicedPuzzleImage1d)
    nparray = nparray.reshape(col, col)
    slicedPuzzleImage = list(nparray)

    # Change rectangle pos in Tile Object
    for i, ii in enumerate(slicedPuzzleImage):
        for j, jj in enumerate(ii):
            if jj == None:
                pass
            else:
                x = j * slicedImageSize + (j * 5) + 10
                y = i * slicedImageSize + (i * 5) + 10
                rect = pygame.Rect(x, y, slicedImageSize, slicedImageSize)
                jj.rectangle = rect


def blitImages():
    for i, ii in enumerate(slicedPuzzleImage):
        for j, jj in enumerate(ii):
            if jj == None:
                pass
            else:
                screen.blit(jj.image, jj.rectangle)


def findClicked(pos):
    x, y = pos
    global selectedTile
    for i, ii in enumerate(slicedPuzzleImage):

        for j, jj in enumerate(ii):
            if jj == None:
                pass

            elif jj.rectangle.collidepoint(pos) == True:
                selectedTile = [i, j]
                return i, j

    return False


def checkMove(pos, move, list):
    global selectedTile,moves
    if len(selectedTile) == 2:
        x, y = selectedTile

        if (x - 1 < col and x - 1 >= 0) and (move == 'up' and list[x - 1][y] == None):
            slicedPuzzleImage[x][y].rectangle.y -= slicedImageSize + 5
            slicedPuzzleImage[x][y].pos = [x - 1, y]
            slicedPuzzleImage[x - 1][y] = slicedPuzzleImage[x][y]
            slicedPuzzleImage[x][y] = None
            selectedTile = [x - 1, y]
            moves +=1
            return True
        if (x + 1 < col) and (move == 'down' and list[x + 1][y] == None):
            slicedPuzzleImage[x][y].rectangle.y += slicedImageSize + 5
            slicedPuzzleImage[x][y].pos = [x + 1, y]
            slicedPuzzleImage[x + 1][y] = slicedPuzzleImage[x][y]
            slicedPuzzleImage[x][y] = None
            selectedTile = [x + 1, y]
            moves += 1
            return True
        elif (y - 1 < col and y - 1 >= 0) and move == 'left' and list[x][y - 1] == None:
            slicedPuzzleImage[x][y].rectangle.x -= slicedImageSize + 5
            slicedPuzzleImage[x][y].pos = [x, y - 1]
            slicedPuzzleImage[x][y - 1] = slicedPuzzleImage[x][y]
            slicedPuzzleImage[x][y] = None
            selectedTile = [x, y - 1]
            moves += 1
            return True
        elif (y + 1 < col) and (move == 'right' and list[x][y + 1] == None):
            slicedPuzzleImage[x][y].rectangle.x += slicedImageSize + 5
            slicedPuzzleImage[x][y].pos = [x, y + 1]
            slicedPuzzleImage[x][y + 1] = slicedPuzzleImage[x][y]
            slicedPuzzleImage[x][y] = None
            selectedTile = [x, y + 1]
            moves += 1
            return True


def checkWin():
    Won = True
    for i in range(col):
        for j in range(col):

            if slicedPuzzleImage[i][j] == None or slicedImage[i][j] == None:
                if slicedPuzzleImage[i][j] != slicedImage[i][j]:
                    Won = False
            else:
                if slicedPuzzleImage[i][j].pos == slicedImage[i][j].pos:
                    Won = True
                else:
                    Won = False
                    return Won

    return Won


def newGame():

    global slicedImage, slicedImage1d, slicedPuzzleImage, slicedPuzzleImage1d,imagepath,completedImagesPath,moves
    moves = 0
    slicedImage = []
    slicedImage1d = []
    slicedPuzzleImage = []
    slicedPuzzleImage1d = []

    if os.path.exists('./completed.pickle'):
        completedImagesPath = pickle.load(open('completed.pickle','rb'))
    else:
        completedImagesPath = []
    if len(os.listdir('./images')) <= len(completedImagesPath):
        completedImagesPath = []
        pickle.dump(completedImagesPath, open('completed.pickle', 'wb'))
    for i,ii in enumerate(imagesPath):
        if ii not in completedImagesPath:
            imagepath = imagesPath[i]
            break

    makeBoard(slicedImageSize, SCREEN_SIZE)
    print("Inversions=>", inversions)


get_images('D:\MyProjects\PYTHON\SlidePuzzle\images')
newGame()
moving = False
running = True
drag = False
while running:

    clock.tick(60)
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("Clicked Tile",findClicked(event.pos))
        if event.type == pygame.KEYDOWN:

            if moving == False:
                if event.key == pygame.K_UP:
                    moving = True
                    checkMove(selectedTile, 'up', slicedPuzzleImage)
                elif event.key == pygame.K_DOWN:
                    moving = True
                    checkMove(selectedTile, 'down', slicedPuzzleImage)
                elif event.key == pygame.K_LEFT:
                    moving = True
                    checkMove(selectedTile, 'left', slicedPuzzleImage)

                elif event.key == pygame.K_RIGHT:
                    moving = True
                    checkMove(selectedTile, 'right', slicedPuzzleImage)
        if event.type == pygame.KEYUP:
            moving = False
            if checkWin():

                slicedPuzzleImage[col-1][col-1] = imageLastPiece
                print("Wonnnnn!,Completed In",moves)
                screen.fill((255, 0, 0))

                blitImages()
                pygame.display.update()
                completedImagesPath.append(imagepath)
                pickle.dump(completedImagesPath,open('completed.pickle','wb'))
                pygame.time.wait(3*1000)
                newGame()

    blitImages()

    pygame.display.update()
