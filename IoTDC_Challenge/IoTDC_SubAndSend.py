import pika
import ssl
import requests
import json


# This is the Username and password that was supplied with the kit
username = "devnet_iot+userX@cisco.com"
password = "password"

# You need to Create a bot at https://developer.ciscospark.com and paste your bot token here
token = "Bearer <token>"

# This is the e-mail address associated with your Spark Account
email_address = "Your_E-mail_address_here_HERE@cisco.com"

# This is the IoTDC organization ID supplied with your kit
orgID = <your org id here>


def spark_it(message, bot_token, email):
    start_url = "https://api.ciscospark.com"

    token = bot_token

    header = {"Authorization": "%s" % token,
              "Content-Type": "application/json"}

    api_url = "/v1/messages/"
    data = {"toPersonEmail": email,
            "text": message}

    spark_url = start_url + api_url

    spark_message = requests.post(spark_url, headers=header, data=json.dumps(data), verify=True)

    return spark_message.text


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


channel.queue_bind(exchange="%s-EXC" % orgID,
                   queue=queue_name,
                   routing_key="dev2app",
                   )

print("Connected to IoTDC")


def callback(ch, method, properties, body):
    msg = body.decode("utf-8")[0]
    print(" [x] Received %r" % msg)
    text = ""
    if msg == "1":
        text = "Alert Triggered"
    print(spark_it(text, token, email_address))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
