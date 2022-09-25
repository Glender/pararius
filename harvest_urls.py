from playwright.sync_api import Playwright, sync_playwright, expect
import time

# Specify how many pages you want to scrape.
nr_of_pages = 66
base_url = "https://www.pararius.nl/koopwoningen/nederland/page-"
urls = [base_url + str(idx) for idx in range(1, nr_of_pages + 1)]

# Choose where you want to store the data.
data_path = "data"


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
    for url in urls:
        
        page.goto(url)
        time.sleep(5)

        html_doc = page.content()
        with open(f"{data_path}/page_{page_idx}.html", "w") as file:
            file.write(html_doc)

        page_idx += 1 

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
   run(playwright)
