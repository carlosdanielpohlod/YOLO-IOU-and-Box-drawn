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

def drawnAllFiles(imageBoxColor, resultBoxColor):
    images = readAllFileImages()

    for i in images:
        img = readImg(f'{images_path}/{i}')
        coordinates = readCoordinates(  f'{labels_path}/{i.split(".")[0]}.xml'  )
        resultCoodinates = readResults( f'{results_path}/result_{i.split(".")[0]}.txt')  
        
        cv2 = drawnBoxes(img, coordinates, color = imageBoxColor)
        cv2 = drawnBoxes(img, resultCoodinates, color = resultBoxColor)

        cv2.imwrite(f'{output_path}/draw_result_{i}', img)