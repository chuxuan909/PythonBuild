import pyautogui
import time
import base64
import cv2
import numpy as np
time.sleep(5)
region_info=[1652,599,50,45]


def screenshot_do(num,*region_infos):
    img = pyautogui.screenshot(region=region_infos[0])
    img.save('screenshot_%s.png' % num)
    
def checks():
    for i in range(2):
        time.sleep(2)
        screenshot_do(i,region_info)
    image1 = cv2.imread("screenshot_0.png")
    image2 = cv2.imread("screenshot_1.png")
    difference = cv2.subtract(image1, image2)
    result = not np.any(difference) #if difference is all zeros it will return False

    if result is True:
        #print("两张图片一样")
        return 1
    else:
        return 2
        #cv2.imwrite("result.jpg", difference)
        #print ("两张图片不一样")

def main():
    flags_num=0
    for j in range(5):
        flags=checks()
        print(flags)
        if flags==1:
            flags_num=flags_num+1
    if flags_num > 4:
        print("WARING!!!")
    else:
        print("OK")

main()
    
        


