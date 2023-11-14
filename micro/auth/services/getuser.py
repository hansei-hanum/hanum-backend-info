from ..client import generate_client
from ..declaration.auth_pb2 import GetUserRequest, User, Verification


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


async def get_user(userid: int) -> User | UserWrapper:
    client = await generate_client()
    response = await client.GetUser(GetUserRequest(userid=userid))
    return response.user if response.success else None
