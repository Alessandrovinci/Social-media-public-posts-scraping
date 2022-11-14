# Social-media-public-posts-scraping

This project is about scraping public posts from Facebook's search bar based on an input query defined by the user.

The user needs to insert an input which corresponds to the query he would look for in the social's search bar. Moreover, there is the possibility to write a list of terms that will then be highlighted if found within the posts extracted.

The algorithm is based on Python, Selenium and Beautiful Soup, hence to run the code it will be necessary to access the social's account page of a personal profile.

The main file serves as the front end for the user, while the code lines for the scraper are within the src folder.

### Note that some small asjustements to the code find_element parts are periodically required since the html paths considered by the algorithm are often changed in the source code.

In the final output I included only the information of interest for my task (the text and the date), however the scraper allows you to export almost all the information available within the post.
Moreover, all the scraped posts are saved in a pickled dictionary in order to avoid extracting them again when visualizing multiple queries with overlapping posts.

Thank you for your attention.
Hope you enjoyed :)


