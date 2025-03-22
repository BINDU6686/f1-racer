from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from f1_racer.forms.user import LoginForm
from f1_racer.firestore import authenticate

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get('/', response_class=[HTMLResponse, RedirectResponse])
@router.post("/", response_class=[HTMLResponse, RedirectResponse])
async def login(request: Request):
    form_data = await request.form()
    form = LoginForm(form_data)
    print(form.data)
    if request.method == 'POST':
        user= await authenticate(form.data['email'], form.data['password'])
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
    