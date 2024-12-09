import os
import logging
import scrapy
from scrapy.crawler import CrawlerProcess


class BookingSpider_details(scrapy.Spider):
    
    name = "Booking_details"
    start_urls=['https://www.booking.com/hotel/fr/campanile-rouen-mermoz.fr.html?label=gen173nr-1BCAEoggI46AdIM1gEaE2IAQGYAQ24AQfIAQ3YAQHoAQGIAgGoAgO4Ao7E6bkGwAIB0gIkMWU4NmQ4OTAtYmZmMC00M2FiLWFmODctODRmYWExNTkyNTE52AIF4AIB&sid=e22d357d0fce5fb130210d87d929b545&aid=304142&ucfs=1&arphpl=1&checkin=2024-11-18&checkout=2024-11-22&dest_id=-1462807&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&hpos=1&hapos=1&sr_order=popularity&srpvid=5f4c980e50f41b01&srepoch=1731879457&all_sr_blocks=270823005_106179857_2_2_0&highlighted_blocks=270823005_106179857_2_2_0&matching_block_id=270823005_106179857_2_2_0&sr_pri_blocks=270823005_106179857_2_2_0__29857&from_sustainable_property_sr=1&from=searchresults']
    
    def parse(self, response):
        for item in response.css('#hotelTmpl'):
            latlng = item.css('::attr(data-atlas-latlng)').get()
            hotel_description = response.css('[data-testid="property-description"]::text').get()
        
        if latlng:
            latitude, longitude = latlng.split(',')
        else:
            latitude, longitude = None, None
                
        yield {   
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
