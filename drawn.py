import cv2
from config import *
from functions import *


# ....................... Especific image ..................

img = readImg('C:/Users/carlos/Documents/projetos/FAPA/results/dji_0575_quadrante2.jpg')
coordinates = readCoordinates('results/dji_0575_quadrante2.xml' )
resultCoodinates  = readResults("C:/Users/carlos/Documents/projetos/FAPA/results/result_dji_0575_quadrante2.txt")

cv2 = drawnBoxes(img, coordinates)
cv2 = drawnBoxes(img = img, coordinates = resultCoodinates, color = (0,255,0))

cv2.imwrite('output.png', img)


#  ................... All images folder

drawnAllFiles(imageBoxColor=(0,255,0), resultBoxColor=(0,255,0))
    





