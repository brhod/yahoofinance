########################################################################
########################################################################

#### File which contains the main routine for the program. 
#### See modules for the specific functionality

########################################################################
########################################################################


import sys
import os
import datetime

from yahoofinance_scrapyutils import *


# get date because it is used in naming folders.... just bookkeeping
date = datetime.date.today().strftime("%Y%m%d")
time_of_day = datetime.datetime.now()
current_time = time_of_day.strftime("%H%M")



# main routine
if __name__ == "__main__":
    # get arguments from the command line and then parse them
    argv = sys.argv[1:]
    tickerfile, csvfile, colnamesfile = parse_arguments(argv, date, current_time)
    
    make_template_file(tickerfile, colnamesfile)
    
    if sys.platform[0:3] == 'win':
        os.system("scrapy runspider yahoofinance_scrapyfromtemplate.py -o " + csvfile.replace('/', '\\'))
    else:
        os.system("scrapy runspider yahoofinance_scrapyfromtemplate.py -o " + csvfile)
    
    sys.exit()