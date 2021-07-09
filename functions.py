import pandas as pd
import xmltodict, json
import os
from PIL import Image
from config import *
import cv2
import numpy as np

def readXml(path):

    with open(path, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
    coordinates = []
    
    object = obj.get('annotation').get('object')
    for i in object:
        coordinates.append([ (int(i.get('bndbox').get('xmin')), int(i.get('bndbox').get('ymin'))), (int(i.get('bndbox').get('xmax')), int(i.get('bndbox').get('ymax')))])
    return coordinates


def drawnBoxes(img, coordinates, color = (0, 0, 255)):
    for coordinate in coordinates:
        cv2.rectangle(img, coordinate[0], coordinate[1],color,3)  
    
    return cv2     

def calcIOU(labelCoordinates, resultCoodinates, img = None, cv2 = None, drawn = False):
    iou = []
   
    for i in range(len(labelCoordinates)):
        
        for j in range(len(resultCoodinates)):
            x1, y1, w1, h1 = labelCoordinates[i][0][0], labelCoordinates[i][0][1], labelCoordinates[i][1][0], labelCoordinates[i][1][1]
            x2, y2, w2, h2 = resultCoodinates[j][0][0], resultCoodinates[j][0][1], resultCoodinates[j][1][0], resultCoodinates[j][1][1]
            w_intersection = min(x1 + w1, x2 + w2) - max(x1, x2)
            h_intersection = min(y1 + h1, y2 + h2) - max(y1, y2)
            if w_intersection > 0 or h_intersection > 0: 
        
                I = w_intersection * h_intersection
                U = w1 * h1 + w2 * h2 - I 
                if(I / U > 0.7):
                    
                    if(drawn):
                        cv2.putText(img,f'{str(round(I/U, 2))} ',(x1,y1),cv2.QT_FONT_NORMAL,1,255)
                    iou.append([[x1, y1, w1, h1],[x2, y2, w2, h2],I / U])
    iou.sort()
    if(cv2 != None):
        return cv2, iou
    else:
        return iou
            
def writeFileInsights(labelCoordinates, resultCoodinates, iou, name):
    

    with open(f'insights_{name}.txt', 'w') as arquivo:
        arquivo.write(f'Image: {name}\n\n')
        arquivo.write(f'* Labeled items: {len(labelCoordinates)}\n')
        arquivo.write(f'* YOLO Predicted items: {len( resultCoodinates)}\n')
        arquivo.write(f'* IOU accepted count: {len(iou)}\n')
        arquivo.write(f'\n IOU accepted items: \n\n')
        for item in iou:
            arquivo.write(f'{item}\n')
        

def resultToTouple(result):
    array = []
    for i in result:
        if(i.find('(left_x') != None):
            
            if(i[i.find('(left_x'): -1].split('   ') != ['']):
                array.append( i[i.find('(left_x'): -1].replace('   ',',').replace(':,',':')
                .replace(':  ',':').replace('(left_x:','{left_x:').replace( ")",  "}" ).replace('left_x','"left_x"')
                .replace('top_y', '"top_y"').replace("width",'"width"').replace("height",'"height"').replace(": ",':')
                .replace('{',',{').replace(' ,',',') )
    
    parse =  ' '.join([str(elem) for elem in array])
    parse = f'[{parse[1:-1]}'+'}'+']'

    
    parse = json.loads(parse)
    array= []
    for i in parse:
        leftx = int(i['left_x'])
        topx = int(i['top_y'])
        width = int(i['left_x'] + i['width'])
        height = int(i['height'] + i['top_y'])
        
        array.append([   (leftx, topx) , (width,height)])
       
    return array

def readAllFileImages():
    return  [_ for _ in os.listdir(images_path) if _.endswith(img_extension)]
def readAllFileLabels():
    return  [_ for _ in os.listdir(labels_path) if _.endswith('xml')]
def readAllFileResults():
    return [_ for _ in os.listdir(results_path) if _.find('result') != -1]

def readImg(url):
   return np.asarray(Image.open(url))

def readCoordinates(url):
    return readXml(url)

def readResults(url):
    return resultToTouple(open(url,"r"))

def drawnAllFiles(imageBoxColor, resultBoxColor, iouImageDrawn = False):
    images = readAllFileImages()

    for i in images:
        img = readImg(f'{images_path}/{i}')
        coordinates = readCoordinates(  f'{labels_path}/{i.split(".")[0]}.xml'  )
        resultCoodinates = readResults( f'{results_path}/result_{i.split(".")[0]}.txt')  
        
        cv2 = drawnBoxes(img, coordinates, color = imageBoxColor)
        cv2 = drawnBoxes(img, resultCoodinates, color = resultBoxColor)

        if(iouImageDrawn):
            cv2, iou = calcIOU(labelCoordinates = coordinates, resultCoodinates = resultCoodinates, img = img, cv2 = cv2, drawn = True)
        else:
        # OR
            iou = calcIOU(labelCoordinates = coordinates, resultCoodinates = resultCoodinates)

            writeFileInsights(coordinates, resultCoodinates, iou, i.split(".")[0])
        if not os.path.isdir(output_path): 
       
            os.mkdir(output_path) 
        cv2.imwrite(f'{output_path}/draw_result_{i}', img)
