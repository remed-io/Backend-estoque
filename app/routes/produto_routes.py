from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def listar_produtos():
    return {"produtos": ["Dipirona", "Paracetamol", "Ibuprofeno"]}

