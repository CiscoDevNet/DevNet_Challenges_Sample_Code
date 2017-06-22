import pika
import ssl
import requests


username = "your username"
password = "password"

token = "Bearer <token>"
email_address = "<email address tied to your spark account>"


def spark_it(message, bot_token, email):
    start_url = "https://api.ciscospark.com"

    token = bot_token

    header = {"Authorization": "%s" % token,
              "Content-Type": "application/json"}

    api_url = "/v1/messages/"
    data = {"email": email,
            "text": message}

    spark_url = start_url + api_url

    spark_message = requests.post(spark_url, headers=header, data=json.dumps(data), verify=True)

    return spark_message


creds = pika.PlainCredentials(username, password)

connection = pika.BlockingConnection(pika.ConnectionParameters(ssl=True,
                                                               host='iotdc-tme.iotspprod.io',
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

print("Connected to IoTDC")


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    print(spark_it(body, token, email_address))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()