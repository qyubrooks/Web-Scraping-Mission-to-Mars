# Web-Scraping-Mission-to-Mars

Build a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page. 

## Step 1: Scrapping

### NASA Mars News
* Script collects the latest News Title and Paragraph Text.

### JPL Mars Space Images - Featured Image
* Script finds the image url for the current Featured Mars Image and assigns the url string of the full size image.

### Mars Weather
* Script visits the Mars Weather twitter account and scrapes the latest Mars weather tweet.

### Mars Facts
Script visit the Mars Facts webpage and uses Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

### Mars Hemispheres
Script visits the USGS Astrogeology site and obtains the full resolution images for each of Mar's hemispheres.


## Step 2: MongoDB and Flask Application

Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.

![mars](Mission_to_Mars_Screen_Capture.png)
