# proyectoBigData
Proyecto del curso de Big Data, utilizando servicio dockerizado de apache spark, servicio que contiene
un container master y dos containers worker. El master escucha el en puerto 9080, el worker1 y worker2 escuchan en los puertos 
8081 y 8082 correspondientemente. 

## Configuracion DataSet 
Los datos que se utilizan para este proyecto se encuentran en el siguiente enlace: https://www.kaggle.com/currie32/crimes-in-chicago?select=Chicago_Crimes_2012_to_2017.csv.
Especificamente se utilizan los datos comprendidos entre el año 2012 y el año 2017 (367 MB).   
Al ser un archivo demasiado grande no se carga dentro del repositorio del proyecto. Para agregar los datos al proyecto, se deben descargar de la pagina y posteriormente, crear una carpeta con el nombre "data" dentro del directorio de proyecto. 
Finalmente se debe copiar el dataset descargado dentro de esta carpeta. 

## Configuracion de entorno y ejecución - Contenedores
Para configuirar el entorno primero se debe crear una imgen docker con el dockerFile.
```
sudo docker build -t "spark" .
```
Posteriormente se debe correr el archivo docker compose.
```
sudo docker-compose up
```
Luego, se debe acceder al contenerdor master (ver el id que tiene usando docker ps -a).
```
sudo docker exec -it <container_id> /bin/bash
```
Ejecución de dataClean.py
```
spark-2.4.1/bin/spark-submit --master spark://master:7077 /usr/src/dataClean/dataClean.py /tmp/data/Chicago_Crimes_2012_to_2017.csv /tmp/data/dataClean/
```
Ejecución de machineL.py
```
spark-2.4.1/bin/spark-submit --master spark://master:7077 /usr/src/machineLearning/machineL.py
```

### Kafka - Comandos básicos

Se debe ingresar la carpeta /bin dentro del servidor kafka. 
```
kafka-topics --list --zookeeper zookeeper:2181
```
```
kafka-topics --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic sample_topic2
```
```
kafka-topics --zookeeper zookeeper:2181 --topic topic --delete
```
```
kafka-console-producer --broker-list kafka:9092 --topic sample_topic
```
```
kafka-console-consumer --bootstrap-server kafka:9092 --topic sample_topic --from-beginning
```

### Kafka - Conectores

* cd etc/kafka/
* cp connect-standalone.properties ~
* cp connect-file-sink.properties ~/
* cp connect-file-source.properties ~/
* connect-standalone.properties
    ```
    echo "bootstrap.servers=kafka:9092" > connect-standalone.properties
    ```
    ```
    echo "key.converter=org.apache.kafka.connect.json.JsonConverter" >> connect-standalone.properties
    ```
    ```
    echo "value.converter=org.apache.kafka.connect.json.JsonConverter" >> connect-standalone.properties
    ```
    ```
    echo "key.converter.schemas.enable=false" >> connect-standalone.properties
    ```
    ```
    echo "value.converter.schemas.enable=false" >> connect-standalone.properties
    ```
    ```
    echo "offset.flush.interval.ms=10000" >> connect-standalone.properties
    ```
    ```
    echo "offset.storage.file.filename=/tmp/connect.offsets" >> connect-standalone.properties
    ```
    ```
    echo "plugin.path=/usr/share/java" >> connect-standalone.properties
    ```
    ```
    echo "plugin.path=/usr/share/java,/usr/local/share/kafka/plugins,/opt/connectors" >> connect-standalone.properties
    ```

    bootstrap.servers=kafka:9092

    key.converter=org.apache.kafka.connect.json.JsonConverter

    value.converter=org.apache.kafka.connect.json.JsonConverter

    key.converter.schemas.enable=false

    value.converter.schemas.enable=false

    offset.flush.interval.ms=10000

    offset.storage.file.filename=/tmp/connect.offsets
    
    plugin.path=/usr/share/java

* connect-file-sink.properties
    ```
    echo "name=local-file-sink" > connect-file-sink.properties
    ```
    ```
    echo "connector.class=FileStreamSink" > connect-file-sink.properties
    ```
    ```
    echo "tasks.max=1" > connect-file-sink.properties
    ```
    ```
    echo "file=/home/appuser/outcome_log.txt" > connect-file-sink.properties
    ```
    ```
    echo "topics=test" > connect-file-sink.properties
    ```

    name=local-file-sink

    connector.class=FileStreamSink

    tasks.max=1

    file=/home/appuser/outcome_log.txt

    topics=test

* connect-file-source.properties
    ```
    echo "name=local-file-source" > connect-file-source.properties
    ```
    ```
    echo "connector.class=FileStreamSource" >> connect-file-source.properties
    ```
    ```
    echo "tasks.max=1" >> connect-file-source.properties
    ```
    ```
    echo "file=/home/appuser/access_log.txt" >> connect-file-source.properties
    ```
    ```
    echo "topic=test" >> connect-file-source.properties
    ```

    name=local-file-source

    connector.class=FileStreamSource

    tasks.max=1

    file=/home/appuser/access_log.txt

    topic=test

* connect-standalone ~/connect-standalone.properties ~/connect-file-source.properties ~/connect-file-sink.properties

## Configuracion de entorno y ejecución - Sandbox

### Kafka - Comandos básicos

Se debe ingresar la carpeta /usr/hdp/current/kafka-broker

Listar todos los temas.
```
./kafka-topics.sh --list --zookeeper sandbox-hdp.hortonworks.com:2181
```
Crear un nuevo tema.
```
./kafka-topics.sh --create --zookeeper sandbox-hdp.hortonworks.com:2181 --replication-factor 1 --partitions 1 --topic sample_topic
```
Eliminar un tema.
```
./kafka-topics.sh --zookeeper sandbox-hdp.hortonworks.com:2181 --topic topic --delete
```
Activar productor.
```
./kafka-console-producer.sh --broker-list sandbox-hdp.hortonworks.com:6667 --topic sample_topic
```
Activar consumidor.
```
./kafka-console-consumer.sh --bootstrap-server sandbox-hdp.hortonworks.com:6667 --topic sample_topic --from-beginning
```
Cambiar tiempo de retención. Default retention.ms = 604800
```
./kafka-topics.sh --zookeeper sandbox-hdp.hortonworks.com:2181 --alter --topic sample_topic --config retention.ms=1000 
```

### Kafka - Conectores

* cd /usr/hdp/current/kafka-broker/conf
* cp connect-standalone.properties ~/
* cp connect-file-sink.properties ~/
* cp connect-file-source.properties ~/
* connect-standalone.properties
    bootstrap.servers=sandbox-hdp.hortonworks.com:6667

* connect-file-sink.properties
    name=local-file-sink

    connector.class=FileStreamSink

    tasks.max=1

    file=/home/maria_dev/outcome_log.txt

    topics=sample_topic

* connect-file-source.properties
    name=local-file-source

    connector.class=FileStreamSource

    tasks.max=1

    file=/home/maria_dev/access_log.txt

    topic=sample_test
* ./connect-standalone.sh ~/connect-standalone.properties ~/connect-file-source.properties ~/connect-file-sink.properties