#coding=utf8
import pika

bd = ''
def infoout():

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='HELLO')

    def callback(ch, method, properties, body):
        print (" [x] Received %r" % (body,))
        global bd
        bd = body
        print('bodys= ',bd)



    channel.basic_consume(callback, queue='HELLO', no_ack=False)

    print('body=',bd)
    print (' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()



infoout()