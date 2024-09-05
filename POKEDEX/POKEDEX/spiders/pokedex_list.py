import scrapy
from ..items import PokedexItem

class PokedexListSpider(scrapy.Spider):
    name = "pokedex_list"
    start_urls = ["https://pokemondb.net/pokedex/all"]
    item = PokedexItem()

    queries = {
        'name': 'td:nth-child(2) a::text',
        'subname': 'td:nth-child(2) small::text',
        'attack': 'td:nth-child(6) ::text'
    }

    def parse(self, response):
        all_tables = response.css('table#pokedex tr')
        i = 0
        for pokemon in all_tables:
            for key, value in self.queries.items():
                self.item[key] = pokemon.css(value).get()
            if i > 1195:
                break
            i = i + 1
            yield self.item
