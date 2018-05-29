import re
import cv2
from pprint import pprint
import numpy as np


def read_file(path_to_file):
    imgname = ""
    positions = []
    metadata_list = []
    position_pattern = re.compile("\d+ \d+ \d+ \d+ [012] [01] [01] [01] [012] [01]")

    with open(path_to_file) as f:
        for line in f:
            if line.endswith("jpg\n"):
                if(imgname != "" and len(positions) != 0):
                    metadata = {"imgname" : imgname , "positions" : positions}
                    metadata_list.append(metadata)
                    positions = []
                imgname = line.strip()
            
            elif (position_pattern.match(line)):
                 values = line.split(" ")
                 dimension = {
                    "x" : int(values[0]) , 
                    "y" : int(values[1]) , 
                    "width" : int(values[2]) , 
                    "height" : int(values[3])
                 }
                 positions.append(dimension)
        
        if(imgname != "" and len(positions) != 0):
            metadata = {"imgname" : imgname , "positions" : positions}
            positions = []
            metadata_list.append(metadata)
            imgname = line.strip()    
        
    return metadata_list


def gen_load_imgs(path_to_file):
    metadata_list = read_file(path_to_file)
    print("[Total image count:]", len(metadata_list))
    
    for metadata in metadata_list:
        path = metadata.get("imgname", None)
        
        if (path != None):
            path = "Data/" + path
            #print(path)
        
        img = cv2.imread(path, 1)
        img_with_metadata = {"img" : img , "positions" : metadata.get("positions")}
        
        yield img_with_metadata

def load_resized_imgs(path_to_file, size):
    imgs = gen_load_imgs(path_to_file)

    for img in imgs:
        image = img.get("img", None)

        height = np.size(image, 0)
        width = np.size(image, 1)
        scalefactor_width = size / width
        scalefactor_height = size / height

        image = cv2.resize(image, (size,size))

        scaled_img = {"img" : image, "positions": img.get("positions"), "sfw" : scalefactor_width, "sfh" : scalefactor_height }
        yield scaled_img

def visualize_resized_imgs(path_to_file, size):
    imgs = load_resized_imgs(path_to_file, size)

    for img in imgs:
        positions = img.get("positions", [])
        sfw = img.get("sfw", 1)
        sfh = img.get("sfh", 1)

        if (positions != None):
            for p in positions:
                x = p.get("x") * sfw
                y = p.get("y") * sfh
                w = p.get("width") * sfw
                h = p.get("height") * sfh

                cv2.rectangle(
                    img.get("img"),
                    (int(x), int(y)),
                    (int(x+w), int(y+h)),
                    (0,255,0)
                )    

        print(type(img.get("img")))
        print(img.get("img").shape)
        cv2.imshow("resized image", img.get("img"))
        cv2.waitKey(1000)