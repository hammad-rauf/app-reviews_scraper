from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ..items import AppreviewItem

from datetime import date


class AppReviewSpider(CrawlSpider):

    name = "appreview"

    start_urls = [
                "https://apps.shopify.com/browse/all?app_integration_kit=off&app_integration_pos=off&pricing=all&requirements=off&sort_by=installed"

    ]

    date = date.today()


    rules = (
        Rule(LinkExtractor(restrict_css=(["#CategoriesFilter .search-filter--is-selected .marketing-radio-label",".search-pagination.display--mobile.text-center .search-pagination__next-page-text"]))),
        Rule(LinkExtractor(restrict_css=(".grid.grid--bleed.grid--equal-height.search-results__grid")),callback="product"),  
    )
    
    month_lst = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December'
    ]

    today_date = date.today()

    def product(self, response):

        review_page = response.css(".app-listing-reviews__footer a::attr(href)").extract_first()

        url = f"https://apps.shopify.com{review_page}"

        product = AppreviewItem()

        product["app_link"] = response.url
        product["app_link"] = product["app_link"].split("?")[0]        

        request = Request(url =url, callback =self.review)

        request.meta["product"] = product

        yield request


    def review(self,response):

        product = response.meta["product"]

        flag = True

        reviews = response.css(".review-listing")

        for data in reviews:
            product["date"] = data.css(".review-metadata__item+ .review-metadata__item .review-metadata__item-value::text").extract_first().strip()
            product["store"] = data.css(".review-listing-header__text::text").extract_first().strip()
            product["store"] = product["store"].replace("'","")

            product["rating"] = data.css(".ui-star-rating::attr(data-rating)").extract_first()
            product["review"] = data.css(".truncate-content-copy p::text").extract_first()

            product["review"] = product["review"]

            if product["review"] != None:
                product["review"] = product["review"].replace("'","")
            
            store = product["date"].replace(",","")
            store = store.split(" ")            

            temp = self.today_date
            temp = str(temp)
            temp = temp.split('-')
            strr = f"{store[2]}-"            
            for index,mon in enumerate(self.month_lst):
                index +=1
                
                if mon in product["date"]:
                    strr += F"{index}-"

            if int(store[1]) < 10:
                strr += F"0{store[1]}"
            else:
                strr += F"{store[1]}"


            if str(strr) == str(self.today_date):
                yield product
                flag = True
            else:
                flag = False


        if flag:            
            next_page = response.css(".search-pagination.hide--mobile.text-center .search-pagination__next-page-text::attr(href)").extract_first()

            if next_page != None:
                yield response.follow(url =next_page,callback= self.review,meta={"product":product})

        