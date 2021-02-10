BOT_NAME = 'bancadiasti'

SPIDER_MODULES = ['bancadiasti.spiders']
NEWSPIDER_MODULE = 'bancadiasti.spiders'
FEED_EXPORT_ENCODING = 'utf-8'
LOG_LEVEL = 'ERROR'
DOWNLOAD_DELAY = 0

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
	'bancadiasti.pipelines.BancadiastiPipeline': 100,

}