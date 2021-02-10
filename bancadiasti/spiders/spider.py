import re

import scrapy
from scrapy.exceptions import CloseSpider

from scrapy.loader import ItemLoader
from ..items import BancadiastiItem
from itemloaders.processors import TakeFirst


class BancadiastiSpider(scrapy.Spider):
	name = 'bancadiasti'
	start_urls = ['https://bancadiasti.it/category/news/']
	page = 1

	def parse(self, response):
		post_links = response.xpath('//article//h5/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		self.page += 1
		next_page = f'https://bancadiasti.it/category/news/page/{self.page}/'

		if not post_links:
			raise CloseSpider('no more pages')

		yield response.follow(next_page, self.parse)


	def parse_post(self, response):
		title = response.xpath('//h2[@class="elementor-heading-title elementor-size-large"]/text()').get()
		description = response.xpath('//section[@class="ob-is-breaking-bad elementor-section elementor-top-section elementor-element elementor-element-179ca93e elementor-reverse-mobile elementor-section-boxed elementor-section-height-default elementor-section-height-default"]//div[@class="elementor-element elementor-element-133980f4 elementor-widget elementor-widget-theme-post-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="elementor-icon-list-text elementor-post-info__item elementor-post-info__item--type-custom"]/text()').get()

		item = ItemLoader(item=BancadiastiItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
