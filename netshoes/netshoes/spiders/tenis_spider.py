import scrapy
from scrapy.spiders import Spider,CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import ShoesItem
from os import path
# scrapy crawl netshoes -t csv -o -> netshoes.csv
class TenisSpider(Spider):
    name = "netshoes"
    page_num = 1
    start_urls = ["https://www.netshoes.com.br/busca/tenis?page=1"]

    index_file = "./page_index.txt"

    def parse(self,response):

        if(path.exists(self.index_file)):
            index = open(self.index_file,"r")
            self.page_num = int(index.readline())
            index.close()

        products = response.css('.item-card')        
        for product in products:
            url = product.css('.item-card__description__product-name::attr(href)').extract_first()
            url = response.urljoin(url)
            yield scrapy.Request(url=url,callback=self.parse_shoe_types)

        next_page = response.css('.next::attr(href)').get()
        if(next_page):
            self.page_num += 1
            index = open(self.index_file,"w")
            index.write(f"{self.page_num}")
            index.close()

            yield response.follow(next_page, callback=self.parse)

    def parse_shoe_types(self,response):
        colors = response.css('.color li a')
        for color in colors:
            url = color.css('a::attr(href)').extract_first()
            url = response.urljoin(url)        
            yield scrapy.Request(url=url,callback=self.parse_shoe,meta={"url" : url},dont_filter=True)

    def parse_shoe(self,response):
        shoe = ShoesItem()
        tags = []

        shoe['url'] = response.meta.get('url')

        shoe['price'] = response.css('#buy-box strong::attr(content)').extract_first()

        colors = response.css('.sku-select-title::text').extract_first()
        colors = [color.lower() for color in colors.split(' ') if len(color)> 2]
        shoe['colors'] = colors
        tags.extend(colors)

        attributes = response.css('.attributes li')
        attributes_dict = {}
        for attribute in attributes:
            attr_name, attr_value = attribute.css('::text').extract()[0].lower()[:-1], attribute.css('::text').extract()[1].lower()
            attributes_dict[attr_name] = attr_value

        gender = attributes_dict['gênero'][1:]
        shoe['gender'] = gender
        tags.append(gender)

        category = attributes_dict.get('categoria') if attributes_dict.get('categoria') else attributes_dict.get('linha')
        if(category):
            category = category[1:]
            tags.append(category)
        shoe['category'] = category
        
        usage_type = attributes_dict['indicado para'][1:]
        shoe['usage_type'] = usage_type
        tags.append(usage_type)

        material = attributes_dict['material'][1:]
        shoe['material'] = material
        tags.append(material)

        nationality = attributes_dict['origem'][1:]
        shoe['nationality'] = nationality
        tags.append(nationality)

        full_name = attributes_dict['nome'][1:]
        if(('tênis' not in full_name) or ('sapatênis' in full_name) or ("kit" in full_name) or ("infantil" in full_name)):
            return ShoesItem()
        shoe['raw_name'] = full_name

        full_name_split = full_name.split(' ')
        shoe_index = full_name_split.index('tênis')
        brand = full_name_split[shoe_index+1] if (full_name_split[shoe_index+1].lower() != 'couro') else  full_name_split[shoe_index+2]
        brand = self.get_known_brand_name(brand) if(not self.get_known_brand_name(brand)) else brand
        shoe['brand'] = brand
        tags.append(brand)

        full_name = full_name.replace(f' {gender}','').replace(f'{gender} ','')
        full_name = full_name.replace(' tênis','').replace('tênis ','')
        full_name = full_name.replace(' couro','').replace('couro ','')
        shoe['name'] = full_name

        description = response.css('#features p::text').extract_first()
        shoe['description'] = description

        customer_recommendation_rate = response.css('.reviews__productAvaliation-average-line-number::text').extract_first()
        shoe['customer_recommendation_rate'] = customer_recommendation_rate

        customer_score = response.css('.reviews__customerFeedback-rating-line-number::text').extract_first()
        shoe['customer_score'] = customer_score

        customer_reviews_number = response.css('.reviews__customerFeedback h3::text').extract_first()
        number_start = customer_reviews_number.index('(') + 1
        number_end = customer_reviews_number.index(')')
        customer_reviews_number = customer_reviews_number[number_start:number_end]
        shoe['customer_reviews_number'] = customer_reviews_number

        images_url = response.css('.swiper-wrapper li img::attr(data-src)').extract()
        shoe['image_urls'] = [response.urljoin(url) for url in images_url]

        shoe['tags'] = tags
        
        return shoe

    def get_known_brand_name(self,full_name):
        known_brands = ['olympkus', 'under_armour', 'nike', 'adidas', 'mizuno','asics','mormaii','puma',
        'oakley','fila','kappa', 'all star','gonew','new balance']

        for brand in known_brands:
            if(brand in full_name.lower()):
                return brand

        return None
