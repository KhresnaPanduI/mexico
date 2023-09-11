import  scrapy

class HotelSpider(scrapy.Spider):
    name = 'hotel_spider'
    start_url = 'https://www.tripadvisor.com/'
    country = 'Mexico'  # You can change this to any country

    def start_requests(self):
        # Step 3: Open https://www.tripadvisor.com/
        yield scrapy.Request(url=self.start_url, callback=self.search_activities)

    def search_activities(self, response):
        # Step 4: Input the text value of the search bar
        search_url = f"https://www.tripadvisor.com/Search?q={self.country}%20Hotels"
        yield scrapy.Request(url=search_url, callback=self.extract_country_code)

    def extract_country_code(self, response):
        # Step 5: Extract the URL of the current page
        current_url = response.url
        print("Current URL:", current_url)

        # Step 6: Extract the code from the URL
        country_code = current_url.split('-')[1]
        print("Code:", country_code)

        # Step 7: Extract the total number of hotels
        total_hotels_element = response.css('span.biGQs._P.pZUbB.KxBGd span.b')
        number_of_hotels = total_hotels_element.css('::text').get().split()[0].replace(',', '')
        print("The total number of hotels is:", number_of_hotels)

        # Calculate the number of pages
        number_of_hotels = int(number_of_hotels)
        last_page = (number_of_hotels + 30 - 1) // 30
        print("Last page: ", last_page)


