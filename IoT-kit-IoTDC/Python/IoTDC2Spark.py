import pika

iotdc_user = "<your username here>"
iotdc_pass = "<your password here>"

creds = pika.PlainCredentials(iotdc_user, iotdc_pass)
spark_token = "Bearer <token>"
spark_room = "<room id>"

connection = pika.BlockingConnection(pika.ConnectionParameters(ssl=True,
                                                               host='iotdc-tme2.iotspdev.io',
                                                               virtual_host="IOTSP_INTERNAL",
                                                               port=5671,
                                                               credentials=creds))

queue_name = ""
channel = connection.channel()
channel.queue_declare(queue=queue_name, passive=False,
                      durable=False, exclusive=False, auto_delete=False)  # Declare a queue


channel.queue_bind(exchange="24-EXC",
                   queue=queue_name,
                   routing_key="dev2app",
                   )


def spark_it(message, bot_token, roomid):
    start_url = "https://api.ciscospark.com"

    token = bot_token

    header = {"Authorization": "%s" % token,
              "Content-Type": "application/json"}

    api_url = "/v1/messages/"
    data = {"roomId": roomid,
            "text": message}

    spark_url = start_url + api_url

    spark_message = requests.post(spark_url, headers=header, data=json.dumps(data), verify=True)

    return spark_message

spark_it("You're connected to IoTDC!!!", spark_token, spark_room)


def callback(ch, method, properties, body):
    spark_it(body, spark_token, spark_room)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

spark_it("Waiting for messages. To exit press CTRL+C", spark_token, spark_room)
channel.start_consuming()
