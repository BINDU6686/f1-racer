from fastapi import APIRouter, Response
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from f1_racer.forms.user import LoginForm, RegisterForm
from f1_racer.models.users import Users


templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get('/', response_class=[HTMLResponse, RedirectResponse])
@router.post("/", response_class=[HTMLResponse, RedirectResponse])
async def login(request: Request):
    form_data = await request.form()
    form = LoginForm(form_data)
    print(form.data)
    if request.method == 'POST':
        user= await Users(email=form.data['email'], password=form.data['password']).authenticate()
        print(user['idToken'])
        response = RedirectResponse(url="/drivers", status_code=303)
        response.set_cookie(
            key="token",
            value=f"Bearer {user['idToken']}",
            httponly=True, 
            max_age=1800,
            expires=1800,
            samesite="lax",
            secure=False
        )
        response.set_cookie(
            key="userId",
            value=user['localId'],
            httponly=True, 
            max_age=1800,
            expires=1800,
            samesite="lax",
            secure=False
        )
 
        return response
    
    
    return templates.TemplateResponse(
            request=request, 
            name="authentication/login.html", 
            context={'form':form}
        )

@router.get('/register', response_class=[HTMLResponse, RedirectResponse])
@router.post("/register", response_class=[HTMLResponse, RedirectResponse])
async def register(request: Request):
    form_data = await request.form()
    form = RegisterForm(form_data)

    if not form.validate():
        return templates.TemplateResponse(
            request=request,
            name="authentication/register.html",
            context={"form": form, "errors": form.errors}
        )
    
    try:
        user = await Users(email=form.data['email'], password=form.data['password']).register_user()
        response = RedirectResponse(url="/", status_code=303)
        return response
    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="authentication/register.html",
            context={"form": form, "errors": [str(e)]}
        )
        
        
@router.get('/logout')
async def logout(response: Response):
    """
    Logout the user by clearing cookies.
    """
    response = Response(status_code=303)
    response.delete_cookie(key="token")
    response.delete_cookie(key="userId")
    response.headers["Location"] = "/"  
    return response