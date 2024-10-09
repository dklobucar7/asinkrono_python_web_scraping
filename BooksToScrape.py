from bs4 import BeautifulSoup
import re
import aiohttp
import asyncio


class BooksToScrape:
    def __init__(self):
        self.results = []

    # ---------------------------------------------------------------------------------------------
    # INFRAKSTRUKTURA
    # DOHVAĆA HTML SADRŽAJ STRANICE
    async def fetch_page(self, session, page_num):
        # Kreiramo URL za željeni broj stranice
        url = f"https://books.toscrape.com/catalogue/page-{page_num}.html"

        # Kreiramo session i kako će izgledati GLAVNI task, u smislu da prvo parsiramo stranicu, a pod parse() ćemo definirati detaljnije što želimo
        async with session.get(url) as response:
            page_content = await response.text()  # Asinkroni zahtjev
            return BeautifulSoup(page_content, "html.parser")  # Parsiranje HTML-a

    # KREIRANJE ASINKRONIH TASKOVA
    async def fetch_all_pages(self, session, total_pages):
        tasks = []

        # Kreiramo zadatke za svaku stranicu koje će se izvoditi paralelno
        for page_num in range(1, total_pages + 1):
            tasks.append(self.fetch_page(session, page_num))

        # Čekamo da se svi zadaci završe, umjesto PAGES, treba pisati RESULTS
        pages = await asyncio.gather(*tasks)
        return pages

    # --------------------------------------------------------------------------------------------
    # PARSIRANJE ONOGA ŠTO ŽELIM
    def extract_book_info(self, item):
        # Izdvajamo podatke o knjizi
        title = item.find("h3").find("a").text
        # price
        price_tag = item.find("p", {"class": "price_color"}).text
        price = float(re.sub(r"[^\d.]", "", price_tag))  # Cleaning the price

        # Check stock availability
        stock_tag = (
            item.find("p", {"class": "instock availability"}).text.strip().lower()
        )
        stock = 1 if stock_tag == "in stock" else 0

        # Extract book rating
        rating_tag = item.find("p", {"class": "star-rating"})["class"][1]
        rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
        rating = rating_map.get(rating_tag, 0)

        # Return a dictionary with the book information
        return {"title": title, "price": price, "stock": stock, "rating": rating}

    # -----------------------------------------------------------------------------------------------------
    # OVO TREBA BITI U MAIN-u po meni jer ovo orkestira cijeli proces

    async def run(self):
        url = "https://books.toscrape.com/"
        async with aiohttp.ClientSession() as session:
            first_page_soup = await self.fetch_page(session, 1)
            current_page_info = first_page_soup.soup.find("li", {"class": "current"})

    # def get_total_pages(self, soup):
    #     current_page_info = soup.find("li", {"class": "current"})
    #     if current_page_info:
    #         total_pages = int(current_page_info.text.strip().split(" ")[-1])
    #         return total_pages
    #     else:
    #         return 1

    def parse(self, total_pages):
        # Parse all the pages
        for page_num in range(1, total_pages + 1):
            doc = self.fetch_page(page_num)
            list_items = doc.find_all(
                "li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"}
            )

            for item in list_items:
                self.results.append(self.extract_book_info(item))

        return self.results
