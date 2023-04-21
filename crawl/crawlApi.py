from crawlService import DataCrawling
from fastapi import FastAPI

app = FastAPI()
crawling = DataCrawling()

# create middleware
@app.on_event("startup")
def startup():
	# start scraping data cyclically
    crawling.timer_crawl()

# create api end-point
@app.post("/currentCrawl")
def currentCrawl():
	crawling.crawling()
	return {"status": "success"}
