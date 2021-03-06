#!bin/bash
#cmake
#dlib
#face_recognition
#numpy
#opencv-python

#steps for insitialize opencv node:
sudo apt-get update
sudo apt-get install python3-pip
pip3 install cmake

sudo apt-get install build-essential cmake pkg-config
sudo apt-get install -y libsm6 libxext6 libxrender-dev

pip3 install dlib
pip3 install face_recognition
pip3 install numpy
pip3 install opencv-python

#install python kafka:
pip3 install kafka-python

#clone from my git
#git clone clone https://github.com/zm6148/2020_insight_de_traffic.git

#trained yolo weights:
cd 2020_insight_de_traffic/kafka_producer/yolo_model
wget https://pjreddie.com/media/files/yolov3.weights

#dash requirements
pip3 install dash
pip3 install dash-renderer
pip3 install dash-html-components
pip3 install dash-core-components
pip3 install plotly --upgrade
pip3 install plotly-express

