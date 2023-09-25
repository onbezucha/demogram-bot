import sys
import globals
import argparse
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class Page:
    def __init__(self, url=""):
        self.title = ""
        self.url = url
        self.status_code = 0
        self.links = []
        self.forms = []

    def __str__(self):
        return f"{self.title};{self.url};{self.status_code};{self.links};{self.forms}\n"


def define_args():
    # Define arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="URL to scrape")
    parser.add_argument("-hh", "--headless", help="Run in headless mode")
    parser.add_argument("-sm", "--skip-map", help="Skip map generation from crawling with provided file")
    # Parse arguments
    args = parser.parse_args()
    print(args)

    # Check if URL is provided - this is a required argument
    if args.url:
        # Set the global variable, for easy access
        globals.url = args.url
        globals.links.append(args.url)
        # Set the domain name from url
        globals.domain = args.url.split("/")[2]
    else:
        # If URL is not provided, exit the program
        print("URL not provided. Exiting...")
        sys.exit(1)

    # Check if headless mode is enabled, by default we have false
    if args.headless:
        # Set the global variable, for easy access
        # Turn the number into a boolean
        globals.headless = bool(int(args.headless))

    # Check if skip map is present and load data
    if args.skip_map:
        # Set the global variable, for easy access
        # Turn the number into a boolean
        globals.skip = True
        load_pages_from_csv(args.skip_map)


def get_driver():
    options = Options()
    if globals.headless:
        options.add_argument("--headless")

    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    # define path of driver form globals.driver
    driver = webdriver.Chrome(options=options)
    return driver


def crawl(driver, index):
    if globals.crawl_index < len(globals.links):
        # get current link
        current_link = globals.links[index]
        # init page object
        page = Page(current_link)

        # visit current link
        driver.get(current_link)

        # use request to get status code
        r = requests.get(current_link)
        page.status_code = r.status_code

        # get title
        page.title = driver.title

        # get all <a> elements and look for same domain links
        link_elements = driver.find_elements(By.TAG_NAME, "a")

        # store total number of links
        page.links = len(link_elements)
        for linkEl in link_elements:
            link = linkEl.get_attribute("href")
            if link.endswith(".pdf") or link.endswith(".jpg") or link.endswith(".png") or link.endswith(".jpeg"):
                continue
            # link already recorded
            if link in globals.links:
                continue
            # link is None or empty
            if link is None:
                continue
            # link is empty
            if link == "":
                continue
            if globals.domain not in link:
                continue
            # add link to links
            print("Adding link", link)
            globals.links.append(link)

        # get all <form> elements
        form_elements = driver.find_elements(By.TAG_NAME, "form")
        page.forms = len(form_elements)

        globals.pages.append(page)
        globals.crawl_index += 1
        crawl(driver, globals.crawl_index)


def store_pages_to_csv():
    with open("map.csv", "w") as f:
        f.write("title;url;status_code;links;forms\n")
        for page in globals.pages:
            f.write(str(page))


def load_pages_from_csv(file_name):
    try:
        with open(file_name, "r") as f:
            f.readline()
            for line in f.readlines():
                # init page
                line = line.strip()
                title, url, status_code, links, forms = line.split(";")
                page = Page(url)
                page.title = title
                page.status_code = status_code
                page.links = links
                page.forms = forms
                globals.pages.append(page)
                # add link to links
                globals.links.append(url)
    except FileNotFoundError:
        print("File not found. Skipping...")
        globals.skip = False
        globals.pages = []
        globals.links = []


def fill_forms(driver):
    for page in globals.pages:
        driver.get(page.url)
        driver.implicitly_wait(2)
        print(f"Visiting {page.url}")
        form_elements = driver.find_elements(By.TAG_NAME, "form")
        for form in form_elements:
            try:
                # find all inputs
                input_elements = form.find_elements(By.TAG_NAME, "input")
                for input_el in input_elements:
                    # check type
                    input_type = input_el.get_attribute("type")
                    if input_type == "text":
                        input_el.send_keys("54321")
                        print_fill_in_log(input_el)
                    elif input_type == "email":
                        input_el.send_keys("pupek@velky.wtf")
                        print_fill_in_log(input_el)
                    elif input_type == "password":
                        input_el.send_keys("987654321")
                        print_fill_in_log(input_el)
                    elif input_type == "checkbox" or input_type == "radio":
                        input_el.click()
                        print_click_log("checkbox/radio")

                # find all selects
                select_elements = form.find_elements(By.TAG_NAME, "select")
                for select_el in select_elements:
                    # find all options
                    option_elements = select_el.find_elements(By.TAG_NAME, "option")
                    if len(option_elements) > 0:
                        option_elements[0].click()
                        print_fill_in_log(select_el)

                # find all textareas
                textarea_elements = form.find_elements(By.TAG_NAME, "textarea")
                for textarea_el in textarea_elements:
                    textarea_el.send_keys("test123321")
                    print_fill_in_log(textarea_el)

                # find buttons
                button_elements = form.find_elements(By.TAG_NAME, "button")
                for button_el in button_elements:
                    button_type = button_el.get_attribute("type")
                    if button_type is None:
                        button_el.click()
                        print_click_log("button unknown type")
                    if button_type == "click":
                        button_el.click()
                        print_click_log("button click type")
                    if button_type == "submit":
                        button_el.click()
                        print_click_log("button submit type")

            except Exception as e:
                print('Error filling form')
                print(e)
                continue


# print log functions
def print_fill_in_log(element):
    print(element.get_attribute("name"), element.get_attribute("value"))


def print_click_log(tag):
    print(tag, "clicked")


def main():
    define_args()
    driver = get_driver()
    if globals.skip is False:
        crawl(driver, globals.crawl_index)
        store_pages_to_csv()
    fill_forms(driver)
    driver.close()


if __name__ == '__main__':
    main()
