from fastapi import FastAPI
import uvicorn
import os
import sys
from fastapi.templating import Jinja2Templates
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from textSummarizer.pipeline.prediction import PredictionPipeline

text:staticmethod =" What is text summarization?"
app = FastAPI()
@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def training():
    try:
        os.system("python main.py")
        return Response("Training Successful")
    except Exception as e:
        return Response(f"Training Failed {e}")
    
@app.get("/predict")
async def predict_route(text)
    try:
        obj = PredictionPipeline()
        text = obj.predict(text)
        return Response(text)
    except Exception as e:
        raise e

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)