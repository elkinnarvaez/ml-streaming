# proyectoBigData

## Configuracion DataSet 
Los datos que se utilizan para este proyecto se encuentran en el siguiente enlace: https://www.kaggle.com/currie32/crimes-in-chicago?select=Chicago_Crimes_2012_to_2017.csv.
Especificamente se utilizan los datos comprendidos entre el año 2012 y el año 2017 (367 MB).   
Al ser un archivo demasiado grande no se carga dentro del repositorio del proyecto. Para agregar los datos al proyecto, se deben descargar de la pagina y posteriormente agregarlos al proyecto.

## Contenedores
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

Listar todos los temas.
```
kafka-topics --list --zookeeper zookeeper:2181
```
Crear un nuevo tema.
```
kafka-topics --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic sample_topic2
```
Eliminar un tema.
```
kafka-topics --zookeeper zookeeper:2181 --topic topic --delete
```
Activar productor.
```
kafka-console-producer --broker-list kafka:9092 --topic sample_topic
```
Activar consumidor.
```
kafka-console-consumer --bootstrap-server kafka:9092 --topic sample_topic --from-beginning
```

### Kafka - Conectores

* Entrar al servidor de kafka
    ```
    cd /etc/kafka/
    ```
* Copiar el archivo connect-standalone.properties
    ``` 
    cp connect-standalone.properties ~/
    ```
*  Copiar el archivo connect-file-sink.properties
    ```
    cp connect-file-sink.properties ~/
    ```
* Copiar el archivo connect-file-source.properties
    ```
    cp connect-file-source.properties ~/
    ```
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
* Ejecutar el conector
    ```
    connect-standalone ~/connect-standalone.properties ~/connect-file-source.properties ~/connect-file-sink.properties
    ```

## Sandbox

### Kafka - Comandos básicos
```
cd /usr/hdp/current/kafka-broker
```
```
cd bin
```
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
./kafka-topics.sh --zookeeper sandbox-hdp.hortonworks.com:2181 --delete --topic sample_topic
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

* Entrar al servidor de kafka
    ```
    cd /usr/hdp/current/kafka-broker/conf
    ```
* Copiar el archivo connect-standalone.properties
    ``` 
    cp connect-standalone.properties ~/
    ```
*  Copiar el archivo connect-file-sink.properties
    ```
    cp connect-file-sink.properties ~/
    ```
* Copiar el archivo connect-file-source.properties
    ```
    cp connect-file-source.properties ~/
    ```
* connect-standalone.properties
    ```
    bootstrap.servers=sandbox-hdp.hortonworks.com:6667
    ```
* connect-file-sink.properties
    ```
    name=local-file-sink
    connector.class=FileStreamSink
    tasks.max=1
    file=/home/maria_dev/outcome_log.txt
    topics=sample_topic
    ```
* connect-file-source.properties
    ```
    name=local-file-source
    connector.class=FileStreamSource
    tasks.max=1
    file=/home/maria_dev/access_log.txt
    topic=sample_topic
    ```
* Ejectutar el conector
    ```
    ./connect-standalone.sh ~/connect-standalone.properties ~/connect-file-source.properties ~/connect-file-sink.properties
    ```

### Flume
```
cd /usr/hdp/current/flume-server
```
```
cd bin
```
#### Example: Netcat
* Archivo de configuración para un agente
    ```
    # Name of the components on this agent
    a1.sources = r1
    a1.sinks = k1
    a1.channels = c1

    # Describe/configure the source
    a1.sources.r1.type = netcat
    a1.sources.r1.bind = localhost
    a1.sources.r1.port = 44444

    # Describethe sink
    a1.sinks.k1.type = logger

    # Use a channel that buffers events in memory
    a1.channels.c1.type = memory
    a1.channels.c1.capacity = 1000
    a1.channels.c1.transactionCapacity = 100

    # Bind the source and sink to the channel
    a1.sources.r1.channels = c1
    a1.sinks.k1.channel = c1
    ```
* Ejecutar el agente
    ```
    sudo flume-ng agent --conf conf --conf-file /home/maria_dev/simple-flume-flow.conf --name a1 -Dflume.root.logger=INFO, console -Dlog4j.configurationFile=/usr/hdp/current/flume-server/conf/log4j2.xml
    ```
* Enviar datos a través de telnet
    ```
    telnet localhost 44444
    ```
* Verificar el archivo log
    ```
    tail -f /var/log/flume/flume.log
    ```

#### Example: Spooldir
* Archivo de configuración para un agente
    ```
    # Name of the components on this agent
    a1.sources = r1
    a1.sinks = k1
    a1.channels = c1

    # Describe/configure the source
    a1.sources.r1.type = spooldir
    a1.sources.r1.spoolDir = /home/maria_dev/spool
    a1.sources.r1.fileHeader = true
    a1.sources.r1.interceptors = timestampInterceptor
    a1.sources.r1.interceptors.timestampInterceptor.type = timestamp

    # Describethe sink
    a1.sinks.k1.type = hdfs
    a1.sinks.k1.hdfs.path = /user/maria_dev/flume/%y-%m-%d/%H%M/%S
    a1.sinks.k1.hdfs.filePrefix = events-
    a1.sinks.k1.hdfs.round = true
    a1.sinks.k1.hdfs.roundValue = 10
    a1.sinks.k1.hdfs.roundUnit = minute

    # Use a channel that buffers events in memory
    a1.channels.c1.type = memory
    a1.channels.c1.capacity = 1000
    a1.channels.c1.transactionCapacity = 100

    # Bind the source and sink to the channel
    a1.sources.r1.channels = c1
    a1.sinks.k1.channel = c1
    ```
* Crear directorio local y en el cluster
    ```
    mkdir spool
    ```
    ```
    hadoop fs -ls
    ```
    ```
    hadoop fs -mkdir flume
    ```
* Ejecutarel agente
    ```
    sudo flume-ng agent --conf conf --conf-file /home/maria_dev/flume-spooldir.conf --name a1 -Dflume.root.logger=INFO,console -Dlog4j.configurationFile=/usr/hdp/current/flume-server/conf/log4j2.xml
    ```

#### Example: Spark and Flume
* Archivo de configuración para el agente
    ```

    ```
* Crear directorio spool
* Copiar el archivo acess_log.txt en el directorio previamente creado
* Crear carpeta checkpoint
    ```
    sudo mkdir checkpoint
    ```
* Código Python
    ```

    ```
* Ejecutar código en Spark
    ```
    sudo /usr/hdp/current/spark2-client/bin/spark-submit --packages org.apache.spark:spark-streaming-flume_2.11:2.3.0 SparkFlume.py
    ```
    ```
    sudo /usr/hdp/current/spark2-client/bin/spark-submit --jars spark-streaming-flume-assembly_2.12-2.4.8.jar SparkFlume.py
    ```
* Ejecutar agente de Flume
    
    Entrar a la carpeta
    ```
    cd /usr/hdp/current/flume-server/bin
    ```
    Ejecutar el script
    ```
    sudo flume-ng agent --conf conf --conf-file /home/maria_dev/ml-streaming/example/spark-streaming-flume.conf --name a1 -Dlog4j.configurationFile=/usr/hdp/current/flume-server/conf/log4j2.xml
    ```
* Hacer cambios en la carpeta spool
    ```
    sudo cp access_log.txt ./spool/log1.txt
    ```

#### Proyecto: Flume
* Entrar a la carpeta ml-streaming
    ```
    cd /home/maria_dev/ml-streaming/
    ```
* Tranferir datos usando FTP dentro de la carpeta /home/maria_dev/ml-streaming/data
* Montar datos en el cluster
    ```
    hadoop fs -copyFromLocal /home/maria_dev/ml-streaming/data/Chicago_Crimes_2012_to_2017.csv /user/maria_dev/ml-streaming/data
    ```
* Ejecutar la limpieza de datos
    ```
    sudo /usr/hdp/current/spark2-client/bin/spark-submit data_cleaning.py /user/maria_dev/ml-streaming/data/Chicago_Crimes_2012_to_2017.csv /user/maria_dev/ml-streaming/data/cleanedData
    ```
* Ejecutar algoritmos de aprendizaje (sin streaming)
    ```
    sudo /usr/hdp/current/spark2-client/bin/spark-submit machine_learning.py
    ```
* Ubicar datos limpios en la carpeta /home/maria_dev/ml-streaming/data/cleanedData
* Archivo de configuración de Flume
    ```

    ```
* Ejecutar código en Spark
    ```
    sudo /usr/hdp/current/spark2-client/bin/spark-submit --packages org.apache.spark:spark-streaming-flume_2.11:2.3.0 machine_learning_streaming_flume.py
    ```
* Ejecutar agente de Flume
    
    Entrar a la carpeta
    ```
    cd /usr/hdp/current/flume-server/bin
    ```
    Ejecutar el script
    ```
    sudo flume-ng agent --conf conf --conf-file /home/maria_dev/ml-streaming/spark-streaming-flume.conf --name a1 -Dlog4j.configurationFile=/usr/hdp/current/flume-server/conf/log4j2.xml
    ```
* Hacer cambios en la carpeta spool
    ```
    cd data/cleanedData
    ```
    ```
    sudo cp data.csv /home/maria_dev/ml-streaming/spool
    ```

#### Proyecto: Structured Streaming
* Entrar a la carpeta ml-streaming
    ```
    cd /home/maria_dev/ml-streaming/
    ```
* sudo /usr/hdp/current/spark2-client/bin/spark-submit machine_learning_streaming.py