# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class MovieItemLoader(ItemLoader):
    # 自定义itemLoader
    default_output_processor = TakeFirst()


def get_year(value):
    match_re = re.match("(\d{4})", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums


class movieTopItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    top = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    play_able = scrapy.Field()
    star = scrapy.Field()
    title = scrapy.Field()
    image = scrapy.Field()
    image_path = scrapy.Field()
    comments_num = scrapy.Field()
    year = scrapy.Field()
    country = scrapy.Field()
    movie_type = scrapy.Field()
    director = scrapy.Field()
    actor = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """insert into movie_top(top,url,url_object_id,play_able,star,comments_num,title,image,year,
        country,movie_type,director,actor) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE 
        top=values(top), star=values(star), comments_num=values(comments_num) """
        params = (
            self["top"], self["url"], self["url_object_id"], self["play_able"], self["star"], self["comments_num"],
            self["title"], self["image"], self["year"], self["country"], self["movie_type"], self["director"],
            self["actor"]
        )

        return insert_sql, params
