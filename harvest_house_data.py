from playwright.sync_api import Playwright, sync_playwright, expect
import time
import csv

data_path = "house_data"

# Read the data with the urls from houses.
with open('pararius_house_urls.csv', newline='') as csvfile:
    data = csv.reader(csvfile, delimiter=' ', quotechar='|')
    
    house_urls = []
    for url in data:
        house_urls = house_urls + url

# Accidently included column header to loop over.
house_urls.pop(0)


def run(playwright: Playwright) -> None:

    # Open a new webpage.    
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Go to the pararius website to collect urls.
    page.goto("https://www.pararius.nl/koopwoningen/nederland")

    # Click on text=Akkoord
    page.locator("text=Akkoord").click()

    page_idx = 1
    # Visit each url and write the page to html.
    for url in house_urls:
        
        page.goto(f"https://{url}")
        time.sleep(3)

        html_doc = page.content()
        with open(f"{data_path}/house_data_p{page_idx}.html", "w") as file:
            file.write(html_doc)
 
        print(f"Number of scraped webpages: {page_idx}")
        page_idx += 1

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
   run(playwright)