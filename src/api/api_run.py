#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.

import uvicorn
import os
import sys

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(root_folder)
from src.api import app

if __name__ == '__main__':
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=True)
