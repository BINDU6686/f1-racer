from fastapi import APIRouter, Depends
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from f1_racer.constants import TeamAttribute
from f1_racer.forms.team import TeamForm
from f1_racer.models.teams import Teams
from f1_racer.utils import get_query_builder_options

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get('/teams/add')
@router.post("/teams/add", response_class=HTMLResponse)
async def add_team(request: Request):
    body = await request.form()
    form = TeamForm(body)
    if request.method == 'POST':
        if form.validate():
            model_data = form.data
            model_data["created_by"] = request.cookies.get("userId")

            model = Teams(**model_data)
            model.add_team()

    return templates.TemplateResponse(request=request,
                                     name="teams/add-team.html",
                                     context={'form': form})


@router.get('/teams/', response_class=HTMLResponse, name="get_teams")
async def get_teams(request: Request):
    
    attribute = request.query_params.get('attribute')
    comparison = request.query_params.get('comparison')
    attr_value = request.query_params.get('value')
    print(attribute, comparison, attr_value)
    
    all_teams = Teams.get_teams_list(attribute, comparison, attr_value)
    query_options = get_query_builder_options(TeamAttribute)
    
    return templates.TemplateResponse(request=request,
                                     name="teams/query-team.html",
                                     context={
                                         'teams': all_teams,
                                         'query_options': query_options
                                     })


@router.get('/teams/get_comparison', response_class=HTMLResponse)
async def get_teams_comparison(request: Request):
    """
    Fetch and compare Teams based on query parameters.
    """
    # Get driver names from query parameters
    team1_name = request.query_params.get('team1', None)
    team2_name = request.query_params.get('team2', None)
    print(team1_name, team2_name)
    
    # Fetch the list of all Teams
    all_teams = Teams.get_teams_list()
    team_names = [team['team_name'] for team in all_teams]  

    # Initialize variables
    team1_details, team2_details = None, None
    comparison = None

    if team1_name and team2_name:
        try:
            comparison_result = Teams.get_teams_comparison(team1_name, team2_name)
            if comparison_result and len(comparison_result) == 2:
                team1_details, team2_details = comparison_result[0], comparison_result[1]
                print('team1 details', team1_details)
                comparison = {}
                for stat in team1_details.keys():
                    if stat not in ['team_name', 'total_race_wins', 'total_constructor_titles']:
                        if stat == 'total_race_wins':
                            comparison[stat] = 'Team 1' if team1_details[stat] < team2_details[stat] else 'Team 2'
                        else:
                            comparison[stat] = 'Team 1' if team1_details[stat] > team2_details[stat] else 'Team 2'
        except Exception as e:
            print(f"Error fetching driver comparison: {e}")
            
    print(comparison)
    return templates.TemplateResponse(
        name="teams/comparison-teams.html",
        context={
            'request': request,
            'teams': team_names,
            'team1': team1_details,
            'team2': team2_details,
            'comparison': comparison
        }
    )

@router.get('/teams/{team_id}', response_class=HTMLResponse)
async def get_team(team_id: str, request: Request):
    print(team_id)
    team = Teams.get_team(team_id)
    team['team_id'] = team_id
    return templates.TemplateResponse(request=request,
                                     name="teams/view-team.html",
                                     context={'team': team})


@router.get('/teams/edit/{team_id}', response_class=HTMLResponse)
@router.post('/teams/edit/{team_id}', response_class=HTMLResponse)
async def edit_team(team_id: str, request: Request):
    """
    Endpoint to edit a team's details.
    """
    body = await request.form()
    form = TeamForm(body)

    team_data = Teams.get_team(team_id)

    if request.method == 'GET':
        if team_data:
            for field_name in form.data.keys():
                if field_name in team_data:
                    form[field_name].data = team_data[field_name]

    if request.method == 'POST' and form.validate():
        model_data = form.data
        model_data["created_by"] = request.cookies.get("userId")

        team = Teams(**model_data)
        result = team.edit_team(team_id)

        if "error" in result:
            return templates.TemplateResponse(request=request,
                                             name="teams/edit-team.html",
                                             context={
                                                 "form": form,
                                                 "error": result["error"]
                                             })
        return templates.TemplateResponse(request=request,
                                         name="teams/edit-team.html",
                                         context={
                                             "form": form,
                                             "success": "Team updated successfully"
                                         })

    return templates.TemplateResponse(request=request,
                                     name="teams/edit-team.html",
                                     context={"form": form})


@router.post('/teams/delete/{team_id}', response_class=HTMLResponse)
async def delete_team(team_id: str, request: Request):
    """
    Endpoint to delete a team.
    """
    result = Teams.delete_team(team_id)

    if "error" in result:
        return RedirectResponse(url="/teams/", status_code=303)

    # Reload the teams list after deletion
    return RedirectResponse(url="/teams/", status_code=303)