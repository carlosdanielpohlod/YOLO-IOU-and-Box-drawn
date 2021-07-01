import cv2
from config import *
from functions import *


# ....................... Especific image ..................

img = readImg('C:/image.jpg')
coordinates = readCoordinates('C:/image.xml' )
resultCoodinates  = readResults("C:/result_image.txt")

cv2 = drawnBoxes(img, coordinates)
cv2 = drawnBoxes(img = img, coordinates = resultCoodinates, color = (0,255,0))

cv2.imwrite('output.png', img)


#  ................... All images folder

drawnAllFiles(imageBoxColor=(0,255,0), resultBoxColor=(0,255,0))
    





