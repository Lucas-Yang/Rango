import socket
import time

class LancerStream(object):
    def __init__(self, logid, sock):
        self.logid = logid
        self.sock = sock
        self.client = None

    def connect(self):
        try:
            self.client = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
            self.client.connect(self.sock)
            self.client.setblocking(0)
        except Exception as e:
            print("Failed to connect to log agent:{}".format(e))
            self.client = None

    def write(self, msg):
        if not self.client:
            self.connect()
        if self.client:
            msg_send = self.logid + str(int(time.time() * 1000)) + msg
            try:
                self.client.sendall(msg_send.encode("utf-8"))
            except Exception as e:
                print("Failed to send log to log agent:{}".format(e))
                self.client = None
