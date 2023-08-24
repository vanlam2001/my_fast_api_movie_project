from fastapi import Depends, Header, HTTPException


def get_token_authorization(Token: str = Header(..., description="Nhập token")) -> str:
    if Token != "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return Token



    

# Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1lIjoiZ3VsZGl1c2d2aWxzIiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9yb2xlIjoiR1YiLCJuYmYiOjE2OTIzNzUyNzYsImV4cCI6MTY5MjM3ODg3Nn0.jkSmNQT5rROC_fQHoX8Q-WUWCs1pcB2hXSGZ64aHWyw