from fastapi import FastAPI
from core.config import settings
from api.v1.api import api_router
import uvicorn

app = FastAPI(title='API RESTFULL com Autenticação e Autorização')

app.include_router(api_router, prefix=settings.API_VERSION)

@app.get("/")
def read_root():
    return {"message": "API está funcionando"}



if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=7000, log_level='info', reload=True)