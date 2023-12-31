# EngetoProject3_Election_scraper

## About
Election scraper is designed to scrape election data from a web [Volby.cz](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ). Scraper is designed to scrape data from the year 2017. Scraped data are stored as csv file and can be used for further data analysis. Application uses 3rd party libraries, and all packages are stored in a configuration file requirements.txt.

## Installation

Download files main.py and requirements.txt. Open a tool supporting to run .py files. Install configuration file "requirements.txt" using command pip install -r requirements.txt.  

## Data scraping
File "main.py" can be triggered from command line using 2 arguments. Once the command line is opened write "python", name of a file "main.py" and write two arguments. First argument is URL of a chosen district [here](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ)(e.g. Brno-venkov, Trebic). The second argument is the name of csv file where data will be stored. Order of arguments must be kept. Once the scraping is completed the program is closed.

__Voting results for district Brno-venkov:__
 
1. argument = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6203"
1. argument = result_brno_venkov.csv

__Starting the program:__  
python main.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6203" result_brno_venkov.csv

__Scraping progress example:__  

![Scraping progress example](https://github.com/SilviePelanova/EngetoProject3_Election_scraper/blob/main/Scraping%20result%20example.png)

__Scraping result example:__

![Sraping result example](https://github.com/SilviePelanova/EngetoProject3_Election_scraper/blob/main/Scraping%20progress%20example.png)
