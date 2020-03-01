import scrapy
from scrapy.loader import ItemLoader
from hltv_crawler.items import MatchItem, TeamItem, PlayerItem

MATCHES_XPATH = '//table[@class="stats-table matches-table no-sort"]//tr/td[@class="date-col"]/a/@href'

class HLTVSpider(scrapy.Spider):
    name = "hltv"
    start_urls = ["https://www.hltv.org/stats/matches?startDate=all&rankingFilter=Top20"]

    def get_match_item(self, response):
        match_info_selector = response.xpath('//div[@class="match-info-box"]')
        loader = ItemLoader(item=MatchItem(), selector=match_info_selector)
        map_name = match_info_selector.xpath('./text()[normalize-space()]')[0].get().strip()
        loader.add_value('map_name', map_name)
        loader.add_xpath('event', '//a[@class="block text-ellipsis"]/text()')
        loader.add_xpath('date', '//div[@class="small-text"]/span/text()')
        match_id = response.xpath('//a[@class="stats-top-menu-item stats-top-menu-item-link selected"]/@href').get().split('/')[4]
        loader.add_value('match_id', match_id)
        return loader.load_item()
    
    def get_team_item(self, match_item, selector):
        loader = ItemLoader(item=TeamItem(), selector=selector)
        loader.add_xpath('team_name', './a[@class="block text-ellipsis"]/text()')
        loader.add_css('score', 'div.bold::text')
        loader.add_value('match_item', match_item)
        return loader.load_item()

    def get_both_teams_items(self, match_item, response):
        left_team_sel = response.css('div.team-left')[0]
        right_team_sel = response.css('div.team-right')[0]
        left_team_item = self.get_team_item(match_item, left_team_sel)
        right_team_item = self.get_team_item(match_item, right_team_sel)
        return (left_team_item, right_team_item)

    def get_player_stats(self, team_item, selector):
        loader = ItemLoader(item=PlayerItem(), selector=selector)
        loader.add_xpath('player_nick', './td[@class="st-player"]/a/text()')
        loader.add_xpath('kills', './td[@class="st-kills"]/text()')
        loader.add_xpath('assists', './td[@class="st-assists"]/text()')
        loader.add_xpath('deaths', './td[@class="st-deaths"]/text()')
        loader.add_xpath('kast', './td[@class="st-kdratio"]/text()')
        loader.add_xpath('adr', './td[@class="st-adr"]/text()')
        loader.add_xpath('rating', './td[@class="st-rating"]/text()')
        loader.add_value('team_item', team_item)
        return loader.load_item()

    def get_team_players_stats(self, team_item, table_selector, response):
        players = []
        for player in table_selector.xpath('.//tr')[1:]:
            players.append(self.get_player_stats(team_item, player))
        return players

    def get_all_players_stats(self, left_team_item, right_team_item, response):
        players_stats = response.xpath('//table[@class="stats-table"]')
        left_team_players_stats = self.get_team_players_stats(left_team_item, players_stats[0], response)
        right_team_players_stats = self.get_team_players_stats(right_team_item, players_stats[1], response)
        return left_team_players_stats + right_team_players_stats        

    def parse_match(self, response):
        match_item = self.get_match_item(response)
        left_team_item, right_team_item = self.get_both_teams_items(match_item, response)
        all_players = self.get_all_players_stats(left_team_item, right_team_item, response)
        for player in all_players:
            yield player

    def parse(self, response):
        for match in response.xpath(MATCHES_XPATH).extract():
            yield response.follow(match, callback=self.parse_match)
        for page in response.css("a.pagination-next"):
            yield response.follow(page, callback=self.parse)