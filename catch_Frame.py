import cv2

#cam = cv2.VideoCapture("rtsp://root:01670@172.18.40.61:554/axis-media/media.amp")
cam = cv2.VideoCapture(0)

cv2.namedWindow("catch_Frame")

img_counter = 0

def cam_cat():
    global img_counter
    while True:
        ret, frame = cam.read() 
        if not ret:
            print("failed to grab frame")
            continue
        
        frame = cv2.resize(frame, (1024, 576), interpolation=cv2.INTER_AREA)
        cv2.imshow("catch_Frame", frame)


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

#cam.release()
#cv2.destroyAllWindows()


if __name__ == '__main__':
    cam_cat()
    
    


