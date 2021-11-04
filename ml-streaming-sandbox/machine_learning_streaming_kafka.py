import re
 
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.flume import FlumeUtils
 
parts = [
    r'(?P<host>\S+)',                   # host %h
    r'\S+',                             # indent %l (unused)
    r'(?P<user>\S+)',                   # user %u
    r'\[(?P<time>.+)\]',                # time %t
    r'"(?P<request>.+)"',               # request "%r"
    r'(?P<status>[0-9]+)',              # status %>s
    r'(?P<size>\S+)',                   # size %b (careful, can be '-')
    r'"(?P<referer>.*)"',               # referer "%{Referer}i"
    r'"(?P<agent>.*)"',                 # user agent "%{User-agent}i"
]
pattern = re.compile(r'\s+'.join(parts)+r'\s*\Z')
 
def extractURLRequest(line):
    exp = pattern.match(line)
    if exp:
        request = exp.groupdict()["request"]
        if request:
           requestFields = request.split()
           if (len(requestFields) > 1):
                return requestFields[1]
 
 
def compute(rdd):
    print(rdd.count())

if __name__ == "__main__":
 
    sc = SparkContext(appName="StreamingFlumeLogAggregator")
    sc.setLogLevel("ERROR")
    ssc = StreamingContext(sc, 1)
 
    flumeStream = FlumeUtils.createStream(ssc, "localhost", 9092)

    # dstream = flumeStream.reduceByWindow(lambda x, y: x + y, lambda x, y : x - y, 10, 1)
 
    # # Sort and print the results
    # sortedResults = urlCounts.transform(lambda rdd: rdd.sortBy(lambda x: x[1], False))
    flumeStream.foreachRDD(compute)
 
    ssc.checkpoint("/user/maria_dev/ml-streaming/checkpoint")
    ssc.start()
    ssc.awaitTermination()