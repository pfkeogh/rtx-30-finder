import requests
from html.parser import HTMLParser


class NeweggScraper(HTMLParser):

    def error(self, message):
        pass

    def __init__(self, *, convert_charrefs=True):
        super().__init__(convert_charrefs=convert_charrefs)
        self.item_grid = False
        self.item_grid_depth = None
        self.item_container = False
        self.item_container_depth = None
        self.depth = 0
        self.items_encountered = 0
        self.card_data = {}
        self.card_urls = {}

    def reset_page_vars(self):
        self.item_grid = False
        self.item_grid_depth = None
        self.item_container = False
        self.item_container_depth = None
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        self.depth += 1
        for key, value in attrs:
            if key == "class" and value == "item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell":
                self.item_grid = True
                self.item_grid_depth = self.depth
            if self.item_grid and key == "class" and value == "item-container":
                self.item_container += True
                self.item_container_depth = self.depth
                self.items_encountered += 1
            if self.item_container and tag == "a" and key == "href" and self.depth == self.item_container_depth + 1:
                self.card_urls[self.items_encountered] = value

    def handle_endtag(self, tag):
        if self.item_container_depth == self.depth:
            self.item_container = False
        if self.item_grid_depth == self.depth:
            self.item_grid = False
        self.depth -= 1

    def handle_data(self, data):
        index = self.items_encountered
        if self.item_container and self.item_grid:
            if self.card_data.get(index) is None:
                self.card_data[index] = data
            else:
                self.card_data[index] += data

    def search(self, search_file=None):

        for page in [1, 2, 3]:
            if search_file is None:
                response = requests.get(url=f"https://www.newegg.com/p/pl?N=100007709%20601357282&page={page}")
                search_text = response.text
            else:
                file = open(search_file, 'r')
                search_text = file.read()
            self.feed(search_text)

            for key, val in self.card_data.items():
                if "OUT OF STOCK" not in val:
                    print(f"Stocked!: {val}")
                    print(f"Go to: {self.card_urls[key]}")
            self.reset_page_vars()
        print(f"Cards searched: {self.items_encountered}")


def check_newegg():
    scraper = NeweggScraper()
    # path = "/Users/patrickkeogh/Library/Application Support/JetBrains/PyCharm2020.2/scratches/scratch.html"
    # scraper.search(path)
    scraper.search()


if __name__ == '__main__':
    check_newegg()


