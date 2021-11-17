from concurrent import futures
from threading import Thread
import threading
import logging
import time

import grpc
import alive_check_pb2
import alive_check_pb2_grpc

def runT():
    time.sleep(10)

class Alive(alive_check_pb2_grpc.AliveServiceServicer):

    def GetHealthy(self, request, context):
        t2 = 0
        for thread in threading.enumerate(): 
            if thread.name == request.name:
                t2 = thread

        if t2 == 0:
            is_alive = False
        else:
            is_alive = t2.is_alive()

        return alive_check_pb2.AliveResponse(is_alive=is_alive)

def serve():
    t1 = Thread(target = runT, name='alive')
    t1.setDaemon(True)
    t1.start()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    alive_check_pb2_grpc.add_AliveServiceServicer_to_server(Alive(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()

