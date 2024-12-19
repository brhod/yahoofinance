# yahoofinance
This is just a basic web scraper to get information from the statistics page of Yahoo Finance. It is not perfect in a lot of ways, but it should suffice for now! If you want to see what information it scrapes, just look here at the Tesla [one](https://ca.finance.yahoo.com/quote/TSLA/key-statistics?p=TSLA). This program just grabs the data and then ouputs it into a `.csv` file. I leave it to the user to load this `.csv` file into whatever program they want to do further filtering. 

## Dependencies
This scraper makes extensive use of the Scrapy library (which is really awesome, so thanks!). Other packages are pretty standard I think. Anyways, here is the list.
* scrapy
* os
* sys
* getopt
* datetime
* itertools

If you don't have any of these files, you can use `pip install` on the command line or use whatever equivalent there is to this in your virtual environment.

## A little note on each file or directory

### Python files

* `yahoofinance_main.py`: File with the main routine. You can run this from the command line, as you will see below.

* `yahoofinance_scrapy.py`: File used if you want to directly tweak the code. Again, more on this below.

* `yahoofinance_scrapyutils.py`: File containing helper functions used in `yahoofinance_main.py` and `yahoofinance_scrapy.py`

* `yahoofinance_scrapyfromtemplate.py`: File which is exactly the same as `yahoofinance_scrapy.py`, except possibly for the global variables defined in these files. This file is created when you use the command line functionality in `yahoofinance_main.py`.

### Other files and directories

* `column-names`: Folder which contains `.txt` files with the names of the columns to be scraped. The set of column names is slightly different than what you will see on Yahoo Finance because when scraping, it was much more convenient to remove information like (ttm = trailing twelve months), and it was necessary to modify and create new columns in cases where the column name is dynamic (meaning it can change on future scrape... this is because it had a date in the column name). See documentation at the bottom of `yahoofinance_scrapy.py` for more details. The file `subset_column_names.txt` is just a subset of the columns used for exposition, and also for reference, but not for use, is the file `default_column_names.txt`, which shows information like ttm and the units for all the data.

* `company-names`: Folder containing the list of all tickers for the NYSE (`all_symbols.txt`... I believe I got this from Kaggle), a subset of them (`sample_symbols.txt`) for exposition purposes and the list of all S&P500 companies (`sp500.txt`), which was scraped from Wikipedia.

* `scraped-data`: Folder which contains the scraped data, if you use the command line functionality.

* `column_names_background_info.txt`: This file is really the reference for how to interpret the data. There is a lot of information, such as frequency of measurements and units, that was much more convenient not to include (or necessary to remove) when scraping. This file helps you keep track of all that information that was not included. This file really helps give meaning to the numbers; the scraper just gets the numbers. This file is important for reference when doing anything analytical with the scraped data.

* `yahoofinance_template.txt`: This `.txt` file is used in `yahoofinance_main.py` to create the `.py` file `yahoofinance_scrapyfromtemplate.py` which is actually used by the Scrapy library. See below for a brief explanation. Not important, but maybe you are curious.


## Tutorial

Okay, there are basically two ways to use this program: (i) using `yahoofinance_main.py`; and (ii) not using `yahoofinance_main.py` and tweaking the global variables in the `yahoofinance_scrapy.py` file yourself. I recommend the first one, although it is not really elegant how it works .. o.O.

### Way 1 (recommend): using `yahoofinance_main.py`

This function takes three arguments: `-i` an input file with the names of the companies to get data on; (optional) `-o` an output file to write the data to, which must be `.csv`; and (optional) `-c` a file containing the column names that you want to scrape, in the event you don't want all the information. The `-o` and `-c` are optional because they have the reasonable defaults: `-o` defaults to an output file named `./yahooscrape-on-<the day's date>/yahooscrape_at_<the time of scrape>_data.csv` in the `scraped-data` folder; `-c` defaults to `./column-names/default_column_names_no_units.txt` which is just a file containing all the file names found on the Yahoo Finance statistics page.

The basic command line syntax is this:
```
python yahoofinance_main.py -i <inputfile> -o <optional: name of file you want output to go, must be .csv> -c <optional: name of file with column names>
```

You can use the flag `-h` to retrieve this information as well.

#### Example: Getting data on a subset of the companies and a subset of the column names

In this case, the path to the data will be `./scraped-data/yahooscrape-on-20201220/yahooscrape_at_1642_data.csv`. I did this scrape on Dec. 20, 2020 at 4.42p. Here is the command used.

```
python yahoofinance_main.py -i ./company-names/sample_symbols.txt -c ./column-names/subset_column_names.txt
```

#### Example: Getting the data on a subset of the companies, specifying the output file and using default column names

In this case, the path to the data is specified by the user, and it is just `./yahoo.csv`, so it is in the current directory. The column names default to the ones in `./column-names/default_column_names_no_units.txt`. The companies to be scraped come from `./company-names/sample_symbols.txt`. Here is the command used.

```
python yahoofinance_main.py -i ./company-names/sample_symbols.txt -o yahoo.csv
```

### Way (not recommended) 2: using `yahoofinance_scrapy.py` directly with `scrapy runspider`

There are two ways of scraping the data because of how I am working with the Scrapy library. I won't go into much detail, but the problem is that I need to instantiate the global variables `COMPANY_NAMES` and `COLUMN_NAMES` in `yahoofinance_scrapy.py` for the spider in that file to work as desired, and it is that file which the Scrapy library searches to do the scrape. Unfortunately, there is no way to cleanly do instantiate these variables using the `yahoofinance_main.py` main routine. So, what I did in the code for the `yahoofinance_main.py` is the following, which is the 'inelegant' thing I alluded to above: first, I created the `.txt` file `yahoofinance_template.txt` to serve as the file which I will basically copy; then, I created the function `make_template_file` to create a `.py` file `yahoofinance_scrapyfromtemplate.py` which has the correct contents to instantiate the desired global variables when the Scrapy library calls on this file to run the spider. I basically just copy the contents from `yahoofinance_template.txt` to a file `yahoofinance_scrapyfromtemplate.py` with two new lines defining the appropriate `COMPANY_NAMES` and `COLUMN_NAMES` global variables. Inelegant, but it works...

Okay, so, now maybe it is clear that to run the spider with different settings, you have to edit the global variables in the file which contains the spider. You can do this directly if you want. Just go into the `yahoofinance_scrapy.py` file and change the directories for you want the corresponding functions to search when defining `COMPANY_NAMES` and `COLUMN_NAMES`. The defaults are in there right now, but you can change them to whatever you want. Suppose you want to look at a file called `my_companies.txt` in the current directory for your companies and a file `my_columns.txt` in the current directory for your columns. Then, you do the following in `yahoofinance_scrapy.py`.

```
COMPANY_NAMES = get_companies("my_companies.txt")
COLUMN_NAMES = get_column_names("my_columns.txt")
```

After saving those changes, you use the following syntax on the command line:

```
scrapy runspider yahoofinance_scrapy.py -o <output file name>
```

In the case that you want to name the output file `my_data.csv`, you would do

```
scrapy runspider yahoofinance_scrapy.py -o my_data.csv
```

I didn't run this example, so there is no example data in the repository at the moment.


## Notes on custom usage

* When you create your own company and/or column files to determine who and what to scrape, just make a `.txt` file with the list of the of company tickers/symbols as they appear on stock exchanges and/or the list of columns that you want to scrape. For the column file, the caveat is that you have to match ***exactly*** the name as they appear in the `./column-names/default_column_names_no_units.txt` file. Maybe I can build in some functionality to catch exceptions when that happens, but as of right now if the column name you specify is not found, the scraper will just skip over that information (as that exception is actually caught by the Scrapy library, so writing in that functionality would mean I have to peer deeper into that library). Also, this fact isn't too terrible; it helps facilitate consistency across scrapes, so if you do want to compare scraped information on different days, it is easier.


## Miscellaneous notes

* For large numbers like millions, billions and trillions, I represented these numbers with scientific notation in the csv file. Python and R should not have a problem recognizing this and reading these as numbers and not strings.

* There is a difference between a company which has a/some 'N/A' in the Yahoo Finance table and a company who doesn't have a statistics page. In the first case, 'N/A' is recorded as `nan`, and companies for which the information you want to scrape doesn't apply just record ' ' for each of the column values. Just look out for this when you scrape. If you see a company with a lot of ' ' values in the csv file where the data goes, it means that the Yahoo Finance statistics page doesn't exist. Again, because so much of the scraping work is done with the Scrapy library, customizing behavior of the scraper in these cases is a bit more involved because it requires me to go into the library code, so that's why I am just putting a little note here.

* Some companies previously had Yahoo Finance statistics pages, but it seems that they no longer have a page. Maybe that is because of bankruptcy or something, but whatever the case may be sometimes information is ***still*** scraped for them because that webpage still exists in some form the Scrapy library can find it! So, if you get surprising results for a company, really use caution to further investigate. I don't think this situation is that common, but it definitely has come up in the examples. The company BGG is an example of this. I think they recently went bankrupt, but information can still be scraped from https://ca.finance.yahoo.com/quote/BGFV/key-statistics?p=BGFV using the Scrapy library, but if I try to navigate here in my browser, I will be redirected to another page.
