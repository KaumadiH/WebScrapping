## Overview

This script processes a list of URLs to extract and analyze content from web pages. It reads URLs from a text file, scrapes specific HTML elements (titles, headers, and paragraphs), cleans the data by removing stop words, performs stemming, and finally calculates a weighted score for each URL's content. The results are saved to CSV files and written to a text file.

## Requirements

*   Python 3.x
*   Libraries: pandas, bs4 (BeautifulSoup), nltk (Natural Language Toolkit)

## Setup

1.   Install the required Python libraries:
          pip install pandas bs4 nltk
2.   Prepare the following files:

*   URLList.txt: A text file containing URLs (one per line) to be processed.
*   commonwords.txt: A text file containing stopwords (one per line) to be removed from the content.

## Usage

1.   Run the script:
          python script_name.py
2.   Replace script_name.py with the name of your Python script file.

## Script Workflow

1. Read URLs:
*   Reads URLs from URLList.txt.
*   Strips leading and trailing whitespace from each URL.

2.   Scrape Web Page Content:
*   For each URL (up to 10 URLs):
 Use get_soup(strippedUrl) to parse the web page.
Extract titles and headers (h1 to h6) using get_title(soup) and get_header(soup, level).
Extract paragraphs using get_paragraphs(soup).

3.	Create DataFrame:
*   Store the extracted content in a DataFrame with columns for Title, headers (h1 to h6), and paragraphs.
*  Save the raw data to raw_data.csv. 

4.	Concatenate Content:

*   Concatenate the extracted content into a single string for each URL.
*   Store this in a new DataFrame column concatenated.
5.	Remove Stopwords:

*   Read stopwords from commonwords.txt.
*   Remove stopwords from the concatenated content and store the cleaned text in concatenated_clean.
6.	Perform Stemming:
*  Use SnowballStemmer from the nltk library to stem the words in the cleaned text.
*  Store the stemmed text in a new DataFrame column stemmed.
*  Save the stemmed data to stemmed.csv.
7.	Calculate Weights:
*   Apply a weighting function weight to the content (titles, headers, paragraphs, and stemmed text) to generate a weighted score.
*   Store the weighted scores in a new DataFrame column weighted.
8.	Sort and Save Results:
*   Sort the URLs based on their weighted scores in descending order.
*   Write the sorted results to a text file using writeToTextFile(result).

## Functions Used
*   get_soup(url): Parses a URL and returns the BeautifulSoup object.
*   get_title(soup): Extracts the title from the BeautifulSoup object.
*   get_header(soup, level): Extracts headers of the specified level from the BeautifulSoup object.
*   get_paragraphs(soup): Extracts paragraphs from the BeautifulSoup object.
*   weights(title, h1, h2, h3, h4, h5, h6, paragraph, stemmed): Calculates a weighted score based on the extracted content.
*   sortKeysInDescendingOrder(weighted_scores, urls): Sorts URLs based on their weighted scores.
*   writeToTextFile(result): Writes the sorted results to a text file.

## Output Files

*   raw_data.csv: Contains the raw extracted content (titles, headers, and paragraphs).
*   stemmed.csv: Contains the stemmed content after stopword removal.
*   result.txt: Contains the URLs sorted by their weighted scores.

## Notes

*   Ensure the helper functions (get_soup, get_title, get_header, get_paragraphs, weights, sortKeysInDescendingOrder, and writeToTextFile) are correctly defined and implemented in the script.
*   Adjust the script as necessary to fit the structure and format of your specific web scraping requirements.
