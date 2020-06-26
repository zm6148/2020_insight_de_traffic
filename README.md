# TrafficSense

> ***Real-time Traffic Pattern Monitoring***


I built this project in 3 weeks during Insight Data Engineering program (Boston, Summer 2020).
Visit [dataengineermz.club/](http://dataengineermz.club/) to see it in action.

## Table of Contents

1. [Usage](README.md#Usage)
1. [System](README.md#System)
1. [Setup](README.md#setup)
1. [Run the system](README.md#run-the-system)
1. [Contact Information](README.md#contact-information)

***

## Usage

This project aim to provide users the live update of traffic pattern (detailed counts of different types of veichels at major junctions). This information would be usefull to daily commuters and add to currently avalibel traffic speed data for traffic planners.

In addition to live update, this project also record historical data. 
- Historical traffic counts at all junctions (last hour, day, week).
- Detialed traffic breakdown at user selected junctions (last hour, day, week).

![Demo_gif](./img/ezgif.com-video-to-gif(1).gif)

For example the traffic condtion along I-95 in Bronx NY.

---
## System

This datapipline takes in live video streams from traffic cams and dedicates 1 computing resource (t2.medium) perfoming data extraction using comupter vision (neural net implemented in OpenCV) analysis for 4 traffic cam footages. After the data extraction stage, the extracted traffci information is feed to a Kafka data stream for temporary storage and queuing. A kafka consumenr aggregate the data and save to database. The flask front end displays the data in real-time.

![system_png](./img/ezgif.com-video-to-gif(2).gif)


---
## Setup

This pipline requires 16 AWS EC2s. [Pegasus](https://github.com/InsightDataScience/pegasus) was used to set up multiple EC2s easier.

For each EC2, clone this repository

```
git clone https://github.com/zm6148/2020_insight_de_traffic.git
```
and run the requiements.sh to install required technologies.

```
bash requirements.sh
```


## Run the system

#### Strat data analysis EC2
```
sudo python3 flask/run.py
```
#### Strat kafka consumer EC2
```
sudo python3 flask/run.py
```
#### Strat front end EC2
```
sudo python3 flask/run.py
```

## Contact Information

* [LinkedIn](https://www.linkedin.com/in/zm6148)
* mz86@njit.edu
