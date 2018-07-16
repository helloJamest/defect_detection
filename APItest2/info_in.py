#coding=utf8
import pika
'''
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

#声明队列，如果消息发送到不存在的队列，rabbitmq会自动清除这些消息
channel.queue_declare(queue='HELLO')

for i in range(1):
    #exchange表示交换器，可以精确的制定消息应发到哪个队列，route_key设置队列的名称，body表示发送的内容
    channel.basic_publish(exchange='', routing_key='HELLO', body='Hello World!' + str(i))
    print (" [%d] Sent 'Hello World!'" % i)
#关闭连接
connection.close()
'''
with open('/home/win/project/APItest2/param', 'w') as f:
    f.write('0')