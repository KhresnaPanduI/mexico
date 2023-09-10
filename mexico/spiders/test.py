import scrapy

class MexicoSpider(scrapy.Spider):
    name = 'mexico_spider'
    start_url = 'https://www.tripadvisor.com/'
    country = 'Mexico'  # You can change this to any country

    # Dictionary mapping categories to their respective codes
    category_dict = {
        'Tours': 'c42',
        'Daily trips': 'c63',
        'Outdoor activities': 'c61',
        'Concert and shows': 'c58',
        'Food and drink': 'c36',
        'Class and workshop': 'c41'
    }

    def start_requests(self):
        # Step 3: Open https://www.tripadvisor.com/
        yield scrapy.Request(url=self.start_url, callback=self.search_activities)

    def search_activities(self, response):
        # Step 4: Input the text value of the search bar
        search_url = f"https://www.tripadvisor.com/Search?q={self.country}%20Things%20to%20Do"
        yield scrapy.Request(url=search_url, callback=self.extract_country_code)

    def extract_country_code(self, response):
        # Step 5: Extract the URL of the current page
        current_url = response.url
        print("Current URL:", current_url)

        # Step 6: Extract the code from the URL
        country_code = current_url.split('-')[1]
        print("Code:", country_code)

        # Iterate through all categories
        for category, cat_code in self.category_dict.items():
            category_url = f"https://www.tripadvisor.com/Attractions-{country_code}-Activities-{cat_code}-{self.country}.html"
            print("Current url: ", category_url)
            yield scrapy.Request(url=category_url, callback=self.parse_category)

    def parse_category(self, response):
        # Extract the text from all elements with the class "nBrpc"
        total_properties_elements = response.css('.uYzlj.c')
        total_properties = int(total_properties_elements.css('::text').getall()[-1].replace(',', ''))
        print("Total properties: ", total_properties)

        # Calculate the number of pages
        last_page = (int(total_properties) + 30 - 1) // 30
        print("Last page: ", last_page)

        for page_number in range(1, 3): # in production, should be until last page+1
            page_url = f"https://www.tripadvisor.com/Attractions-{country_code}-oa{(page_number - 1) * 30}-{cat_code}-{self.country}.html"
            print("Crawling start for page: ", page_url)
            yield scrapy.Request(url=page_url, callback=self.parse_page)

    def parse_page(self, response):
        # Extract and process data from the page with activity listings
        activity_elements = response.css('.OlPMM.z.o')

        for activity_element in activity_elements:
            # Extract activity link
            activity_link = activity_element.css('.BUupS._R.w._Z.y.M0.B0.Gm.wSSLS::attr(href)').get()
            print("Activity link: ", activity_link)

            yield scrapy.Request(url=activity_link, callback=self.parse_activity())

    def parse_activity(self, response):
        #extracting business links
        business_link = response.css('.UikNM._G.B-._S._T.c.G_.y.wSSLS.wnNQG.raEkE::attr(href)').get()
        activity_name = response.css('.biGQs._P.fiohW.ncFvv.EVnyE::text').get()

        yield scrapy.Request(url=business_link, callback=self.parse_business())

    def parse_business(self, response):
        # Scrapy code for extracting location, phone number, email, and website
        try:
            # Extract location
            location_element = response.css('.biGQs._P.fiohW.fOtGX::text').get()
            if location_element:
                location = location_element.strip()
                city = location.split(', ')[0]
                print('City:', city)
            else:
                city = ''
                print('City not found on this page.')

            # Extract phone number
            phone_number_element = response.css('a[href^="tel:"]::attr(href)').get()
            if phone_number_element:
                phone_number = phone_number_element[4:].replace("%", " ")
                print('Phone number:', phone_number)
            else:
                phone_number = ''
                print('Phone number not found on this page.')

            # Extract email
            email_element = response.css('a[href^="mailto:"]::attr(href)').get()
            if email_element:
                email = email_element[7:]
                print('Email:', email)
            else:
                email = ''
                print('Email not found on this page.')

            # Extract website
            website_element = response.xpath('//a[@target="_blank"]/@href').get()
            if website_element:
                website = website_element
                print('Website:', website)
            else:
                website = ''
                print('Website not found on this page.')

        except Exception as e:
            print('An error occurred:', str(e))




