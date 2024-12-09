import os
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import quote

cities = ["Mont Saint Michel","St Malo","Bayeux","Le Havre","Rouen",
"Paris","Amiens","Lille","Strasbourg","Chateau du Haut Koenigsbourg",
"Colmar","Eguisheim","Besancon","Dijon","Annecy","Grenoble","Lyon",
"Gorges du Verdon","Bormes les Mimosas","Cassis","Marseille","Aix en Provence",
"Avignon","Uzes","Nimes","Aigues Mortes","Saintes Maries de la mer","Collioure",
"Carcassonne","Ariege","Toulouse","Montauban","Biarritz","Bayonne","La Rochelle"]

class BookingSpider(scrapy.Spider):
    name = "Booking"
    
    def start_requests(self):
        for city in cities:
            
            encoded_city = quote(city)
            start_urls = (f'https://www.booking.com/searchresults.fr.html?ss={encoded_city}%2C+France'
                    '&label=gen173nr-1BCAEoggI46AdIM1gEaE2IAQGYAQ24ARjIAQzYAQHoAQGIAgGoAgS4AtKW17kGwAIB0gIkY2UyYTM0MTgtMzI5Ny00MWYyLTlhYTAtMTI5MTY2YjhlMTdj2AIF4AIB'
                    '&lang=fr&sb=1&src_elem=sb&src=index'
                    '&checkin=2024-11-18&checkout=2024-11-22&group_adults=2&no_rooms=1&group_children=0')
            
            yield scrapy.Request(url=start_urls, callback=self.parse, meta={'city': city})
    
    def parse(self, response):
        city = response.meta['city']  
        
        for item in response.css('div[data-testid="property-card"]'):
            hotel_name = item.css('[data-testid="title"]::text').get()
            link = item.css('a::attr(href)').get()
            review_score = item.css('div[data-testid="review-score"] div.ac4a7896c7::text').get()
            address = item.css('span[data-testid="address"]::text').get()
            
            if review_score:
                review_score = review_score.split()[-1]
            
            yield {    
                
                'address': address,      
                'hotel_name': hotel_name,
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
