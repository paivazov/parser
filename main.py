import csv
import re
from datetime import datetime
from typing import Union

import requests
from bs4 import BeautifulSoup, Tag
from fake_user_agent import user_agent
from requests import Response

"""NO_INFO = "No information"

# 
def get_response(page: int = 1) -> Union[Response, str]:
    domain = 'https://www.kijiji.ca/'
    path = f"b-apartments-condos/city-of-toronto/page-{page}/c37l1700273"
    headers = {"user-agent": user_agent("chrome")}
    response = requests.get(
        domain + path,
        headers=headers)
    status = response.status_code
    if status == 200:
        return response
    else:
        return f"Can't connect to {domain}. Error code is {status}."

# 
def convert_date_format(date: str) -> str:
    if date == NO_INFO:
        return NO_INFO
    try:
        return str(datetime.strptime(date, "%d-%m-%Y"))
    except ValueError:
        return datetime.now().strftime("%d-%m-%Y")

# 
def parse_price(price: str) -> dict:
    re_price = re.search(r"(\$)(\d+,\d+)", price)
    result = {
        "currency": NO_INFO,
        "price": NO_INFO
    }
    if re_price is not None:
        parsed_price = re_price.groups()
        result.update(currency=parsed_price[0], price=parsed_price[1])
        return result
    return result

# 
def extract_bedrooms_info(bedrooms_text: str) -> str:
    re_digits = re.compile(fr"\d+|{NO_INFO}")
    bedrooms_regex = re_digits.search(bedrooms_text)
    if bedrooms_regex is None:
        return bedrooms_text
    else:
        return bedrooms_regex.group()

# 
def extract_text_or_no_info(bs4_tag: Union[Tag, None]) -> str:
    return NO_INFO if bs4_tag is None else bs4_tag.text.strip()

# 
def find_attr_in_tag_or_no_info(bs4_tag: Union[Tag, None], attr: str) -> str:
    return NO_INFO if bs4_tag is None else bs4_tag[attr]


def parse_html():
    result = []

    # print(re_digits.search("studio"))
    # response = get_response(1)
    # print(response)
    # with open("sourcccce.html", "w", encoding="utf-8") as f:
    #     f.write(str(response))

    page = 1
    while True:
        response = get_response(page)
        time.sleep(2)
        # response = html
        if isinstance(response, str):
            print(response)
            break
        else:
            soup = BeautifulSoup(response.text, "lxml")

        ads = soup.find_all("div", class_="clearfix")
        # ads = [] if ads is None else ads

        for ad in ads:
            bedrooms = extract_bedrooms_info(extract_text_or_no_info(
                ad.find_next("span", class_="bedrooms")))

            location = ad.find_next("div", class_="location")

            city = location.find_next("span", class_="")
            date = location.find_next("span", class_="date-posted")

            image = ad.find_next("source")
            title = ad.find_next("div", class_="title")

            price = ad.find_next("div", class_="price")

            description = ad.find_next("div", class_="description")
            parsed_price = parse_price(extract_text_or_no_info(price))
            res = {
                "image": find_attr_in_tag_or_no_info(image, "srcset"),
                "ad_url": "ddd" + find_attr_in_tag_or_no_info(title.find("a"),
                                                              "href"),
                "title": extract_text_or_no_info(title),
                "currency": parsed_price["currency"],
                "price": parsed_price["price"],
                "city": extract_text_or_no_info(city),
                "date": convert_date_format(extract_text_or_no_info(date)),
                "description": extract_text_or_no_info(description),
                "bedrooms": bedrooms
            }
            result.append(res)

            print(res)
        # print(f"page {page} has benn parsed with result: \n")
        # print(result[page-1]["date"])
        print("\n\n\n\n\n\n\n")
        # res = ad.find("div", class_="descriptionccc")
        # print("No info" if res is None else res.text.strip())
        try:
            soup.find("div", class_="pagination").find("a", title="Next")
        except AttributeError:
            print("No more pages")
            with open("some.txt", "w") as f:
                f.write(str(result))
            break
        # finally:
        #     break

        page += 1

    # print(cards)
    # with open("sourcccce.html", "w", encoding="utf-8") as f:
    #     f.write(str(cards))"""


class Parser:
    def __init__(self, page: int = 1):
        self.page = page
        self.__NO_INFO = "No information"
        self.domain = 'https://www.kijiji.ca'

    def get_response(self) -> Union[Response, str]:
        path = f"/b-apartments-condos/city-of-toronto/page-{self.page}/c37l1700273"
        headers = {"user-agent": user_agent("chrome")}
        response = requests.get(
            self.domain + path,
            headers=headers)
        status = response.status_code
        if status == 200:
            return response
        else:
            return f"Can't connect to {self.domain}. Error code is {status}."

    def convert_date_format(self, date: str) -> str:
        # print(date)
        if date == self.__NO_INFO:
            return self.__NO_INFO
        try:
            return datetime.strptime(date, "%d/%m/%Y").strftime("%d-%m-%Y")
        except ValueError:
            return datetime.now().strftime("%d-%m-%Y")

    def parse_price(self, price: str) -> dict:
        re_price = re.search(r"(\$)(\d+,\d+)", price)
        result = {
            "currency": self.__NO_INFO,
            "price": self.__NO_INFO
        }
        if re_price is not None:
            parsed_price = re_price.groups()
            result.update(currency=parsed_price[0], price=parsed_price[1])
            return result
        return result

    def extract_bedrooms_info(self, bedrooms_text: str) -> str:
        re_digits = re.compile(fr"\d+|{self.__NO_INFO}")
        bedrooms_regex = re_digits.search(bedrooms_text)
        if bedrooms_regex is None:
            return bedrooms_text
        else:
            return bedrooms_regex.group()

    def _extract_text_or_no_info(self, bs4_tag: Union[Tag, None]) -> str:
        return self.__NO_INFO if bs4_tag is None else bs4_tag.text.strip()

    def _find_attr_in_tag_or_no_info(self, bs4_tag: Union[Tag, None],
                                     attr: str) -> str:
        return self.__NO_INFO if bs4_tag is None else bs4_tag[attr]

    def parse_html(self):
        result = []
        # print(re_digits.search("studio"))
        # response = get_response(1)
        # print(response)
        # with open("sourcccce.html", "w", encoding="utf-8") as f:
        #     f.write(str(response))
        # page = 1
        while True:
            response = self.get_response()
            # time.sleep(2)
            # response = html
            # soup = BeautifulSoup(response, "lxml")
            if isinstance(response, str):
                print(response)
                break
            else:
                soup = BeautifulSoup(response.text, "lxml")
            ads = soup.find_all("div", class_="clearfix")
            # ads = [] if ads is None else ads
            for ad in ads:
                bedrooms = self.extract_bedrooms_info(
                    self._extract_text_or_no_info(
                        ad.find_next("span", class_="bedrooms")))
                location = ad.find_next("div", class_="location")
                city = location.find_next("span", class_="")
                date = location.find_next("span", class_="date-posted")
                image = ad.find_next("source")
                title = ad.find_next("div", class_="title")
                price = ad.find_next("div", class_="price")
                description = ad.find_next("div", class_="description")
                parsed_price = self.parse_price(
                    self._extract_text_or_no_info(price))


                res = {
                    "image": self._find_attr_in_tag_or_no_info(image, "srcset"),
                    "ad_url": self.domain + self._find_attr_in_tag_or_no_info(
                        title.find("a"),
                        "href"),
                    "title": self._extract_text_or_no_info(title),
                    "currency": parsed_price["currency"],
                    "price": parsed_price["price"],
                    "city": self._extract_text_or_no_info(city),
                    "date": self.convert_date_format(self._extract_text_or_no_info(date)),
                    "description": self._extract_text_or_no_info(description),
                    "bedrooms": bedrooms
                }
                result.append(res)

                print(res)

            print("\n\n\n\n\n\n\n")
            with open("dump.csv", 'w', encoding='UTF-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(result[0].keys())

                for row in result:
                    writer.writerow(row.values())
            try:
                soup.find("div", class_="pagination").find("a", title="Next")
            except AttributeError:
                print("No more pages")
                with open("some.txt", "w") as f:
                    f.write(str(result))
                break
            # finally:
            #     break
            if self.page == 5:
                break
            self.page += 1


if __name__ == '__main__':
    # with open("source.html", "r", encoding="utf-8") as file:
    #     parse_html(file.read())

    # print(convert_date_format())
    # parse_html()
    parser = Parser(page=1)
    parser.parse_html()
    # with open("source.html", "r", encoding="utf-8") as file:

        # parser.parse_html(file.read())
    # print(parse_price('No information'))
