#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.

# init file for a fastapi server
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers import config_router, existing_infrastructure_router, auth_router, deploy_router

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(config_router.router)
app.include_router(existing_infrastructure_router.router)
app.include_router(deploy_router.router)
app.include_router(auth_router.router)
