library(XML)
library(stringr)
library(RCurl)
library(xml2)
library(rvest)
library(curl)

# Examine the number of pages that you want to scrape
# given the underlying url https://www.pararius.nl/..
nr_of_websites <- 66
urls <- sprintf("https://www.pararius.nl/koopwoningen/nederland/page-%d", 1:nr_of_websites)

# Set wd to store url files
mkdirs <- function(path) {
  if(!file.exists(path)) {
    mkdirs(dirname(path))
    dir.create(path)
  }
} 
mkdirs("~/data")
setwd("data")

# Get the desired data
for (i in 1:length(urls)) {
  
  # Read html files using curl
  page <- rvest::read_html(
    curl(urls[i], handle = curl::new_handle(
      "useragent" = str_c(R.version$platform, R.version$version.string,sep=", ")
      )
    )
  )
  
  # Save html file 
  write_xml(page, file = sprintf("page%d.html", 1:length(urls))[i])
  
  # Set timer on sleep to destress servers
  Sys.sleep(5)  # in seconds
  
  # Poormans Counter
  if (i%%1==0) cat("Number of extracted pages:",i, "-", urls[i], "\n")  
  
}
