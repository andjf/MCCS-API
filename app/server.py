import logging
from datetime import datetime

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.llm.controller import router as llm_router
from app.query.controller import data_router, query_router

logging.basicConfig(level=logging.INFO)

app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "https://marineshrink.info",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("app/static/favicon.ico")


@app.get("/")
def home():
    return {
        "status": "up",
        "path": "/",
        "timestamp": datetime.now(),
    }


app.include_router(query_router)
app.include_router(data_router)
app.include_router(llm_router)

if __name__ == "__main__":
    uvicorn.run("app/server:app", host="localhost", port=8000, reload=True)
