# Real Time Stock Tracker Pipeline
This project is a data streaming pipeline for Finnhub stock market ticker data using Kafka, Spark, Cassandra. This project is intended to showcase the setup of an end-to-end containerised data streaming pipeline that is highly scalable.

Thank you to GitHub user RSKriegs for the inspiration on the solution architecture and data source for this personal project. You can find their original implementation of this project here: [!https://github.com/RSKriegs/finnhub-streaming-data-pipeline].
I will delve into the rationale behind the technologies used, going through the high level workings of each framework used, as well as the containerization strategy.


# The stack
- Python 3.7
- Apache Kafka
- Apache Spark
- Cassandra DB
- Grafana


# Solution Architecture
TODO - add solution architecture diagram


# The Objective
The data source for this project is Finnhub, and we will be building a real-time dashboard to track last price updates for Microsoft stock price. To ferry the data from the upstream source (Finnhub websocket) to the dashboard application we are building, we will need a robust pipeline in the middle to handle the I/O. This is where kafka will come into the fold as the message broker, and Apache Spark to provide the processing grunt to shovel this data across to the Cassandra DB. It is important to note that for the purpose of this demo project, each component will be dockerised and ran locally for intial testing, after which we will refactor and setup kubernetes orchestration. With minor code refactoring, we can easily set this up to run remotely on EKS/ECS with higher redundancy.


# Initial setup

## Producer


## Kafka Cluster
Kafka is a distributed messaging system that allows producers to write data to topics and consumers to read data from topics. Producers and consumers in Kafka are client applications that use the Kafka API to interact with the Kafka cluster. Overall, the Kafka producer and consumer APIs provide a powerful and flexible way to write and read data to and from Kafka topics. The producer and consumer APIs allow developers to build highly scalable and fault-tolerant applications that can process and analyze large volumes of data in real-time.

Our Kafka cluster will be run on docker, and the container configurations can be found in the `docker-compose.yaml` file in the root directory:
- zookeeper container:  A distributed coordination service that is used by Apache Kafka to manage and maintain the Kafka cluster. ZooKeeper helps Kafka in performing several important tasks, such as leader election, broker registration, and cluster membership management.
- broker container: A broker is a server that is responsible for managing a portion of the Kafka topic partitions. Brokers store the topic partitions, receive messages from producers, and deliver messages to consumers. Brokers also maintain metadata information about the topic partitions, such as the number of partitions, replication factor, and the location of partition replicas.
- Kafdrop container: An open-source web-based tool for monitoring Apache Kafka clusters. It provides a user-friendly web interface for visualizing the Kafka topics, partitions, messages, and consumer groups, and allows you to monitor the real-time activity of your Kafka cluster.
![Kafdrop example](docs/kafdrop.png)

# Starting with data source prep
Finnhub provides a free, real-time stocks API which can be consumed via websocket. They have a very handy Python library to help interface with their API, called `finnhub-python`.

We'll start off by writing a long-running python service that subscribes to the Binance Bitcoin trading topic on the Finnhub WS endpoint. This producer app reads the messages sent via the WS polls and encodes the json response in avro binary format. The message is sent to the Kafka broker 

