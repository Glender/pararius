library(stringr)
library(XML)
library(readr)

# Define all links.
# dir should be the location of the scraped htmls.
html_files <- dir()
files_list <- vector("list", length = length(html_files))

idx <- 1
for(website in html_files){
  
  # Read html file and extract links to house website.
  html_parsed <- XML::htmlParse(website)
  files <- XML::xpathSApply(
    html_parsed, path = "//h2/a", XML::xmlAttrs
  )
  
  # Transform to right object
  # and store data in the container.
  links <- as.vector(t(files)[,-2])
  links <- stringr::str_c("www.pararius.nl", links)
  
  files_list[[idx]] <- links
  idx <- idx + 1
  
  cat("# Extracted data from webpage:", website, "\n")  
}

# merge all results
all_urls <- unique(do.call(c, files_list))
cat("Scraped", length(all_urls), "urls.")

df <- data.frame(all_urls)
readr::write_csv(df, "pararius_house_urls.csv")