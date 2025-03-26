
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


from f1_racer.controller import drivers, teams, authentication

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(drivers.router)
app.include_router(teams.router)
app.include_router(authentication.router)



# Reference code to include routers from different modules
# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )



