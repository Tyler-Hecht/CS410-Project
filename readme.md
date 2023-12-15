# CS 410 Project
Tyler Hecht (thecht2)

## Video link:

[https://youtu.be/hL-R-dziSeU](https://youtu.be/hL-R-dziSeU)

## Project Description

The goal of this project was to create a query system to recommend UIUC CS courses given a query text.

### Data

The data used for this project was scraped from the UIUC course explorer website. The title and course description were scraped for each course, as well as the terms offered. For every term offered (up to a specified limit), the text from that term's page was scraped as well. A certain amount of links were also explored from each term's page, and the text from those pages was scraped as well. There were 161 courses in the dataset.

### Processing

The data was processed by tokenizing, lemmatizing, and removing stop words. Additionally, only valid english words were kept. The data were processed into a dataframe where each row was a course, and the columns were the unique words. The values in the dataframe were the number of times that word appeared in the course description. This format can be easily applied to common text retrieval algorithms.

### Querying

The BM25 algorithm is used to rank the courses based on a query. The query was processed in the same way as the data, and the BM25 algorithm was applied to the query and each course. The top 5 courses are returned as the results. The values of k1 and b were tuned to 1.2 and 0.75 by default, respectively, but can be changed.

## Using the system

### Extension

The querying system was made into a Chrome extension using PyScript. The extension provides a browser-based interface for querying the system. The user can enter a query, and the top 5 courses will be displayed. The link to the course can be copied from the results.

#### Installing the extension

To install the extension, navigate to chrome://extensions in Google Chrome. Enable developer mode, and click "Load unpacked". Select the folder containing the extension files.

#### Using the extension

To use the extension, click on the extension icon in the top right of the browser and click on this extension. You can then use the extension to query the system.

### Command line

The querying system can also be used from the command line. It uses a version of the data that is more accurate since it can use the nltk lemmatizer. You can simply run the file `query.py` to query the system. Run the appropriate command for your operating system:\
`py query.py`\
`python query.py`\
`python3 query.py`

## Documentation

### Scraping

To scrape, the following files can be run in sequence. However, scraping takes a very long time (depending on the limits specified), so the data is already provided in the file `courses_df.pkl`.

#### get_cs_courses.py

This file scrapes the UIUC course explorer website for CS courses. It gets the title, description, and terms offered for each course and saves them to the file `courses_dict.pkl`.

#### crawling.py

This file uses BeautifulSoup to scrape data from each course for many terms. For each term, it explores a certain number of links and scrapes the text from those pages. It saves the data to the file `courses_dict.pkl`.

Scraping all the data would take a long time, so limits can be specified:
- `MAX_TERMS` is the maximum number of terms to scrape for each course
- `MAX_LINKS` is the maximum number of links to explore for each term
- `TIMEOUT` is the timeout for each page request

#### counter.py

This file creates the dataframe with counts for each word in each course. It uses the file `courses_dict.pkl` to get the data. It saves the dataframe to the file `courses_df.pkl`.

Configuration options:
- `MAX_TOKENIZER_LEN` is the maximum length of the data to tokenize for each course
- `MAX_WORDS` is the maximum number of words to keep for each course
- `TITLE_WEIGHT` is the weight to give to the title of the course when counting words
- `DESCRIPTION_WEIGHT` is the weight to give to the description of the course when counting words

### Querying

#### query.py

This file provides functions to query the system. It uses the file `courses_df.pkl` to get the data.

The function `BM25` implements the BM25 algorithm. It takes in a query and returns a list of the top 5 courses that match the query. On the first two parameters are required.\
Parameters:
- `term`: The word (term)
- `course` The course (document)
- `k1`: The k1 parameter for BM25
- `b`: The b parameter for BM25

Returns:
- The BM25 score for the term and course

The function `query` takes in a query and prints the top 5 courses that match the query. Only the first parameter is required.\
Parameters:
- `query_text`: The query text
- `excluded_courses`: A list of courses to exclude from the results
- `k1`: The k1 parameter for BM25
- `b`: The b parameter for BM25
- `data`: The dataframe containing the data
- `tokenize`: The tokenization function
- `lemmatize`: The lemmatization function
