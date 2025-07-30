from fastapi import APIRouter, Query
from models.request_models import PowRequest
from models.response_models import ResultResponse
from services.math_ops import compute_pow, compute_fibonacci, compute_factorial
from storage.memory_store import store_request

router = APIRouter()


@router.post("/pow", response_model=ResultResponse)
def pow_endpoint(req: PowRequest):
    result = compute_pow(req.base, req.exponent)
    store_request("pow", req.dict(), result)
    return {"result": result}


@router.get("/fibonacci", response_model=ResultResponse)
def fibonacci_endpoint(n: int = Query(..., ge=0)):
    result = compute_fibonacci(n)
    store_request("fibonacci", {"n": n}, result)
    return {"result": result}


@router.get("/factorial", response_model=ResultResponse)
def factorial_endpoint(n: int = Query(..., ge=0)):
    result = compute_factorial(n)
    store_request("factorial", {"n": n}, result)
    return {"result": result}
