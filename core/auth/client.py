import grpc

from core.auth.declaration.auth_pb2 import (
    AuthorizeRequest,
    GetUserRequest,
    User,
    Verification,
)
from core.auth.declaration.auth_pb2_grpc import AuthServiceStub
from env import MicroEnv

STORED_CLIENT = None


async def generate_client():
    global STORED_CLIENT

    if STORED_CLIENT:
        return STORED_CLIENT

    channel = grpc.aio.insecure_channel(f"{MicroEnv.AUTH_HOST}:{MicroEnv.AUTH_PORT}")
    client = AuthServiceStub(channel)

    STORED_CLIENT = client
    return client


class VerificationWrapper:
    type: str
    department: str
    grade: int
    classroom: int
    number: int
    valid_until: str
    graduated_at: str


class UserWrapper:
    id: int
    phone: str
    name: str
    profile: str
    created_at: str
    is_suspended: bool
    verification: Verification | VerificationWrapper


async def authorize(token: str) -> int:
    client = await generate_client()

    response = await client.Authorize(AuthorizeRequest(token=token))
    return response.userid if response.userid else None


async def get_user(userid: int) -> User | UserWrapper:
    client = await generate_client()
    response = await client.GetUser(GetUserRequest(userid=userid))
    return response.user if response.success else None
