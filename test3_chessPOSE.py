import cv2
import numpy as np
from enum import Enum


cam = cv2.VideoCapture(0)
# Defining the dimensions of checkerboard
CHECKERBOARD = (10,7)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# Creating vector to store vectors of 3D points for each checkerboard image
objpoints = []
# Creating vector to store vectors of 2D points for each checkerboard image
imgpoints = [] 


# Defining the world coordinates for 3D points
objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
prev_img_shape = None

axis = np.float32([[3,0,0],[0,3,0],[0,0,-3]])
mtx= np.float32([[598.07385615,0,508.23020821],[0,451.52457204,309.6144548 ],[0,0,1]]) #after calibration
dist= np.float32([[ 0.03801154, -0.01150382,  0.01532702, -0.0017193,  -0.02911065]]) #after calibration

img_counter = 0

def drawAxes(img,corners,imgpts):
    def tupleOfInts(arr):
        return tuple(int(x) for x in arr)
    
    corner = tupleOfInts(corners[0].ravel())
    img =cv2.line(img,corner,tupleOfInts(imgpts[0].ravel()),(255,0,0),3)
    img =cv2.line(img,corner,tupleOfInts(imgpts[1].ravel()),(0,255,0),3)
    img =cv2.line(img,corner,tupleOfInts(imgpts[2].ravel()),(0,0,255),3)
    return img

def drawpose(images):
    
    gray = cv2.cvtColor(images,cv2.COLOR_BGR2GRAY)
    #cor_ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
    cor_ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)
    
    if cor_ret == True:
        objpoints.append(objp)
        #refining pixel coordinates for given 2d points.
        corners2 = cv2.cornerSubPix(gray, corners, (11,11),(-1,-1), criteria)
        imgpoints.append(corners2)

        #_,mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        _,rvecs,tvecs = cv2.solvePnP(objp,corners2,mtx,dist)

        imgpts,_ = cv2.projectPoints(axis,rvecs,tvecs,mtx,dist)
        images = drawAxes(images,corners2,imgpts)
        #cv2.imshow("cam_POSE", images)
        
        return images
        #cv2.destroyAllWindows()

def cam_catch():
    global img_counter
    while True:
        ret, frame = cam.read() 
        if not ret:
            print("failed to grab frame")
            continue
        
        #cv2.imshow("cam_Frame", frame)
        drawpose(frame)
        cv2.imshow("cam_FramePOSE", frame)
        
        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            cam.release()
            cv2.destroyAllWindows()

            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = "frame_{}.jpg".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1


    

if __name__ == '__main__':
    cam_catch()
    
