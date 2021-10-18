from fastapi import HTTPException, status

def not_found(obj: str, id: int):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{obj} with id {id} is not available :("
    )

def user_exits(email: str):
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"User with email {email} already exit"
    )

def email_error():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Invalid email"
    )

def disabled_user():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Disabled user"
    )

{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzQ1ODg4NzQsImlhdCI6MTYzNDU4NzA3NCwic2NvcGUiOiJhY2Nlc3NfdG9rZW4iLCJzdWIiOiJ1c2VyQGV4YW1wbGUuY29tIn0.ngXQvZSleaWHBOAMQKVKRwuYwcAndKZFv4ryE6Eoy14",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzQ2MjMwNzQsImlhdCI6MTYzNDU4NzA3NCwic2NvcGUiOiJyZWZyZXNoX3Rva2VuIiwic3ViIjoidXNlckBleGFtcGxlLmNvbSJ9.eLjwVizEFcm-zF_5NwMdrc1c4ty8JhgnNvTLjUGS6XY"
}