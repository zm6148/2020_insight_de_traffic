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

For each EC2, clone this repository and run the 
### Cluster Structure:

- (4 nodes) Spark Cluster - Batch & Airflow
- (1 node) PostgreSQL
- (1 node) Flask

```
peg up ./cluster_configs/spark/master.yml
peg up ./cluster_configs/spark/worker.yml
peg up ./cluster_configs/post_node.yml
peg up ./cluster_configs/flask_node.yml
```

For each cluster, install the services.

#### spark cluster
```
peg service install spark_cluster aws
peg service install spark_cluster environment
peg service install spark_cluster hadoop
peg service install spark_cluster spark
```

Install airflow on leader node of spark cluster

```
sudo apt-get install python3-pip
sudo python3 -m pip install apache-airflow
```


Config spark cluster and sync the hadoop and spark configs among nodes.
```
bash ./cluster_configs/sync_scripts/sync_h.sh
bash ./cluster_configs/sync_scripts/sync_s.sh
```

#### postgres node & flask node
```
peg service install post_node aws
peg service install post_node environment
peg service install flask_node aws
peg service install flask_node environment
```
On the postgres node install postgres
```
sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get install postgresql postgresql-contrib​
```
On the flask node install flask
```
sudo apt-get install python3-pip
pip install Flask
```
---

## Run the system

#### Compile scala project
Generate the fat jar using sbt tools.
```
cd spark_batch
sbt clean
sbt compile
sbt assembly
```

#### Run spark job

After compile the jar file. Submit the job to spark to run. 
```
bin/spark-submit --class com.spot.parking.tracking.Aggregateor --master yarn --deploy-mode client ~/Spot/parking-tracking/target/scala-2.11/parking-tracking-assembly-0.0.1.jar
```

#### Schedule job

Running airflow/schedule.sh on the master of spark cluster will add the batch job to the scheduler. The batch job is set to execute every 24 hours
```
bash airflow/schedule.sh
```

#### Run web app
On the flask node
```
sudo python3 flask/run.py
```

## Contact Information

* [LinkedIn](https://www.linkedin.com/in/pengwei715)
* weipeng0715@gmail.com
