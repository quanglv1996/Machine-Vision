import shutil
from statistics import mean
import sys

from cv2 import CV_32F
sys.path.append('../.')

import cv2
import os
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
from tqdm import tqdm


def histogram_equalization(img):
    if img.shape == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
    img_his = clahe.apply(img)
    return img_his


def adjust_gamma(img):
    standard_bright = 136.01778758888764
    bright = np.mean(img)
    gamma = standard_bright / bright

    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    adj_gamma_image = cv2.LUT(img, table)  # Apply gamma correction using the lookup table
    return adj_gamma_image


def blur(img, kernel=(3,3)):
    if img.shape == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img_blur = cv2.blur(img, kernel)
    return img_blur


def rotate(img, angle=0):
    (h, w) = img.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
    img = cv2.warpAffine(img, M, (w, h))
    return img


def canny(img, min=100, max=200):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.Canny(img,min, max)
    return img


def gray2bgr(img):
    if len(img.shape) == 3:
        return img
    img = img.astype(np.uint8)
    bgr_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    return bgr_img


def gray2binary(gray_img, threshold=127):
    _, binary_img = cv2.threshold(gray_img, threshold, 255, cv2.THRESH_BINARY)
    binary_img = binary_img.astype(np.uint8)
    return binary_img


def bgr2rgb(img):
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return rgb_img


def resize(img, w=1920, h=1080, interpolation=cv2.INTER_AREA):
    img_resize = cv2.resize(img, (w, h), interpolation=interpolation)
    return img_resize


def padding_square(img):
    if len(img.shape) == 3:
        h, w = img.shape[:2]
        if h>w:
            offset = h - w
            padding = offset//2
            img_pad = np.zeros((h, h, 3))
            img_pad[:, padding:padding+w, :] = img
            return img_pad
        elif h<w:
            offset = w - h
            padding = offset//2
            img_pad = np.zeros((w, w, 3))
            img_pad[padding:padding+h, :, :] = img
            return img_pad
        else:
            return img
    else:
        h, w = img.shape[:2]
        if h>w:
            offset = h - w
            padding = offset//2
            img_pad = np.zeros((h, h))
            img_pad[:, padding:padding+w] = img
            return img_pad
        elif h<w:
            offset = w - h
            padding = offset//2
            img_pad = np.zeros((w, w))
            img_pad[padding:padding+h, :] = img
            return img_pad
        else:
            return img
        

def opening(img, kernel=(3,3)):
    img_open = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    return img_open


def closing(img, kernel=(3,3)):
    img_close = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    return img_close


def dilation (img, kernel=(3,3), iterations=5):
    img_dilation= cv2.dilate(img, kernel,iterations=iterations)
    return img_dilation


def erosion (img, kernel=(3,3), iterations=5):
    img_Erosion= cv2.erode(img,kernel,iterations = iterations)
    return img_Erosion


def create_histogram_image(img, save_filename='debug.jpg', show=False):
    if len(img.shape) == 3:
        color = ('b', 'g', 'r')
        for i,col in enumerate(color):
            histr = cv2.calcHist([img],[i],None,[256],[0,256])
            plt.plot(histr,color = col)
            plt.xlim([0,256])
        plt.savefig(save_filename)
        if show:
            plt.show()
        plt.close()
    if len(img.shape) == 2:
        plt.hist(img.ravel(),256,[0,256])
        plt.savefig(save_filename)
        if show:
            plt.show()
        plt.close()



def main():
    save_dir = './debug'
    if os.path.exists(save_dir):
        shutil.rmtree(save_dir)
    os.mkdir(save_dir)
    filename = './asset/1.jpg'
    img = cv2.imread(filename)
    create_histogram_image(img, os.path.join(save_dir, filename), True)
    # img_pad = padding_square(img)
    # cv2.imwrite(os.path.join(save_dir, filename), open_cv_image)
    


if __name__ == '__main__':
    main()