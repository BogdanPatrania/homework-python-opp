import io
import csv
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from api.routes import router
from services.math_ops import compute_pow, compute_fibonacci, compute_factorial
from storage.sqlite_store import init_db, store_request_sqlite, get_all_requests_sqlite


init_db()


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
        store_request_sqlite("pow", {"base": a, "exponent": b}, result)

    elif op_type == "fibonacci":
        result = compute_fibonacci(a)
        store_request_sqlite("fibonacci", {"n": a}, result)

    elif op_type == "factorial":
        result = compute_factorial(a)
        store_request_sqlite("factorial", {"n": a}, result)

    else:
        result = "Invalid operation"

    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": result,
        "op_type": op_type
    })

@app.get("/history/export")
def export_history():
    history = get_all_requests_sqlite()
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Operation', 'Input', 'Result', 'Timestamp'])
    cw.writerows(history)
    si.seek(0)
    return StreamingResponse(
        si,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=history.csv"}
    )
