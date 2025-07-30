from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from api.routes import router
from services.math_ops import compute_pow, compute_fibonacci, compute_factorial

app = FastAPI(title="Math Microservice")
app.include_router(router)

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
def post_form(
    request: Request,
    op_type: str = Form(...),
    a: int = Form(0),
    b: int = Form(0)
):
    if op_type == "pow":
        result = compute_pow(a, b)
    elif op_type == "fibonacci":
        result = compute_fibonacci(a)
    elif op_type == "factorial":
        result = compute_factorial(a)
    else:
        result = "Invalid operation"

    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": result,
        "op_type": op_type
    })
