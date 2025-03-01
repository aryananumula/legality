import requests
from bs4 import BeautifulSoup
import time


def scrape_lawyer_directory(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; LawFirmScraper/1.0)",
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(
            f"Error: Unable to retrieve page (Status code: {response.status_code})")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # Modify the selector below to match the structure of the website you wish to scrape.
    # Here we assume each lawyer's info is in a <div class="lawyer-profile">.
    profiles = soup.find("div", class_="has-no-top-margin")
    columns = profiles.find("div").find_all("div")

    results = []

    for column in columns:
        pars = column.find_all("p")
        for par in pars:
            results.append(par.find("a").get("href"))

    return results


if __name__ == "__main__":
    # Replace the URL with the actual directory page you want to scrape.
    url = "https://www.justia.com"

    lawyer_data = scrape_lawyer_directory(url)

    for lawyer_category in lawyer_data:
