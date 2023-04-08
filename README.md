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
The data source for this project is Finnhub, and we will be building a real-time dashboard to track Bitcoin:USD price & volume metrics. To ferry the data from the upstream source (Finnhub websocket) to the dashboard application we are building, we will need a robust pipeline in the middle to handle the I/O. This is where kafka will come into the fold as the message broker, and Apache Spark to provide the processing grunt to shovel this data across to the Cassandra DB. It is important to note that for the purpose of this demo project, each component will be dockerised and ran locally for intial testing, after which we will refactor and setup kubernetes orchestration. With minor code refactoring, we can easily set this up to run remotely on EKS/ECS with higher redundancy.


# Initial setup

## Kafka Cluster
Kafka is a distributed messaging system that allows producers to write data to topics and consumers to read data from topics. Producers and consumers in Kafka are client applications that use the Kafka API to interact with the Kafka cluster. Overall, the Kafka producer and consumer APIs provide a powerful and flexible way to write and read data to and from Kafka topics. The producer and consumer APIs allow developers to build highly scalable and fault-tolerant applications that can process and analyze large volumes of data in real-time.

Our Kafka cluster will be run on docker, and the container configurations can be found in the `docker-compose.yaml` file in the root directory:
- zookeeper container:  A distributed coordination service that is used by Apache Kafka to manage and maintain the Kafka cluster. ZooKeeper helps Kafka in performing several important tasks, such as leader election, broker registration, and cluster membership management.
- broker container: A broker is a server that is responsible for managing a portion of the Kafka topic partitions. Brokers store the topic partitions, receive messages from producers, and deliver messages to consumers. Brokers also maintain metadata information about the topic partitions, such as the number of partitions, replication factor, and the location of partition replicas.
- Kafdrop container: An open-source web-based tool for monitoring Apache Kafka clusters. It provides a user-friendly web interface for visualizing the Kafka topics, partitions, messages, and consumer groups, and allows you to monitor the real-time activity of your Kafka cluster.
![Kafdrop example](docs/kafdrop.png)

## Producer
We'll start off by writing a long-running python service that subscribes to the Binance Bitcoin trading topic on the Finnhub WS endpoint. This producer app uses `websocket` and `kafka-python` to read messages in near real time via the web socket and encodes each json response in avro binary format. Each message is sent to the Kafka broker we set up in the docker compose file above. Since we are using Kafka as a message bus only, we are mainly interested in sending these ticker data points to a single topic for the purpose of consuming them asynchronously in a separate spark processing cluster.

## Consumer Test
This is something I added for testing purposes to validate that the Kafka cluster was setup properly and the producer app was successfully pulling data from the web socket and submitting them to the kafka topic. This definitely helped debugging formatting issues with AVRO conversions prior to writing up the spark processor app.

## Spark Processor (Consumer)



## Grafana Dashboard
![Grafana Dashboard](docs/dashboard.png)


## Improvements & Takeaways
* Log tracing with Spark clusters can be painful. It would be great to setup robust log monitoring by segmenting different log levels and using a third party monitoring tool to more easily access these logs and debug errors that may not be easily detected sifting through raw logs within each docker instance.
* Clean up CI/CD and use Kubernetes to orchestrate the docker containers.
* Add multiple stock tickers and add more aggregated views such as hourly comparisons or anomaly detection.
