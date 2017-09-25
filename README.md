# Movie Hype
==============================

## Summary
A exploratory data analysis project that seeks to answer the question: "Which movies are overrated/underrated and why?"

## Objectives
- Clean and transform the movie data
- Scrape and clean the movie feedback data
- Add the movie and movie feedback data to SQL (for practice)
- Perform EDA on the data in SQL in python
- Develop a visual report using Tableau

## Setup
- Python v3.5
- Jupyter v4.2

## Cleaning/Transforming/Storing Process
For the imdb data, I changed the movie titles to have only alpha-numeric characters, all lower-cased and roman numerals were changed to arabic numerals. This was to ensure consistency and maximal overlap between movie titles, which is the join key, between the two datasets. I also ensured that no duplicates (same movie title) were copied into one of the datasets. The resulting changes are written to a new csv file.

For the scraped data from MovieInsider.com, I also converted the movie titles to lowercase, alpha-numeric characters. I also removed non-ascii characters which seemed to have made it through the scraping process. I scraped the "will see" and "won't see" metric for every movie on the website and converted them into an "interest ratio" - a ratio of will see vs. won't see. The scraped data is transferred to a csv file.

The two csv files are then stored in dataframes where they were merged, combining the movie data with the initial interest associated with those movies.

## Insights

## Conclusion

## Further Work

## Resources
