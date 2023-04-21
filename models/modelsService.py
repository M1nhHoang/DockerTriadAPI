import aiomysql
import json

class sqlDataAccess:
  # connect database using aiomysql for async
  def __init__(self):
    """
    Initializes the class and loads the database config from a JSON file.

    Args:
      None.

    Returns:
      None.
    """
    # load config
    with open('./config.json') as f:
      config = json.load(f)
      
    database_config = config['database']
    self.host = database_config['host']
    self.port = database_config['port']
    self.username = database_config['username']
    self.password = database_config['password']
    self.database_name = database_config['database_name']
    self.pool = None

  async def connect(self):
    """
    Connects to the MySQL database using config.

    Args:
      None.

    Returns:
      None.
    """
    # create pool
    self.pool = await aiomysql.create_pool(
        host = self.host,
        port = self.port,
        user = self.username,
        password = self.password,
        db = self.database_name,
        autocommit = True
      )

  async def execute(self, sqlQuery):
    """
    Executes a SQL query string and returns the results.

    Args:
      sqlQuery: Sql query string.

    Returns:
      A tuple return for select query or show number of row effect.
    """
    async with self.pool.acquire() as conn:
      async with conn.cursor() as cur:
        await cur.execute(sqlQuery)
        result = await cur.fetchall()
        return result if result else f"{cur.rowcount} rows affected"

  async def execute_storedProcedure(self, psName, values = ()):
    """
    Executes a stored Procedure and returns the results.

    Args:
      psName: Name of the procedure.
      values: A list or tuple values to pass to the stored procedure.

    Returns:
      A tuple return for select query or show number of row effect.
    """
    # check values if values not list rise error
    if not isinstance(values, (list, tuple)):
      raise Exception("Argument 2 must be list or tuple")

    async with self.pool.acquire() as conn:
      async with conn.cursor() as cur:
        await cur.callproc(psName, values)
        result = await cur.fetchall()
        return result if result else f"{cur.rowcount} rows affected"

class modelService:
  def __init__(self):
    self.sqlQuery = None

  async def insertStringQuery(self, data):
    self.sqlQuery = "INSERT INTO tb_news (news_id, news_url, title, category, content, image, time_stamp) VALUES" 
    for items in data['data_crawling']:
      content_value = items["content"].replace('"', '\\"')
      title_value = items["title"].replace('"', '\\"')
      self.sqlQuery += f'("{items["news_id"]}", "{items["news_url"]}", "{title_value}", "{items["category"]}", "{content_value}", "{items["image"]}", "{items["time_stamp"]}"),'

    self.sqlQuery = self.sqlQuery[:-1] + ' ON DUPLICATE KEY UPDATE news_id = VALUES(news_id), news_url = VALUES(news_url), title = VALUES(title), category = VALUES(category), content = VALUES(content), image = VALUES(image),time_stamp = VALUES(time_stamp);'

  async def getReportJSON(self, reportList):
    result = []
    for item in reportList:
      result.append({
          "datetime": str(item[0]),
          "insert": str(item[1]),
          "update": str(item[2]),
          "delete": str(item[3]),
          "duplicate": str(item[4])
      })
    return json.dumps(result)