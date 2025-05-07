from fastapi import FastAPI

from src.utils.db_session import get_session

from src.api.routes.llm import router as llm_router
from src.api.routes.data import router as data_router
from src.api.routes.ml import router as ml_router
from src.api.routes.system import router as system

app = FastAPI()
app.include_router(llm_router)
app.include_router(data_router)
app.include_router(ml_router)
app.include_router(system)
db = get_session()

