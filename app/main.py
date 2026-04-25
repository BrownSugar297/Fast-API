from fastapi import FastAPI
from . routers import stoners,locals,auth
from . config import settings


app=FastAPI()

app.include_router(stoners.router)
app.include_router(locals.router)
app.include_router(auth.router)

  





