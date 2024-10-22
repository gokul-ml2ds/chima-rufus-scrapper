# api/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from RufusClient.client import RufusClient
import json

app = FastAPI(
    title="Rufus API",
    description="API for Rufus Web Data Extraction Tool",
    version="1.0"
)

class ScrapeRequest(BaseModel):
    url: HttpUrl
    instructions: str

class ScrapeResponse(BaseModel):
    documents: dict

@app.post("/scrape", response_model=ScrapeResponse)
def scrape(scrape_request: ScrapeRequest):
    try:
        client = RufusClient(user_prompt=scrape_request.instructions)
        documents = client.scrape(scrape_request.url)
        return ScrapeResponse(documents=documents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scrape/download")
def scrape_and_download(scrape_request: ScrapeRequest):
    try:
        client = RufusClient(user_prompt=scrape_request.instructions)
        documents = client.scrape(scrape_request.url)
        # Save to a file
        file_path = "output.json"
        with open(file_path, 'w') as f:
            json.dump(documents, f, indent=4)
        return {"message": "Scraping completed. Data saved to output.json."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))