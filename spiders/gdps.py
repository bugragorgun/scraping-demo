import scrapy
import logging

class GdpsSpider(scrapy.Spider):
    name = 'gdps'
    allowed_domains = ['worldpopulationreview.com']
    start_urls = ['https://www.worldpopulationreview.com/countries/countries-by-national-debt/']

    def parse(self, response):
        countries = response.xpath('//table/tbody/tr')
        for country in countries:
            name = country.xpath(".//td[1]/a/text()").get()
            link = country.xpath(".//td[1]/a/@href").get()
            gdp = country.xpath(".//td[2]/text()").get()

            # yield{
            #     'name': name,
            #     'gdp': gdp,
            #     'link': link
            # }
            yield response.follow(url=link, callback=self.parse_bd, meta={'name':name, 'gdp':gdp})
            # absolute_url = f"https://worldpopulationreview.com{link}"

            # absolute_url = response.urljoin(link)
            # yield scrapy.Request(url=absolute_url, callback=self.parse_bd, meta={'name':name, 'gdp':gdp})
            

    def parse_bd(self, response):
        name = response.request.meta['name']
        gdp = response.request.meta['gdp']
        # rows = response.xpath('//*[@id="popClock"]/div/div[1]/div/div/table/tbody')
        rows = response.xpath("(//table[@class='table table-striped'])[1]/tbody")
        for row in rows:
            births = row.xpath(".//tr[3]/td[@class='number']/text()").get()
            deaths = row.xpath(".//tr[4]/td[@class='number']/text()").get()
            yield{
                'name': name,
                'gdp': gdp,
                'births': births,
                'deaths': deaths
            }
