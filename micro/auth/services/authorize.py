from ..client import client
from ..declaration.auth_pb2 import AuthorizeRequest


async def authorize(token: str) -> int:
    response = await client.Authorize(AuthorizeRequest(token=token))
    return response.userid if response.userid else None
