# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst

class MatchItem(scrapy.Item):
    match_id = scrapy.Field(output_processor=TakeFirst())
    map_name = scrapy.Field(output_processor=TakeFirst())
    event = scrapy.Field(output_processor=TakeFirst())
    date = scrapy.Field(output_processor=TakeFirst())

class TeamItem(scrapy.Item):
    match_item = scrapy.Field(output_processor=TakeFirst())
    team_name = scrapy.Field(output_processor=TakeFirst())
    score = scrapy.Field(output_processor=TakeFirst())

class PlayerItem(scrapy.Item):
    team_item = scrapy.Field(output_processor=TakeFirst())
    player_nick = scrapy.Field(output_processor=TakeFirst())
    kills = scrapy.Field(output_processor=TakeFirst())
    assists = scrapy.Field(output_processor=TakeFirst())
    deaths = scrapy.Field(output_processor=TakeFirst())
    kast = scrapy.Field(output_processor=TakeFirst())
    adr = scrapy.Field(output_processor=TakeFirst())
    rating = scrapy.Field(output_processor=TakeFirst())