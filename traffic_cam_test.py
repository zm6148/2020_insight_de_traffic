import functions as fun
import os
import cv2
import numpy as np

# current script path
scripty_path = os.path.dirname(os.path.realpath(__file__))

# config yolo model
config_path = scripty_path + '/yolo_model/yolov3.cfg'
weight_path = scripty_path + '/yolo_model/yolov3.weights'
class_path = scripty_path + '/yolo_model/yolov3.txt'
# build net
net = cv2.dnn.readNet(weight_path, config_path)
# build output layer
output_layers = fun.get_output_layers(net)

# define classes
classes = None
with open(class_path, 'r') as f:
    classes = [line.strip() for line in f.readlines()]
# pre-define color scheme
COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

# Video URL
VIDEO_URL = "https://s52.nysdot.skyvdn.com:443/rtplive/R11_018/playlist.m3u8"
# Camera Info
# lan
# lat
# address name
# facing

cam = cv2.VideoCapture(VIDEO_URL)
cv2.namedWindow("traffic")

while True:
    f, im = cam.read()
    
    # Our operations on the frame come here
    image_o, class_ids = fun.object_identification(im, classes, net, output_layers, COLORS)
    print('cars: {}'.format(class_ids.count(2)))
    print('trucks: {}'.format(class_ids.count(7)))
    print('person: {}'.format(class_ids.count(0)))
    print('bicycle: {}'.format(class_ids.count(1)))
    print('motorcycle: {}'.format(class_ids.count(3)))
    print('bus: {}'.format(class_ids.count(5)))
    print('dog: {}'.format(class_ids.count(16)))
    print('horse: {}'.format(class_ids.count(17)))
    
    # Display the resulting frame
    # cv2.imshow('traffic',image_o)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
cam.release()
cv2.destroyAllWindows()