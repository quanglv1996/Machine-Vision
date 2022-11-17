import os
import glob
import shutil
from tkinter import E
import xml.etree.cElementTree as ET
import cv2

class LabelCreating(object):
    def __init__(self, class_mapping):
        self.class_mapping = class_mapping

    @staticmethod
    def yolo_to_cor(box, w, h):
        x1, y1 = int((box[0] - box[2]/2)*w), int((box[1] - box[3]/2)*h)
        x2, y2 = int((box[0] + box[2]/2)*w), int((box[1] + box[3]/2)*h)
        return abs(x1), abs(y1), abs(x2), abs(y2)

    def create_label_from_txt(self, path_img, path_txt, path_save):
        # Read img get w, h image
        img = cv2.imread(path_img)
        h, w = img.shape[:2]

        # Read file txt yolo format
        with open(path_txt, 'r') as file:
            lines = file.readlines()
            voc_labels = []
            for line in lines:
                voc = []
                line = line.strip()
                elems = line.split(' ')
                if (len(elems)<=4):
                    continue
                try:
                    id = int(elems[0])
                    box=list(map(float, elems[1:5]))
                except ValueError as e:
                    print (e)    
                voc.append(self.class_mapping.get(id))
                x1, y1, x2, y2 = self.yolo_to_cor(box, w, h)
                voc.append(x1)
                voc.append(y1)
                voc.append(x2)
                voc.append(y2)
                voc_labels.append(voc)
        
        '''
        Create file xml
        '''
        # Create root
        root = ET.Element("annotations")
        ET.SubElement(root, "filename").text = path_img
        ET.SubElement(root, "folder").text = "images"
        size = ET.SubElement(root, "size")
        ET.SubElement(size, "width").text = str(w)
        ET.SubElement(size, "height").text = str(h)
        ET.SubElement(size, "depth").text = "3"

        # Create object annotations
        for voc_label in voc_labels:
            obj = ET.SubElement(root, "object")
            ET.SubElement(obj, "name").text = voc_label[0]
            ET.SubElement(obj, "pose").text = "Unspecified"
            ET.SubElement(obj, "truncated").text = str(0)
            ET.SubElement(obj, "difficult").text = str(0)
            bbox = ET.SubElement(obj, "bndbox")
            ET.SubElement(bbox, "xmin").text = str(voc_label[1])
            ET.SubElement(bbox, "ymin").text = str(voc_label[2])
            ET.SubElement(bbox, "xmax").text = str(voc_label[3])
            ET.SubElement(bbox, "ymax").text = str(voc_label[4])

        # Create xml tree
        tree = ET.ElementTree(root)
        out_path = "{}/{}.xml".format(path_save, os.path.basename(path_img).split('.')[0])
        tree.write(out_path)

    def create_label_from_res(self, res, img):
        pass 

def main():
    # Test create label from txt file
    img_dir = './img'
    txt_dir = './txt'
    save_dir = './label'
    if os.path.exists(save_dir):
        shutil.rmtree(save_dir)
    os.mkdir(save_dir)

    class_mapping = {
        0: 'solder',
    }

    label_creator = LabelCreating(class_mapping=class_mapping)
    img_filenames = os.listdir(img_dir)

    for filename_img in img_filenames:
        path_img = os.path.join(img_dir, filename_img)
        path_txt = os.path.join(txt_dir, '{}.txt'.format(filename_img.split('.')[0]))
        
        label_creator.create_label_from_txt(path_img=path_img, path_txt=path_txt, path_save=save_dir)


if __name__ == '__main__':
    main()