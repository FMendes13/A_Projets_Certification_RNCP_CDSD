import os
import json
import logging
import scrapy
from scrapy.crawler import CrawlerProcess

class BookingSpider_details(scrapy.Spider):
    name = "Booking_details"

    def start_requests(self):
        input_file = '/Users/fredericmendessemedo/Desktop/Projets - Full Stack/Jedha_Bootcamp_Exo_n_Projets/Scrapping_results/test.json'
        try:
            with open(input_file, 'r') as f:
                hotels = json.load(f)
                for hotel in hotels:
                    url = hotel.get('url')
                    if url:
                        yield scrapy.Request(url=url, callback=self.parse, meta={'hotel_name': hotel['hotel_name']})
        except Exception as e:
            self.logger.error(f"Error loading JSON file: {e}")

    def parse(self, response):
        hotel_name = response.meta['hotel_name']

        for item in response.css('#hotelTmpl'):
            latlng = item.css('::attr(data-atlas-latlng)').get()
            hotel_description = item.css('[data-testid="property-description"]::text').get()
        
        if latlng:
            latitude, longitude = latlng.split(',')
        else:
            latitude, longitude = None, None

        yield {
            'hotel_name': hotel_name,
            'latitude': latitude,
            'longitude': longitude,
            'hotel_description': hotel_description,
        }

output_dir = '/Users/fredericmendessemedo/Desktop/Projets - Full Stack/Jedha_Bootcamp_Exo_n_Projets/Scrapping_results'
filename = "test_details.json"
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

process.crawl(BookingSpider_details)
process.start()
