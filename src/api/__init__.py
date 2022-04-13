#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.

# init file for a fastapi server
import uvicorn
from fastapi import FastAPI

from routers import config_router, existing_infrastructure_router, auth_router

app = FastAPI()

app.include_router(config_router.router)
app.include_router(existing_infrastructure_router.router)
app.include_router(auth_router.router)
