import pygame
import pygame.camera
from pygame.locals import *
import time
import os

# initialize
pygame.init()
pygame.camera.init()

# capture a image
camera = pygame.camera.Camera("/dev/video0", (640, 480))

camera.start()
num = 0
while True:
    if (not os.listdir(r"/home/pi/project/data/test_data/normal")):
        image = camera.get_image()
        pygame.image.save(image, r"/home/pi/project/data/test_data/normal/image"+str(num)+".jpg")
        print('save the image',num)
        #pygame.image.save(image, r"../data/test_data/open/image"+str(num+1)+".jpg")
        #print('save the image',num+1)
        time.sleep(4)
        num+=1
print('close')
camera.stop()