import grpc
from .declaration.auth_pb2_grpc import AuthServiceStub
from env import MicroEnv


channel = grpc.aio.insecure_channel(f"{MicroEnv.AUTH_HOST}:{MicroEnv.AUTH_PORT}")
client = AuthServiceStub(channel)
