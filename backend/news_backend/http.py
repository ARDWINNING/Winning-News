import json
from typing import Any, Optional

class Request:
    def __init__(self, method: str, path: str, headers: dict[str, str], cookies: dict[str, str], body: bytes, 
                 user: Optional[Any] = None, permissions: Optional[set[str]] = None, session: Optional[dict[str, Any]] = None,):
        self.method = method.upper() 
        self.path = path 
        self.headers = headers 
        self.cookies = cookies 
        self.body = body 
        self.user = user 
        self.permissions = permissions or set() 
        self.session = session
    
    def json(self) -> Any:
        if not self.body: 
            return None 
        return json.loads(self.body.decode("utf-8"))

class Response:
    def __init__(self, body: bytes, status: int = 200, headers: Optional[dict[str, str]] = None):
        self.body = body
        self.status = status
        self.headers = headers or {}

    def as_wsgi(self):
        return self.status, self.headers, [self.body]

    def as_asgi(self):
        return {"status": self.status, "headers": [
            (k.encode("latin-1"), v.encode("latin-1"))
            for k, v in self.headers.items()
            ],
            "body": self.body,
        }


class JSONResponse(Response):
    def __init__(self, data: Any, status: int = 200, headers: Optional[dict[str, str]] = None):
        body = json.dumps(data).encode("utf-8")
        headers = headers or {}
        headers.setdefault("Content-Type", "application/json")
        super().__init__(body=body, status=status, headers=headers)