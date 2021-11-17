from __future__ import print_function

import logging

import grpc
import alive_check_pb2
import alive_check_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = alive_check_pb2_grpc.AliveServiceStub(channel)
        response = stub.GetHealthy(alive_check_pb2.AliveRequest(name='alive'))
        return response.is_alive

if __name__ == '__main__':
    logging.basicConfig()
    run()