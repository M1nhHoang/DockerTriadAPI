from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler
import requests, json, pytz

class DataCrawling:
	def __init__(self):
		# load config
		with open('./config.json') as f:
			config = json.load(f)

		crawl_config = config["crawl"]
		self.crawl_delay = crawl_config["delay"]
		self.page_number = crawl_config["number_of_pages"]
		self.data_crawling = None
		self.scheduler = BackgroundScheduler()

	def timer_crawl(self):
		# start scheduler to run crawling at specific times
		self.scheduler.add_job(self.crawling, 'cron', hour=self.crawl_delay["hour"], minute=self.crawl_delay["minute"], timezone=pytz.timezone('Asia/Bangkok'))
		self.scheduler.start()

	def crawling(self):
		# create a dictionary to store the scraped data
		data = {
			"data_crawling": []
		}

		# crawl pages
		for i in range(1, self.page_number + 1):
			if i == 1:
				rs = requests.get('https://tuoitre.vn/tin-moi-nhat.htm')
			else:
				rs = requests.get(f'https://tuoitre.vn/timeline/0/trang-{i}.htm')
				
			soup = BeautifulSoup(rs.text, 'html.parser')
			news_items = soup.select(".box-category-item")
			for item in news_items:
				# extract data from the HTML tags
				time_stamp = item.span['title']
				news_url = item.select("a")[0]['href']
				news_id = news_url[news_url.rfind('-')+1:-4]
				image = item.select("a")[0].img['src'] if item.select("a")[0].img else item.select("a")[0].video['poster']
				category = item.select("a")[1].string
				title = item.select("a")[2].string
				content = item.p.string

				# add data to the dictionary
				data["data_crawling"].append({
					"time_stamp": time_stamp, 
					"news_url": news_url, 
					"news_id": news_id, 
					"image": image, 
					"category": category, 
					"title": title, 
					"content": content
				})

		# store the scraped data in the object's data_crawling attribute
		self.data_crawling = data
		# call insertData() to insert the data into a database
		self.send_data()

	def send_data(self):
		# send a POST request to a URL with the scraped data in JSON format
		requests.post('http://models:1919/insertData', data=json.dumps(self.data_crawling))