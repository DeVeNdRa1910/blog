from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/")
def create_blog(request: Request):
    print(request)
    return {"data": "Blos has been created"}