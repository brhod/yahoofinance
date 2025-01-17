# file which contains the spider used by scrapy for the information extraction

import scrapy
import itertools
from yahoofinance_scrapyutils import *


# get the company and column information
COMPANY_NAMES = get_companies("./company-names/sample_symbols.txt")
COLUMN_NAMES = get_column_names("./column-names/default_column_names_no_units.txt")


# set the urls to be scraped
URLS = ('https://ca.finance.yahoo.com/quote/' + ticker + '/key-statistics?p=' + ticker for ticker in COMPANY_NAMES)


# define a spider class to be used to scrape information
class YahooFinanceSpider(scrapy.Spider):
    name = "yahoo-finance"
    start_urls = URLS
    
    def parse(self, response):
        company_name = response.url.split('=')[1]                                     # gets company name from url
        company_column = zip(['Company'], [company_name])                             # just here to be able to make generator
        column_names = (cn.get() for cn in response.xpath('//tr/td[1]/span/text()'))  # get column names from response
        information = (info.get() for info in response.xpath('//tr/td[2]//text()'))   # get data from response
        data = zip(column_names, information)                                         # combine column names and data
        converted_data = (convert_data(dt) for dt in data)                            # convert units to numbers
        labeled_data = company_column                                                 # initialize final generator with company column
        for cdt in converted_data:                                                    # build final generator... see note below
            labeled_data = itertools.chain(labeled_data, cdt)
        filtered_data = (ldt for ldt in labeled_data if ldt[0] in COLUMN_NAMES)       # get only the columns you want
        
        yield dict(filtered_data)
        

"""
i am not sure if i should make such extensive use of generators, but since we don't want to do anything with this 
information other than copy it to a file, i think it makes some sense. however, to get the speed improvements 
from using a generator, it makes the code a little convoluted because of how i create the table to be exported to 
a csv file. 

background on table construction:
for a column name like `Shares short (Nov. 30, 2020)' with data `2.00', i actually split this up into
two data points. the first is one with column name `Shares short' and data `2.00'; the other is with column name
`Date: Shares short' and data `Nov. 30, 2020'. i hope this makes sense and makes for easier integration of data
in the future, as these particular column names are dynamic, meaning they will change in a month or so. basically,
i formatted it in a way such that i split the column name which changes over time to two column names which don't 
change over time, and i made the changing part of the old column name to be the data part of the new column name.

how this affects code:
this table construction, unfortunately, makes the code using generators a bit trickier... and a bit inelegant, but
perhaps it is faster. i have to basically zip everything in the convert_data function, and then i have a generator
of zips which have to be chained to become a single generator so it can be outputted correctly to csv. i have to 
zip things because the convert_data function returns a single tuple in the cases which don't have a column name
which is dynamic, but it returns *two* tuples in the case where the column name is dynamic (as explained above).
zipping things basically abstracts away the difference by making them both of the zipped type. then we can link
them using itertools.
"""