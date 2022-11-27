from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession


# set conf
conf = (
    SparkConf()
        .set("spark.hadoop.fs.s3a.fast.upload", True)
        .set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .set('spark.hadoop.fs.s3a.aws.credentials.provider', 'com.amazonaws.auth.EnvironmentVariableCredentialsProvider')
        .set('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:2.7.3')
)

# apply config
sc = SparkContext(conf=conf).getOrCreate()

if __name__ == "__main__":

    # init spark session
    spark = SparkSession\
        .builder\
        .appName("ENADE Job")\
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    df = (
        spark
        .read
        .format("csv")
        .options(header="true", inferSchema='true', delimeter=';')
        .load("s3a://desafio-modulo-3-850900288339/zona_raw/enade/")
    )

    df.printSchema()

    (df
    .write
    .mode("overwrite")
    .format("parquet")
    .save("s3a://desafio-modulo-3-850900288339/zona_staging/enade/")
    )

    print("**************")
    print("Escrito com sucesso!")
    print("**************")

    spark.stop()