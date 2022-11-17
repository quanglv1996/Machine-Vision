import numpy as np
import cv2
import time
import pickle

class ExportCalibrationConfig(object):
    def __init__(self, width=1280, height=720, path_save_config='../assets/calibration.pkl'):
        self.NUM_X = 7
        self.NUM_Y = 6
        self.TIMES = 20
        # termination criteria
        self.criteria  = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        self.objp = np.zeros((self.NUM_X*self.NUM_Y,3), np.float32)
        self.objp[:,:2] = np.mgrid[0:self.NUM_Y,0:self.NUM_X].T.reshape(-1,2)
        # Arrays to store object points and image points from all the images.
        self.objpoints = [] # 3d point in real world space
        self.imgpoints = [] # 2d points in image plane.
        
        # Set camera
        self.width = width
        self.height = height
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        
        self.gray, self.mtx, self.dist, self.rvecs, self.tvecs = None, None, None, None, None
        
        self.count = 0
        self.path_save_config = path_save_config

    def calibrate(self):
        while True:
            _, img = self.cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, (self.NUM_Y,self.NUM_X), None)
            # If found, add object points, image points (after refining them)
            if ret == True:
                self.objpoints.append(self.objp)
                corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), self.criteria)
                self.imgpoints.append(corners)
                # Draw and display the corners
                cv2.drawChessboardCorners(img, (self.NUM_Y,self.NUM_X), corners2, ret)
                self.count +=1
                time.sleep(0.1)
                print('Progress: {}%'.format(int((self.count/self.TIMES)*100)))
                if self.count == 20:
                    self.gray = gray
                    break
            cv2.imshow('calibration', img)
            cv2.waitKey(100)
            
        config_calibration = [self.objpoints, self.imgpoints, gray]
        with open(self.path_save_config, 'wb') as f:
            pickle.dump(config_calibration,f)
        
        self.ret, self.mtx, self.dist, self.rvecs, self.tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints, self.gray.shape[::-1], None, None)
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(self.mtx, self.dist, (self.width,self.height), 1, (self.width,self.height))
        while True:
            _, img = self.cap.read()
            stime = time.time()
            dst = cv2.undistort(img, self.mtx, self.dist, None, newcameramtx)
            print('Time: {}'.format(time.time()-stime))
            x, y, w, h = roi
            dst = dst[y:y+h, x:x+w]
            cv2.imshow('img_calibrated', dst)
            cv2.waitKey(100)
        cv2.destroyAllWindows()
        
def main():
    pass

if __name__ == '__main__':
    main()