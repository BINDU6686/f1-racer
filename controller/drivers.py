from fastapi import APIRouter, Depends
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from f1_racer.constants import DriverAttribute
from f1_racer.forms.driver import DriverForm
from f1_racer.models.drivers import Drivers
from f1_racer.models.teams import Teams
from f1_racer.utils import get_query_builder_options

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get('/drivers/add')
@router.post("/drivers/add", response_class=HTMLResponse)
async def add_driver(request: Request):
    body = await request.form()
    form = DriverForm(body)
    teams = Teams.get_teams_list()
    team_choices = [(team['id'], team['team_name']) for team in teams]
    form.driver_belong_to_team.choices = team_choices
    if request.method == 'POST':
        if form.validate():
            model_data = form.data
            model_data["created_by"] = request.cookies.get("userId")

            model = Drivers(**model_data)
            message=model.add_driver()

    return templates.TemplateResponse(request=request,
                                      name="drivers/add-driver.html",
                                      context={'form': form})


@router.get('/drivers/', response_class=HTMLResponse)
async def get_drivers(request: Request):
    
    attribute = request.query_params.get('attribute',None)
    comparison = request.query_params.get('comparison',None)
    attr_value = request.query_params.get('value',None)
    print(attribute, comparison, attr_value)
    
    all_drivers = Drivers.get_drivers_list(attribute, comparison, attr_value)
    query_options = get_query_builder_options(DriverAttribute)
    
    return templates.TemplateResponse(request=request,
                                      name="drivers/query-driver.html",
                                      context={
                                          'drivers': all_drivers,
                                          'query_options': query_options
                                      })

@router.get('/drivers/get_comparison', response_class=HTMLResponse)
async def get_drivers_comparison(request: Request):
    """
    Fetch and compare drivers based on query parameters.
    """
    # Get driver names from query parameters
    driver1_name = request.query_params.get('driver1', None)
    driver2_name = request.query_params.get('driver2', None)
    
    # Fetch the list of all drivers
    all_drivers = Drivers.get_drivers_list()
    driver_names = [driver['driver_name'] for driver in all_drivers]  

    # Initialize variables
    driver1_details, driver2_details = None, None
    comparison = None

    if driver1_name and driver2_name:
        try:
            comparison_result = Drivers.get_drivers_comparison(driver1_name, driver2_name)
            if comparison_result and len(comparison_result) == 2:
                driver1_details, driver2_details = comparison_result[0], comparison_result[1]
                
                comparison = {}
                for stat in driver1_details.keys():
                    if stat not in ['driver_name', 'driver_belong_to_team', 'created_by']:
                        if stat == 'age':
                            comparison[stat] = 'Driver 1' if driver1_details[stat] < driver2_details[stat] else 'Driver 2'
                        else:
                            comparison[stat] = 'Driver 1' if driver1_details[stat] > driver2_details[stat] else 'Driver 2'
        except Exception as e:
            print(f"Error fetching driver comparison: {e}")

    return templates.TemplateResponse(
        name="drivers/comparison-drivers.html",
        context={
            'request': request,
            'drivers': driver_names,
            'driver1': driver1_details,
            'driver2': driver2_details,
            'comparison': comparison
        }
    )

    
@router.get('/drivers/{driver_id}', response_class=HTMLResponse)
async def get_driver(driver_id: str, request: Request):
    print(driver_id)
    driver = Drivers.get_driver(driver_id)
    driver['driver_id'] = driver_id
    return templates.TemplateResponse(request=request,
                                      name="drivers/view-driver.html",
                                      context={'driver': driver})


@router.get('/drivers/edit/{driver_id}', response_class=HTMLResponse)
@router.post('/drivers/edit/{driver_id}', response_class=HTMLResponse)
async def edit_driver(driver_id: str, request: Request):
    """
    Endpoint to edit a driver's details.
    """
    body = await request.form()
    form = DriverForm(body)

    teams = Teams.get_teams_list()
    team_choices = [(team['id'], team['team_name']) for team in teams]
    form.driver_belong_to_team.choices = team_choices

    driver_data = Drivers.get_driver(driver_id)

    if request.method == 'GET':
        if driver_data:
            for field_name in form.data.keys():
                if field_name in driver_data:
                    form[field_name].data = driver_data[field_name]

    if request.method == 'POST' and form.validate():
        model_data = form.data
        model_data["created_by"] = request.cookies.get("userId")

        driver = Drivers(**model_data)
        result = driver.edit_driver(driver_id)

        if "error" in result:
            return templates.TemplateResponse(request=request,
                                              name="drivers/edit-driver.html",
                                              context={
                                                  "form": form,
                                                  "error": result["error"]
                                              })
        return templates.TemplateResponse(request=request,
                                          name="drivers/edit-driver.html",
                                          context={
                                              "form":
                                              form,
                                              "success":
                                              "Driver updated successfully"
                                          })

    return templates.TemplateResponse(request=request,
                                      name="drivers/edit-driver.html",
                                      context={"form": form})


@router.post('/drivers/delete/{driver_id}', response_class=HTMLResponse)
async def delete_driver(driver_id: str, request: Request):
    """
    Endpoint to delete a driver.
    """
    result = Drivers.delete_driver(driver_id)

    if "error" in result:
        return RedirectResponse(url="/drivers/", status_code=303)

    # Reload the drivers list after deletion
    return RedirectResponse(url="/drivers/", status_code=303)



    
