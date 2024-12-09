import os
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import quote


class BookingSpider(scrapy.Spider):
    
    name = "Booking"
    start_urls=['https://www.booking.com/searchresults.fr.html?ss=Paris%2C+France&ssne=Eurotunnel+France&ssne_untouched=Eurotunnel+France&label=gen173nr-1BCAEoggI46AdIM1gEaE2IAQGYAQ24ARjIAQzYAQHoAQGIAgGoAgS4AtKW17kGwAIB0gIkY2UyYTM0MTgtMzI5Ny00MWYyLTlhYTAtMTI5MTY2YjhlMTdj2AIF4AIB&sid=0711f708ec72522233342c15a48d0d96&aid=304142&lang=fr&sb=1&src_elem=sb&src=index&dest_id=-1456928&dest_type=city&checkin=2024-11-18&checkout=2024-11-22&group_adults=2&no_rooms=1&group_children=0']
    
    def parse(self, response):
        for item in response.css('[data-testid="property-card"]'):
            hotel_name = item.css('[data-testid="title"]::text').get()
            link = item.css('a::attr(href)').get()
            review_score = item.css('div[data-testid="review-score"] div.ac4a7896c7::text').get()
            address = item.css('span[data-testid="address"]::text').get()
                
            if review_score:
                review_score = review_score.split()[-1]
                
            yield {        
                'hotel_name': hotel_name,
                'address': address,    
                'review_score': review_score,
                'url': link,
                        }


output_dir = '/Users/fredericmendessemedo/Desktop/Projets - Full Stack/Jedha_Bootcamp_Exo_n_Projets/Scrapping_results'
filename = "test.json"
file_path = os.path.join(output_dir, filename)


if os.path.exists(file_path):
    os.remove(file_path)


process = CrawlerProcess(settings={
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0 Safari/537.36',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        file_path: {"format": "json"},
    },
})

process.crawl(BookingSpider)
process.start()
