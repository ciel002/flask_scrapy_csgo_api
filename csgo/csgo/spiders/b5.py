# -*- coding: utf-8 -*-
import json

import scrapy

from csgo.items import B5Item


class B5Spider(scrapy.Spider):
    name = 'b5'
    allowed_domains = ['b5csgo.com.cn']
    steamId = '186939639'
    page = 1
    b5_data_url = 'https://www.b5csgo.com.cn/personalCenterV2Controller/match.do?pageNum=' + str(
        page) + '&pageSize=20&steamId=' + steamId + '&matchClass=-1&favourites=-1&gameTime=&competitionName=&mapId=-1'
    start_urls = [
        'https://www.b5csgo.com.cn/personalCenterV2Controller/match.do?pageNum=1&pageSize=20&steamId=' + steamId + '&matchClass=-1&favourites=-1&gameTime=&competitionName=&mapId=-1']

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            method='POST',
            callback=self.parse,
            headers={'Content-Type': 'application/json;charset=utf-8'},
        )

    def parse(self, response):
        result = json.loads(response.text)
        for match in result['data']['items']:
            # 记录比赛数据
            item = B5Item()
            item['steamId'] = self.steamId
            item['map'] = match['mapName'].split("_")[-1]
            item['score'] = match['score']
            item['time'] = match['updateTime']
            # item['achievement'] = match['achievement']
            item['kda'] = match['kad']
            item['result'] = match['result']

            next_url = 'https://www.b5csgo.com.cn/api/matchDetail/personal/' + str(
                match['matchId']) + '/' + self.steamId
            item['url'] = next_url
            yield scrapy.Request(
                url=next_url,
                method='GET',
                callback=self.parse_detail,
                headers={'Content-Type': 'application/json;charset=utf-8'},
                meta={
                    'item': item
                },
            )
            current_page = result['data']['pageNum']
            if current_page < result['data']['pages']:
                current_page += 1
                b5_data_url = 'https://www.b5csgo.com.cn/personalCenterV2Controller/match.do?pageNum=' + str(
                    current_page) + '&pageSize=20&steamId=' + self.steamId + '&matchClass=-1&favourites=-1&gameTime=&competitionName=&mapId=-1'
                yield scrapy.Request(
                    url=b5_data_url,
                    method='POST',
                    callback=self.parse,
                    headers={'Content-Type': 'application/json;charset=utf-8'},
                )

    def parse_detail(self, response):
        result = json.loads(response.text)
        item = response.meta['item']
        item['rws'] = result['rws']
        item['rating'] = result['rating']
        item['damage'] = result['damage']
        item['awp'] = result['awp']
        item['firstKill'] = result['firstKill']
        yield item
