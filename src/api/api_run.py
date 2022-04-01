#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.

import uvicorn
from src.api import app

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
