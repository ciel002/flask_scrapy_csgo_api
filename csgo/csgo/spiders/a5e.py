# -*- coding: utf-8 -*-
import json
import re

import scrapy

from csgo.items import A5EItem


class A5eSpider(scrapy.Spider):
    name = '5e'
    allowed_domains = ['5ewin.com']

    def __init__(self, domain='', *args, **kwargs):
        super(A5eSpider, self).__init__(*args, **kwargs)
        self.domain = domain
        self.url = 'https://www.5ewin.com/data/player/' + domain
        self.start_urls = [self.url]

    def close(spider, reason):
        return 1

    def parse(self, response):
        season_list = response.xpath("//div[@id='J_PlayerSeasonLine']//a/@href").extract()
        for season_url in season_list:
            if 's1' in season_url:
                yield scrapy.Request(
                    url=season_url,
                    callback=self.parse_season
                )

    def parse_season(self, response):
        match_list = response.xpath("//div[@id='match-tb']//tr")[1:]
        # 赛季
        year = str(re.findall(r".*/(\d+)", response.url)[0])
        # 该赛季的总比赛数量和每个比赛列表的比赛数量
        match_count = response.xpath("//ul[@class='stat-data']/li")[1].xpath("span/text()").extract_first()
        if str.isdigit(match_count):
            match_count = int(match_count)
        else:
            match_count = 200
        match_per_list = 10
        # 该赛季的总比赛列表页数
        match_page = int(match_count / match_per_list)
        name = response.xpath("//h1/span/text()").extract_first().strip()
        for i in range(2, match_page + 1):
            next_base_url = "https://www.5ewin.com/api/data/match_list/" + self.domain
            next_page_data = next_base_url + "?yyyy=" + year + "&page=" + str(i)
            yield scrapy.Request(
                url=next_page_data,
                callback=self.parse_json_data,
                meta={
                    'year': year,
                    'name': name
                }
            )

        for match in match_list:
            item = A5EItem()
            info = match.xpath("td")
            item['domain'] = self.domain
            item['time'] = year + "-" + info[2].xpath("text()").extract_first().split(" ")[0]
            item['map'] = info[4].xpath("text()").extract_first().split("_")[-1]
            item['score'] = info[5].xpath("text()").extract_first().strip()
            result = info[7].xpath("text()").extract_first()
            if result:
                item['result'] = result
            else:
                item['result'] = info[7].xpath("span/text()").extract_first()
            item['rws'] = info[8].xpath("text()").extract_first().strip()
            item['rating'] = info[9].xpath("text()").extract_first().strip()
            item['url'] = info[11].xpath('a/@href').extract_first()

            yield scrapy.Request(
                url=item['url'],
                callback=self.parse_detail,
                meta={
                    'name': name,
                    'item': item
                }
            )

    def parse_json_data(self, response):
        result = json.loads(response.text)
        name = response.meta['name']
        year = response.meta['year']
        if result['success'] is True:
            for match in result['data']:
                item = A5EItem()
                item['domain'] = self.domain
                item['time'] = year + "-" + match['start_time'].split(" ")[0]
                item['map'] = match['map'].split("_")[-1]
                item['score'] = match['score1'] + ":" + match['score2']
                item['result'] = "胜" if match['is_win'] is "1" else "负"
                item['result'] = "平" if match['score1']==match['score2'] else item['result']
                item['rws'] = match['rws']
                item['rating'] = match['rating']
                item['url'] = "https://www.5ewin.com/data/match/" + match['match_code']

                yield scrapy.Request(
                    url=item['url'],
                    callback=self.parse_detail,
                    meta={
                        'name': name,
                        'item': item
                    }
                )

    def parse_detail(self, response):
        item = response.meta['item']
        name = response.meta['name']
        player_list = response.xpath("//div[@id='match-data-list']//tr")[1:]
        for player in player_list:
            info = player.xpath('td')
            if name == info[1].xpath('a/span/text()').extract_first().strip():
                kill = info[2].xpath('text()').extract_first().strip()
                assist = info[3].xpath('text()').extract_first().strip()
                death = info[4].xpath('text()').extract_first().strip()
                item['kda'] = kill + "/" + death + "/" + assist
                item['headshot'] = info[5].xpath('text()').extract_first()
                item['firstKill'] = info[6].xpath('text()').extract_first()
                item['adr'] = info[9].xpath('text()').extract_first()
                yield item
