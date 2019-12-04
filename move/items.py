# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MoveItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    href = scrapy.Field()
    img = scrapy.Field()
    video = scrapy.Field()
    content = scrapy.Field()
    details_title = scrapy.Field()
    number = scrapy.Field()
    status = scrapy.Field()
    result = scrapy.Field()
    des = scrapy.Field()
    start_urls = scrapy.Field()
    page = scrapy.Field()
    time = scrapy.Field()
    onei = scrapy.Field()
    create_time = scrapy.Field()
    score = scrapy.Field()
    type = scrapy.Field()
    year = scrapy.Field()
    actor = scrapy.Field()
    director = scrapy.Field()
    js = scrapy.Field()
    platform = scrapy.Field()
    is_update = scrapy.Field()
    update_title = scrapy.Field()
    video_list = scrapy.Field()
    title = scrapy.Field()
    move_id = scrapy.Field()
    type = scrapy.Field()
    pass
class toutiaoItem(scrapy.Item):

    pass
class MeijuttItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    href = scrapy.Field()
    img = scrapy.Field()
    video = scrapy.Field()
    content = scrapy.Field()
    details_title = scrapy.Field()
    number = scrapy.Field()
    status = scrapy.Field()
    result = scrapy.Field()
    des = scrapy.Field()
    start_urls = scrapy.Field()
    page = scrapy.Field()
    time = scrapy.Field()
    create_time = scrapy.Field()
    score = scrapy.Field()
    type = scrapy.Field()
    year = scrapy.Field()
    actor = scrapy.Field()
    director = scrapy.Field()
    js = scrapy.Field()
    platform = scrapy.Field()
    is_update = scrapy.Field()
    update_title = scrapy.Field()
    video_list = scrapy.Field()
    title = scrapy.Field()
    move_id = scrapy.Field()
    type = scrapy.Field()

    pass
class MeijuttUpdateItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    href = scrapy.Field()
    img = scrapy.Field()
    video = scrapy.Field()
    content = scrapy.Field()
    details_title = scrapy.Field()
    number = scrapy.Field()
    status = scrapy.Field()
    result = scrapy.Field()
    des = scrapy.Field()
    start_urls = scrapy.Field()
    page = scrapy.Field()
    time = scrapy.Field()
    create_time = scrapy.Field()
    score = scrapy.Field()
    type = scrapy.Field()
    year = scrapy.Field()
    actor = scrapy.Field()
    director = scrapy.Field()
    js = scrapy.Field()
    platform = scrapy.Field()
    is_update = scrapy.Field()
    update_title = scrapy.Field()
    move_id = scrapy.Field()
    video_list = scrapy.Field()
    title = scrapy.Field()
    pass