from fastapi import HTTPException, status

def not_found(obj: str, id: int):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{obj} with id {id} is not available :("
    )