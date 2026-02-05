from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def home():
    return {"message": "Bee - Your Personal Task Manager"}
