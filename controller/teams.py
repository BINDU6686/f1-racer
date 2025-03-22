from fastapi import APIRouter
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.post("/teams/add", response_class=HTMLResponse)
async def add_team(request: Request):
    return templates.TemplateResponse(
        request=request, name="teams/add-team.html"
    )
    
    
@router.get('/teams/', response_class=HTMLResponse)
async def get_teams_info(request: Request):
    return templates.TemplateResponse(
        request=request, name="teams/query-team.html"
    )