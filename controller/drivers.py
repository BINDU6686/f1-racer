from fastapi import APIRouter, Depends
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from f1_racer.forms.driver import DriverForm
from f1_racer.models.drivers import Drivers


templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get('/drivers/add')
@router.post("/drivers/add", response_class=HTMLResponse)
async def add_driver(request: Request):
    body = await request.form()
    form = DriverForm(body)
    if request.method == 'POST':
        if form.validate():
            model_data = form.data
            model_data["created_by"] = request.cookies.get("userId")
            print(model_data)
            model = Drivers(**model_data)
            model.add_driver()
            
    return templates.TemplateResponse(
        request=request, name="drivers/add-driver.html", context={'form':form}
    )
    
    
@router.get('/drivers/', response_class=HTMLResponse)
async def get_drivers(request: Request):
    all_drivers = Drivers.get_drivers_list()
    return templates.TemplateResponse(
        request=request, name="drivers/query-driver.html", context={'drivers': all_drivers}
    )
    
@router.get('/drivers/{driver_id}', response_class=HTMLResponse)
async def get_driver(driver_id: str,request: Request):
    print(driver_id)
    driver = Drivers.get_driver(driver_id)
    return templates.TemplateResponse(
        request=request, name="drivers/view-driver.html", context={'driver': driver}
    )
    