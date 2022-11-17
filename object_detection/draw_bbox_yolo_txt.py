import cv2
import os
import matplotlib.pyplot as plt
import shutil
from tqdm import tqdm

def draw_bbox_yolo_txt(path_img, path_label, path_save):
    img = cv2.imread(path_img)
    dh, dw, _ = img.shape

    fl = open(path_label, 'r')
    data = fl.readlines()
    fl.close()
    if len(data) == 0:
        cv2.imwrite(path_save, img)
    else:
        for dt in data:
            # Split string to float
            _, x, y, w, h = map(float, dt.split(' '))

            l = int((x - w / 2) * dw)
            r = int((x + w / 2) * dw)
            t = int((y - h / 2) * dh)
            b = int((y + h / 2) * dh)
            
            if l < 0:
                l = 0
            if r > dw - 1:
                r = dw - 1
            if t < 0:
                t = 0
            if b > dh - 1:
                b = dh - 1

            img = cv2.rectangle(img, (l, t), (r, b), (0, 0, 255), 1)
        cv2.imwrite(path_save, img)

def main():
    path_img = 'images'
    path_label = 'labels'

    path_save = './visualize_labels'
    if os.path.exists(path_save):
        shutil.rmtree(path_save)
    os.mkdir(path_save)
   
    img_filenames = os.listdir(path_img)
    img_filenames = [filename for filename in img_filenames if filename.split('.')[-1] in ['jpg', 'png']]
    img_filenames.sort()

    label_filenames =  os.listdir(path_label)
    label_filenames = [filename for filename in label_filenames if filename.split('.')[-1] in ['txt']]
    label_filenames.sort()

    for filename in tqdm(img_filenames):
        draw_bbox_yolo_txt(os.path.join(path_img, filename), os.path.join(path_label, filename.replace('jpg', 'txt')), os.path.join(path_save, filename))
    

if __name__ == '__main__':
    main()