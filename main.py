from bs4 import BeautifulSoup
from BooksToScrape import BooksToScrape
import time
import asyncio

if __name__ == "__main__" and hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if __name__ == "__main__":
    # Start time
    start_time = time.time()

    # Kreiramo instancu klase i pokrećemo asinkrono izvršavanje
    parser = BooksToScrape()
    asyncio.run(parser.run())

    # Execution time
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.2f} sec!")
