import logging
from datetime import datetime

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse

from llm.controller import router as llm_router
from query.controller import router as query_router

logging.basicConfig(level=logging.INFO)

app = FastAPI()


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")


@app.get("/")
def home():
    return {
        "status": "up",
        "timestamp": datetime.now(),
    }


app.include_router(query_router)
app.include_router(llm_router)

if __name__ == "__main__":
    uvicorn.run("server:app", host="localhost", port=8000, reload=True)
