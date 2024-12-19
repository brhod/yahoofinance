import os
import getopt
import sys
import itertools
import datetime

# gets list of tickers that you want to scrape from a file you specify
def get_companies(filename):
    with open(filename, encoding = 'utf-8') as file:
        company_names = [line.strip('\n') for line in file]
    return company_names



# gets column names that you want to scrape from a file you specify
def get_column_names(filename):
    column_names = set()
    with open(filename, encoding = 'utf-8') as file:
        for line in file:
            column = line.strip('\n')
            column_names.add(column)

    return column_names



# function which converts and formats data to be written to csv file appropriately
def convert_data(column):
    column_name = column[0]
    data_string = column[1]
    data_string = data_string.replace(',', '')              # remove comma so that string numbers can be converted to actual numbers
    
    
    
    # clean data
    if '∞' in data_string:
        data = "nan"
    elif data_string[-1] == '%':
        data = data_string[:-1]
    elif data_string[-1] == 'k':
        data = data_string[:-1] + "e+3"
    elif data_string[-1] == 'M':
        data = data_string[:-1] + "e+6"
    elif data_string[-1] == 'B':
        data = data_string[:-1] + "e+9"
    elif data_string[-1] == 'T':
        data = data_string[:-1] + "e+12"
    elif data_string == 'N/A' or data_string == '':
        data = "nan"
    elif ':' in data_string:                                # this one is for ratios
        data = data_string
    else:
        data = data_string
    
    
    # this bit sets up the next chunk which processes the weird columns with the 
    # date included in the name... annoying on yahoo
    if ',' in column_name:
        column_name = column_name.replace(',', '')          # remove comma so that it doesn't interfere with csv formant in printing
        new_column_name, date = column_name.split('(')
        new_column_name = new_column_name[:-1]              # removes space that preceded the date we just split off
        date = date[:-1]                                    # removes the parenthesis ')' at the end
        column_name = new_column_name
        
        # now to make the new column
        date_column_name = "Date: " + column_name          
        if date[0:5] == "prior":
            date = date[12:]
            column_name = column_name + " prior month"
            date_column_name = date_column_name + " prior month"
        
        # convert date into a different string format
        datetime_obj = datetime.datetime.strptime(date, "%b. %d %Y")
        new_date = datetime_obj.strftime("%Y-%m-%d")
        
        converted_data = zip([column_name, date_column_name], [data, new_date])
    else:
        converted_data = zip([column_name], [data])
    
    
    return converted_data





# function which parses arguments obtained from the command line
def parse_arguments(argv, date, time):
    """
    VARIABLES
    argv: list of str, contains arguments from command line
    date: str, this is the day's date... used for naming
    time: str, this is the day's time... used for naming
    """
    
    # get the arguments and options
    try:
        opts, args = getopt.getopt(argv,"hi:o:c:",["tickerfile=","csvfile=","columnnames="])
    except getopt.GetoptError:
        print("yahoofinance_main.py -i <file with tickers> -o <csv file you want to the data to go; if not provided, a file will be created in folder named data>")
        sys.exit(2)
     
    # initialize the relevant variables
    tickerfile = None
    csvfile = None
    colnamesfile = None
    
    # set the variables from the arguments and options obtained
    for opt, arg in opts:
        if opt == "-h":
            print("\nyahoofinance_main.py\n\t -i <file with tickers>\n\t -o <csv file you want to the data to go (must be csv)\n\t -c <file with column names>")
            sys.exit()
        elif opt in ("-i", "--tickerfile"):
            tickerfile = arg
        elif opt in ("-o", "--csvfile"):
            csvfile = arg
        elif opt in ("-c", "--columnnames"):
            colnamesfile = arg
            
            
    # exit the program if no companies were given to scrape
    if not tickerfile:
        print("Please provide a file with the ticker labels for which you want data.")
        sys.exit()         
    print("Ticker file used is " + tickerfile)
    
    
    # if no output csv file is given, let user know where the file will be created
    if csvfile:
        try:
            csvfile.split('.csv')
            print("Output csv file used is " + csvfile)
        except:
            print("Please provide a filename with an extension that is csv (comma separated value)")
            sys.exit()
    else:
        print("Output csv file will be ./scraped-data/yahooscrape-on-" + date + "/yahooscrape_at_" + time + "_data.csv")
        csvfile = "./scraped-data/yahooscrape-on-" + date + "/yahooscrape_at_" + time + "_data.csv"
    
     
    # inform the user on the column names used
    try:
        print("Column names to be scraped are from file " + colnamesfile)
    except:
        print("Column names to be scraped are the default from ./column-names/default_column_names.txt")
        colnamesfile = "./column-names/default_column_names_no_units.txt"
    
    
    # return the set of relevant variables for program
              
    return tickerfile, csvfile, colnamesfile




# function to create a new .py file with the correct global vars to run spider. only use this function
# if you don't feel like changing the yahoofinancescrapy.py file yourself
def make_template_file(textfile, colnamesfile):
    try:
        with open("yahoofinance_template.txt", 'r', encoding = 'utf-8') as template:
            lines = [line for line in template]
            anchor = "# get the company and column information\n"            # find point in template to insert global var code
            point_of_insertion = lines.index(anchor)
            
            company_name_global_var = "COMPANY_NAMES = get_companies(\"" + textfile + "\")\n"
            column_name_global_var = "COLUMN_NAMES = get_column_names(\"" + colnamesfile + "\")\n"
            
            lines[point_of_insertion+1] = company_name_global_var            # insert global var codes
            lines[point_of_insertion+2] = column_name_global_var
            
            
            # make a python file to be read after making relevant insertions into the template file
            with open("yahoofinance_scrapyfromtemplate.py", 'w+', encoding = 'utf-8') as py_template:
                for line in lines:
                    py_template.write(line)
    except:
        print("Please check to see if the template file yahoofinance_template.txt exists. It should be there and should resemble exactly the file yahoofinance_scrapy.py except that the global variables COMPANY_NAMES and COLUMN_NAMES are omitted.")