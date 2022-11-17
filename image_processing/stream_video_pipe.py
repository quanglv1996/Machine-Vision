import numpy as np
import time
import cv2
import os
import subprocess
import argparse
import threading
import time
from collections import deque

VIDEO_PATH = os.path.join('test.avi')

# Resolution, FPS
path_rtsp = 'rtsp://path/stream'
cap =  cv2.VideoCapture(path_rtsp)

#----- Save video ------
fourcc = cv2.VideoWriter_fourcc(*'XVID')
size = (4096,2160)
fps = 12
out = cv2.VideoWriter(VIDEO_PATH, fourcc, fps, size)

data_queue = []

class ImageGraber(threading.Thread):
	def __init__(self, cap):
		threading.Thread.__init__(self)
		self.cap = cap
	
	def run(self):
		global grab
		global data_queue
		if not self.cap.isOpened():
			print("Camera not available")
			cap.release()
			return
		while grab:
			time.sleep(0.001)
			ret, frame = self.cap.read()
			if ret == False:
				continue
			data_queue.append(frame)
			print("Queue len: {}".format(len(data_queue)))
		cap.release()

class ImageWriter(threading.Thread):
	def __init__(self, out):
		threading.Thread.__init__(self)
		self.out = out

	def run(self):
		global grab
		global data_queue
		while len(data_queue) > 0 or grab:
			if len(data_queue) > 0:
				frame = data_queue[0]
				print(frame.shape)
				del data_queue[0]
				out.write(frame)
		out.release()
		cv2.destroyAllWindows()
		print("Finishing writing")

if __name__ == "__main__":
	grab = True
	image_graber = ImageGraber(cap)
	image_writer = ImageWriter(out)
	image_graber.start()
	image_writer.start()