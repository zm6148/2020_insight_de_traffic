import functions as fun
import os
import cv2
import numpy as np
from time import sleep
from json import dumps
from kafka import KafkaProducer
import server_name
from kafka.admin import KafkaAdminClient, NewTopic
from datetime import datetime

# connect and create camera specific topic
servers = server_name.servers
cam_ID = 'cam_2'

# connect to kafka server and produce topic
producer = KafkaProducer(bootstrap_servers=servers,
                        value_serializer=lambda x:dumps(x).encode('utf-8'))
print(producer.bootstrap_connected())

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
VIDEO_URL = 'https://s51.nysdot.skyvdn.com:443/rtplive/R11_004/playlist.m3u8'
# Camera Info
cam_name = 'I-278 at Whittier Street'
# lat
lat = 40.822477
# lon
lon = -73.885890
# facing
facing = 'south north'

# read video
cam = cv2.VideoCapture(VIDEO_URL)
#cv2.namedWindow("traffic")

while True:
    f, im = cam.read()
    
    # count objects in the frame
    image_o, class_ids = fun.object_identification(im, classes, net, output_layers, COLORS)
    #print('cars: {}'.format(class_ids.count(2)))
    #print('trucks: {}'.format(class_ids.count(7)))
    #print('person: {}'.format(class_ids.count(0)))
    #print('bicycle: {}'.format(class_ids.count(1)))
    #print('motorcycle: {}'.format(class_ids.count(3)))
    #print('bus: {}'.format(class_ids.count(5)))
    #print('dog: {}'.format(class_ids.count(16)))
    #print('horse: {}'.format(class_ids.count(17)))
    data = {'cars': class_ids.count(2),
            'trucks': class_ids.count(7),
            'person': class_ids.count(0),
            'bicycle': class_ids.count(1),
            'motorcycle': class_ids.count(3),
            'bus': class_ids.count(5),
            'vehicles': class_ids.count(2) + class_ids.count(7) + class_ids.count(3) + class_ids.count(5), 
            'cam_ID': cam_ID,
            'cam_name': cam_name,
            'lat': lat,
            'lon': lon,
            'facing': facing,
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'region': 500 
           }
    
    # send data to topic
    producer.send(cam_ID, value=data)
    print('sent')
    sleep(1)

