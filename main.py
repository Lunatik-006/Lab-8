import time
import cv2

def image_processing(): #Задание 1
    image = cv2.cvtColor(cv2.imread("variant-10.jpg"), cv2.COLOR_BGR2GRAY)
    ret, threshold_image = cv2.threshold(image, 150, 255, 0)
    cv2.imshow("Old Car 150", threshold_image)

def add_fly(background,i,j):
    overlay = cv2.imread('fly64.png', cv2.IMREAD_COLOR)
    h, w = overlay.shape[:2]
    x=i-(h//2)
    y=j-(w//2)
    result = cv2.addWeighted(background[x:x+h, y:y+w], 0.4, overlay, 0.5, 0)
    background[x:x+h, y:y+w] = result
    return background

def video_processing(): #Задание 2 и 3
    cap = cv2.VideoCapture("sample.mp4")
    down_points = (640, 480)
    i = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.resize(frame, down_points, interpolation=cv2.INTER_LINEAR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #gray = cv2.GaussianBlur(gray, (21, 21), 0)
        ret, thresh = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY_INV)
        M = cv2.getRotationMatrix2D((320, 240), 180, 1.0)

        contours, hierarchy = cv2.findContours(thresh,
                            cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            a = x + (w // 2)
            b = y + (h // 2)

            frame=add_fly(frame, b, a) #adding fly

            if (a in range(245,395,1)) and (b in range(165,315,1)): 
                flip=True
            else: 
                flip=False

        if flip:
            frame = cv2.warpAffine(frame, M, (640, 480))

        cv2.imshow('frame', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):   
            break

        time.sleep(0.1)
        i += 1
    cap.release()

if __name__ == '__main__':
    #image_processing()
    video_processing()

cv2.waitKey(0)
cv2.destroyAllWindows()