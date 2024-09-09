from pathlib import Path
from pytube import YouTube
import cv2
import os
import math

def create_images(vid, n_images = 50, n_same_images = 1, frametake = 10):
    imgpath = Path('images')
    imgpath.mkdir(exist_ok=True)

    cap = cv2.VideoCapture(vid)

    count = 1 # choosing 0 will result in integer modulo by zero
    i_n = 1 # to align with count more accurately
    while cap.isOpened():
        success, image = cap.read()
        if success and count <= (frametake * n_images): # take n_images images from video, count starts as 1
            if count % frametake == 0:
                for i in range(n_same_images): # take n_same_images of the same image
                    cv2.imwrite(os.path.join('images', '{}_{}.png'.format(i_n, i)), image)
                i_n += 1
            count += 1
        else:
            break

create_images('vid.mp4')