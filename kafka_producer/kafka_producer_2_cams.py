import functions as fun
import os
import cv2
import numpy as np
from time import sleep
from json import dumps
from kafka import KafkaProducer
import server_name
from datetime import datetime
import cam_info

# connect and create camera specific topic
servers = server_name.servers

# index of those two cams
cam_index_1 = 0
cam_index_2 = 1

# cam id
cam_ID_1 = cam_info.cam_IDs[cam_index_1]
cam_ID_2 = cam_info.cam_IDs[cam_index_2]

# Video URL
VIDEO_URL_1 = cam_info.VIDEO_URLs[cam_index_1]
VIDEO_URL_2 = cam_info.VIDEO_URLs[cam_index_2]

# Camera Info
cam_name_1 = cam_info.addresses[cam_index_1]
cam_name_2 = cam_info.addresses[cam_index_2]
# lat
lat_1 = cam_info.lats[cam_index_1]
lat_2 = cam_info.lats[cam_index_2]
# lon
lon_1 = cam_info.lons[cam_index_1]
lon_2 = cam_info.lons[cam_index_2]
# facing
facing_1 = cam_info.facings[cam_index_1]
facing_2 = cam_info.facings[cam_index_2]

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

# read video
cam_1= cv2.VideoCapture(VIDEO_URL_1)
cam_2= cv2.VideoCapture(VIDEO_URL_2)

cv2.namedWindow("traffic1")
cv2.namedWindow("traffic2")

while True:
    
    f_1, im_1 = cam_1.read()
    f_2, im_2= cam_2.read()
    
    # count objects in the frame
    if im_1 is not None:
        image_o_1, class_ids_1 = fun.object_identification(im_1, classes, net, output_layers, COLORS)
    if im_2 is not None:
        image_o_2, class_ids_2 = fun.object_identification(im_2, classes, net, output_layers, COLORS)

    data_1 = {'cars': class_ids_1.count(2),
            'trucks': class_ids_1.count(7),
            'person': class_ids_1.count(0),
            'bicycle': class_ids_1.count(1),
            'motorcycle': class_ids_1.count(3),
            'bus': class_ids_1.count(5),
            'vehicles': class_ids_1.count(2) + class_ids_1.count(7) + class_ids_1.count(3) + class_ids_1.count(5),
            'cam_ID': cam_ID_1,
            'cam_name': cam_name_1,
            'lat': lat_1,
            'lon': lon_1,
            'facing': facing_1,
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'region': 500 
           }
           
    data_2 = {'cars': class_ids_2.count(2),
            'trucks': class_ids_2.count(7),
            'person': class_ids_2.count(0),
            'bicycle': class_ids_2.count(1),
            'motorcycle': class_ids_2.count(3),
            'bus': class_ids_2.count(5),
            'vehicles': class_ids_2.count(2) + class_ids_2.count(7) + class_ids_2.count(3) + class_ids_2.count(5),
            'cam_ID': cam_ID_2,
            'cam_name': cam_name_2,
            'lat': lat_2,
            'lon': lon_2,
            'facing': facing_2,
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'region': 500 
           }
    
    # Display the resulting frame
    # cv2.imshow('traffic1',image_o_1)
    # cv2.imshow('traffic2',image_o_2)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

    # send data to topic
    # only if car detected
    if class_ids_1.count(2) + class_ids_1.count(7) + class_ids_1.count(3) + class_ids_1.count(5) > 0:
        producer.send(cam_ID_1, value=data_1)
    print('sent 1')
    if class_ids_2.count(2) + class_ids_2.count(7) + class_ids_2.count(3) + class_ids_2.count(5) > 0:
        producer.send(cam_ID_2, value=data_2)
    print('sent 2')
    #sleep(1)
