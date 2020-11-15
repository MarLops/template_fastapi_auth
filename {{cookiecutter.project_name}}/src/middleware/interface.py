from abc import ABC
from fastapi import Request
from starlette.middleware.base import StreamingResponse


class MiddlewareBase(ABC):
    def __init__(self):
        ...
    
    async def __call__(self, request: Request, call_next):
        request = await self.middleware_before(request)
        response = await call_next(request)
        response = await self.middleware_after(response)
        return response

    async def middleware_before(self,request: Request):
        return request
    
    async def middleware_after(self,response: StreamingResponse):
        return response
    

    

