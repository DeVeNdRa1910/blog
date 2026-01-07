from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def start_get():
    return "Hello Devendra please try to finish fastapi, Rag, lang chain before end of january"