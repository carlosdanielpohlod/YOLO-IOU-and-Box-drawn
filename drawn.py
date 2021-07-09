import cv2
from config import *
from functions import *


# ....................... Especific image ..................

# img = readImg('C:/Users/carlos/Documents/projetos/FAPA/results/dji_0575_quadrante2.jpg')
# coordinates = readCoordinates('results/dji_0575_quadrante2.xml' )
# resultCoodinates  = readResults("C:/Users/carlos/Documents/projetos/FAPA/results/result_dji_0575_quadrante2.txt")

# cv2 = drawnBoxes(img, coordinates, (0,0,255))
# cv2 = drawnBoxes(img = img, coordinates = resultCoodinates, color = (0,255,0))

# #Calc IOU and dranw on the image
# cv2, iou = calcIOU(labelCoordinates = coordinates, resultCoodinates = resultCoodinates, img = img, cv2 = cv2, drawn = True)
# # OR
# iou = calcIOU(labelCoordinates = coordinates, resultCoodinates = resultCoodinates)

# writeFileInsights(coordinates, resultCoodinates, iou, 'dji_0575_quadrante2')

# cv2.imwrite('output.png', img)


#  ................... All images folder

drawnAllFiles(imageBoxColor=(0,0,255), resultBoxColor=(0,255,0), iouImageDrawn = True)
    





