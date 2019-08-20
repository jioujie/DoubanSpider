# -*- coding: utf-8 -*-
from time import sleep
from urllib import parse

import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader

from items import movieTopItem, MovieItemLoader
from utils.common import get_md5


class MovietopSpider(scrapy.Spider):
    name = 'movieTop'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        movies = response.css("ol li")
        for movie in movies:
            sleep(0.03)
            item_loader = MovieItemLoader(item=movieTopItem(), selector=movie)

            url = movie.css(".pic a::attr(href)").extract_first()
            item_loader.add_css("url", ".pic a::attr(href)")
            item_loader.add_value("url_object_id", get_md5(url))
            able = movie.css(".hd span.playable::text").extract_first()
            if able:
                pass
            else:
                able = " "
            item_loader.add_value("play_able", able)
            item_loader.add_css("top", ".pic em::text")
            item_loader.add_css("title", ".hd a span:nth-child(1)::text")
            item_loader.add_css("star", ".rating_num::text")
            item_loader.add_css("image", ".pic img::attr(src)")
            item_loader.add_css("comments_num", ".star span:nth-child(4)::text")

            move = movie.css(".bd p")
            tag_p = move.xpath("text()[1]").extract()[0].strip()
            tag_m = move.xpath("text()[2]").extract()[0].strip()
            tag_p = tag_p.split('\xa0\xa0\xa0')
            item_loader.add_value("director", tag_p[0])
            try:
                item_loader.add_value("actor", tag_p[1])
            except:
                item_loader.add_value("actor", " ")
            tag_m = tag_m.split('\xa0/\xa0')

            item_loader.add_value("year", tag_m[0])
            item_loader.add_value("country", tag_m[1])
            item_loader.add_value("movie_type", tag_m[2])

            item = item_loader.load_item()
            yield item

        next_page = response.css('span.next a::attr(href)').extract_first()
        if next_page:
            yield Request(url=parse.urljoin(response.url, next_page), callback=self.parse, dont_filter=False)
