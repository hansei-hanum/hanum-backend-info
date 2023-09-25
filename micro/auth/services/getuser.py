from ..client import client
from ..declaration.auth_pb2 import GetUserRequest


async def get_user(userid: int) -> dict:
    response = await client.GetUser(GetUserRequest(userid=userid))
    return response.user if response.success else None
