This tool implements Scrapy framework to scrape (extract) data from a
dummy site ”https://books.toscrape.com”. This website build for a purpose of
practicing scraping by beginners in web scraping. The given program extracts
around 1000 books from a total of 50 pages. The parameters it scrapes is tag,
title, price, rating, image URL, product description and the image itself and
stores them locally in files system (/FILES/tag/title) where images are stored
in .JPEG format and the rest of the parameters is stored in .JSON format.
The create.py script purpose is to create a single database.json file from all
distributed .JSON files in the folder FILES.
The parse.py script purpose is to create a ”query result.json” file in which it
contains data points from database.json filtered out by user-based conditions
and projects user-based attributes only.
