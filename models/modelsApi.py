from fastapi import FastAPI, Request
from modelsService import sqlDataAccess, modelService
from fastapi.responses import JSONResponse
import json

app = FastAPI()
sql = sqlDataAccess()
service = modelService()

# create middleware
@app.on_event("startup")
async def startup():
	# connect to database
    await sql.connect()


# create api end-point
# tìm kiếm tin tức
@app.get("/sreach")
async def findNews(content: str):
	result = await sql.execute_storedProcedure('psGetNews', [content])
	return {"status": "success",
			"result": json.dumps(result, default=str)}

# thống kê dữ liệu
@app.get("/reportData")
async def reportData():
	result = await service.getReportJSON(await sql.execute_storedProcedure('psGetLog'))
	return {"status": "success",
			"result": json.loads(result)}

# insert maunal
@app.post("/insertData")
async def insertData(request: Request):
	payload = await request.json()
	await service.insertStringQuery(payload)
	result = await sql.execute(service.sqlQuery)
	return {"status": "success"}

# lấy toàn bộ tin tức
@app.get("/getNews")
async def findNews():
	result = await sql.execute_storedProcedure('psGetNews', [None])
	return {"status": "success",
			"result": result}
