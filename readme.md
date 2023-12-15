# CS 410 Project
Tyler Hecht

## Video link:

[http://www.youtube.com/watch?v=](http://www.youtube.com/watch?v=)

## Project Description

The goal of this project was to create a query system to recommend UIUC CS courses given a query text.

### Data

The data used for this project was scraped from the UIUC course explorer website. The title and course description were scraped for each course, as well as the terms offered. For every term offered (up to a specified limit), the text from that term's page was scraped as well. A certain amount of links were also explored from each term's page, and the text from those pages was scraped as well. There were 161 courses in the dataset.

### Processing

The data was processed by tokenizing, lemmatizing, and removing stop words. Additionally, only valid english words were kept. The data were processed into a dataframe where each row was a course, and the columns were the unique words. The values in the dataframe were the number of times that word appeared in the course description. This format can be easily applied to common text retrieval algorithms.

### Querying

The BM25 algorithm is used to rank the courses based on a query. The query was processed in the same way as the data, and the BM25 algorithm was applied to the query and each course. The top 5 courses are returned as the results. The values of k1 and b were tuned to 1.2 and 0.75 by default, respectively, but can be changed.

### Extension

The querying system was made into a Chrome extension using PyScript. The extension provides a browser-based interface for querying the system. The user can enter a query, and the top 5 courses will be displayed. The link to the course can be copied from the results.

#### Installing the extension

To install the extension, navigate to chrome://extensions in Google Chrome. Enable developer mode, and click "Load unpacked". Select the folder containing the extension files.

#### Using the extension

To use the extension, click on the extension icon in the top right of the browser and click on this extension. You can then use the extension to query the system.


