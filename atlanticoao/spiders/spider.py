import scrapy

from scrapy.loader import ItemLoader

from ..items import AtlanticoaoItem
from itemloaders.processors import TakeFirst


class AtlanticoaoSpider(scrapy.Spider):
	name = 'atlanticoao'
	start_urls = ['https://www.atlantico.ao/pt/institucional/noticias/Pages/home.aspx']

	def parse(self, response):
		post_links = response.xpath('//div[@class="row-sm-height"]//a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//center[@class="articleTitle"]/text()').get()
		description = response.xpath('//div[@class="articleContent"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//center[@class="articleDate"]/text()').get()

		item = ItemLoader(item=AtlanticoaoItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
