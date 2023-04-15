from fastapi import FastAPI, Request
from sqlDataAccess import sqlDataAccess

app = FastAPI()
sql = sqlDataAccess()

# create middleware
@app.on_event("startup")
async def startup():
	# connect to database
    await sql.connect()

# create api end-point
@app.get("/findNews")
async def findNews(content: str):
	result = await sql.execute_storedProcedure('psGetNews', [content])
	return {"status": "success",
			"persons": result}

@app.get("/reportData")
async def reportData():
	pass

@app.post("/insertData")
async def insertData(request: Request):
	payload = await request.json()
	pass

@app.get("/getNews")
async def findNews(content: str):
	result = await sql.execute_storedProcedure('psGetNews', [None])
	return {"status": "success",
			"persons": result}
