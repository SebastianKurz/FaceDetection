import re
import cv2
from pprint import pprint


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
    
    for metadata in metadata_list:
        path = metadata.get("imgname", None)
        
        if (path != None):
            path = "Data/" + path
            #print(path)
        
        img = cv2.imread(path, 1)
        img_with_metadata = {"img" : img , "positions" : metadata.get("positions")}
        
        yield img_with_metadata

# test
"""
for img in gen_load_imgs("Data/wider_face_train_bbx_gt.txt"):
    pic = img.get("img" , None)
    if (pic != None):
        cv2.imshow("image" , pic)
        cv2.waitKey(100)
        cv2.destroyAllWindows()
    
    positions = img.get("positions")
    pprint(positions)
"""
