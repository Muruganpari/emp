# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import uvicorn
from fastapi import Depends, FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Form
from fastapi.encoders import jsonable_encoder

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from model import Employee
from memcache import memclient
import schema
from database import SessionLocal, engine
import model

app = FastAPI()

model.Base.metadata.create_all(bind=engine)

#Api Rate limiter
limiter = Limiter(key_func=get_remote_address)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def get_database_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
@limiter.limit("20/minute")
async def read_item(request: Request, db: Session = Depends(get_database_session)):
    records = db.query(Employee).all()
    #records = memclient.get('employee_list')

    if records is None:
        records = db.query(Employee).all()
        memclient.set('employee_list', records)

    return templates.TemplateResponse("index.html", {"request": request, "data": records})


@app.get("/employee/{name}", response_class=HTMLResponse)
@limiter.limit("20/minute")
def read_item(request: Request, name: schema.Employee.name, db: Session = Depends(get_database_session)):
    item = db.query(Employee).filter(Employee.id == name).first()
    return templates.TemplateResponse("update.html", {"request": request, "employee": item})


@app.post("/employee/")
async def create_employee(db: Session = Depends(get_database_session), name: schema.Employee.name = Form(...),
                       designation: schema.Employee.designation = Form(...), age: schema.Employee.age = Form(...), email: schema.Employee.email = Form(...)):
    emp = Employee(name=name, designation=designation, age=age, email=email)
    db.add(emp)
    db.commit()
    db.refresh(emp)
    memclient.set('employee_list', emp)
    response = RedirectResponse('/', status_code=303)
    return response


@app.patch("/employee/{id}")
async def update_employee(request: Request, id: int, db: Session = Depends(get_database_session)):
    requestBody = await request.json()
    emp = db.query(Employee).get(id)
    emp.name = requestBody['name']
    emp.email = requestBody['email']
    emp.designation = requestBody['designation']
    emp.age = requestBody['age']
    db.commit()
    db.refresh(emp)
    newEmployee = jsonable_encoder(emp)
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "message": "success",
        "employee": newEmployee
    })


@app.delete("/employee/{id}")
async def delete_employee(request: Request, id: int, db: Session = Depends(get_database_session)):
    movie = db.query(Employee).get(id)
    db.delete(movie)
    db.commit()
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "message": "success",
        "employee": None
    })


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
