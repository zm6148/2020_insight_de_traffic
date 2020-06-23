from multiprocessing import Process
import functions as fun
import os
import cv2
import numpy as np
from time import sleep
from json import dumps
from kafka import KafkaProducer
#import server_name
from datetime import datetime
import cam_info
import time

# connect and create camera specific topic
#servers = server_name.servers
    
def image_processing(cam_index):
    
    # cam id
    cam_ID = cam_info.cam_IDs[cam_index]
    # Video URL
    VIDEO_URL = cam_info.VIDEO_URLs[cam_index]
    
    # Camera Info
    cam_name = cam_info.addresses[cam_index]
    # lat
    lat = cam_info.lats[cam_index]
    # lon
    lon = cam_info.lons[cam_index]
    # facing
    facing = cam_info.facings[cam_index]
    
    # connect to kafka server and produce topic
    #producer = KafkaProducer(bootstrap_servers=servers,
    #                        value_serializer=lambda x:dumps(x).encode('utf-8'))
    #print(producer.bootstrap_connected())
    
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
    cam= cv2.VideoCapture(VIDEO_URL)
    
    while True:
        
        f, im = cam.read()
        
        # count objects in the frame
        if im is not None:
            image_o, class_ids = fun.object_identification(im, classes, net, COLORS)

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
        # only if car detected
        if class_ids.count(2) + class_ids.count(7) + class_ids.count(3) + class_ids.count(5) > 0:
            #producer.send(cam_ID, value=data)
            print(cam_index)
        

if __name__ == "__main__":  # confirms that the code is under main function
    names = ['America', 'Europe', 'Africa']
    proc0 = Process(target=image_processing, args=(0,))
    proc1 = Process(target=image_processing, args=(1,))
    proc2 = Process(target=image_processing, args=(2,))
    proc3 = Process(target=image_processing, args=(3,))
    proc0.start()
    proc1.start()
    proc2.start()
    proc3.start()

