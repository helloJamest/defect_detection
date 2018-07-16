#code=utf-8
import sys
sys.path.append('./evaluate')
import httptools
import socket

hostname = socket.gethostname()
print hostname
com_info = {'mac':hostname,'lightnum':1,'cameranum':1}
httptools.addpc(com_info)
