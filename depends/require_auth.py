from fastapi import Header
from fastapi.exceptions import HTTPException
from grpc.aio._call import AioRpcError

from core.auth.client import authorize


async def RequireAuth(authorization: str = Header(...)):
    try:
        token_type, token = authorization.split(" ")

        if token_type.lower() != "bearer":
            raise

        userid = await authorize(token)

        if not userid:
            raise

        return userid
    except AioRpcError:
        raise HTTPException(status_code=500, detail="INTERNAL_COMMUNICATION_ERROR")
    except:
        raise HTTPException(status_code=401, detail="UNAUTHORIZED")
