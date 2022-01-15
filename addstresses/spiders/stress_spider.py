import scrapy
import urllib
from scrapy.loader import ItemLoader
from helpers import mark_stress
from addstresses.items import StressspiderItem


class StressSpider(scrapy.Spider):
    name = 'stressspider'
    custom_settings = {
        'FEED_URI': 'stresses.csv'
    }
    handle_httpstatus_list = [404]

    def __init__(self, *args, **kwargs):
        super(StressSpider, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('start_url')
        if self.start_urls == None:
            self.start_urls = ["https://xn----8sbhebeda0a3c5a7a.xn--p1ai/%D0%B2-%D1%81%D0%BB%D0%BE%D0%B2%D0%B5-%D0%B3%D0%BE%D1%81%D0%BF%D0%BE%D0%B4%D0%B0/"]

    def start_requests(self):
        """

        """
        urls = self.start_urls
        print(f'GETTING URLS {self.start_urls}')
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        word_of_interest = urllib.parse.unquote(response.url)[49:-1]
        if response.status == 404:
            warning = f'\n\n\nWARNING: {word_of_interest} failed\n\n\n'
            self.logger.warning(warning)
            l = ItemLoader(item=StressspiderItem(), response=response)
            l.add_value('stressed', word_of_interest)
            l.add_value('clean', word_of_interest)
            yield l.load_item()
        else:
            # will output items with a clean (unstressed) version and a stressed version
            explanations = response.xpath('//div[@class="word"]').getall()
            """
            creates a list of the HTML elements containing the explanation of the
            stress, e.g.,
            ['<div class="word">\n\t\t\t<b>I.</b> горы́\n\t\t\t\t\t\t\t— родительный
            падеж слова гора\t\t\t\t\t</div>',
            '<div class="word">\n\t\t\t<b>II.</b> го́ры\n\t\t\t\t\t\t\t—
            множественное число слова гора\t\t\t\t\t</div>']
            """
            stresses = response.xpath(
                "//div[@class='rule']").getall()
            """
            Creates a list of the HTML elements containing the stress, e.g.,
            ['<div class="rule ">\n\t\n\t\t В указанном выше варианте ударение
            падает на слог с буквой Ы — гор<b>Ы</b>. \n\t\t\t</div>',
            '<div class="rule ">\n\t\n\t\t В таком варианте ударение следует
            ставить на слог с буквой О — г<b>О</b>ры. \n\t\t\t</div>']
            """
            if len(stresses) > 1:
                # if there is more than one stress variant, add all options
                for line in stresses:
                    l = ItemLoader(item=StressspiderItem(), response=response)
                    l.add_value('stressed', mark_stress(line))
                    print(f'added {mark_stress(line)} and {word_of_interest}')
                    l.add_value('clean', word_of_interest)
                    yield l.load_item()
            else:
                target_word_stressed_list = mark_stress(stresses[0])
                # check to see if multiple options were included in the same div
                # as for some words with multiple acceptable variants, both
                # options are in the same div (e.g. держитесь)
                if len(target_word_stressed_list) > 1:
                    assert len(target_word_stressed_list) == 2
                    l1 = ItemLoader(item=StressspiderItem(),
                                    response=response)
                    l2 = ItemLoader(item=StressspiderItem(),
                                    response=response)
                    l1.add_value('stressed', target_word_stressed_list[0])
                    print(f'added {target_word_stressed_list[0]} and {word_of_interest}')
                    l1.add_value('clean', word_of_interest)
                    l2.add_value('stressed', target_word_stressed_list[1])
                    print(f'added {target_word_stressed_list[1]} and {word_of_interest}')
                    l2.add_value('clean', word_of_interest)
                    for item in (l1.load_item(), l2.load_item()):
                        yield item
                else:
                    l = ItemLoader(item=StressspiderItem(), response=response)
                    # if only one option for stress exists, add it
                    stressed_line = stresses[0]
                    # isolate target word and mark stress with color html tag
                    target_word_stressed_list = mark_stress(stressed_line)
                    l.add_value('stressed', target_word_stressed_list[0])
                    l.add_value('clean', word_of_interest)
                    print(f'added {target_word_stressed_list[0]} and {word_of_interest}')
                    yield l.load_item()
