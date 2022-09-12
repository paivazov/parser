import re
import time
from datetime import datetime
from typing import Union

import requests
from bs4 import BeautifulSoup, Tag
from fake_user_agent import user_agent
from requests import Response
from requests.exceptions import ChunkedEncodingError

from db import get_session
from app.models import ParsedData


class Parser:
    def __init__(self, start_page: int = 1):
        self.page = start_page
        self.__NO_INFO = "No information"
        self.domain = 'https://www.kijiji.ca'
        self.session = get_session()

    def get_response(self, path) -> Union[Response, str]:
        headers = {"user-agent": user_agent("chrome")}
        link = self.domain + path
        print("Link: " + link)
        try:
            response = requests.get(link, headers=headers)
        except ChunkedEncodingError:
            return (
                "Connection broken because of invalid chunk length.\n"
                "Try to reconnect parser."
            )
        status = response.status_code
        if status == 200:
            return response
        else:
            return f"Can't connect to {self.domain}. Error code is {status}."

    def convert_date_format(self, date: str) -> str:
        date_stamp = "%d-%m-%Y"
        if date == self.__NO_INFO:
            return self.__NO_INFO
        try:
            return datetime.strptime(date, "%d/%m/%Y").strftime(date_stamp)
        except ValueError:
            return datetime.now().strftime(date_stamp)

    def parse_price(self, price: str) -> dict:
        re_price = re.search(r"(\$)(\d+,\d+)", price)
        result = {"currency": self.__NO_INFO, "price": self.__NO_INFO}
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

    def _find_attr_in_tag_or_no_info(
        self, bs4_tag: Union[Tag, None], attr: str
    ) -> str:
        return self.__NO_INFO if bs4_tag is None else bs4_tag[attr]

    def parse_html_page(self):
        path = f"/b-apartments-condos/city-of-toronto/page-{self.page}/c37l1700273"
        result = []
        while True:
            print(f"\nParsing page.")

            response = self.get_response(path)
            time.sleep(2)
            if isinstance(response, str):
                print(response)
                break
            else:
                soup = BeautifulSoup(response.text, "lxml")

            ads = soup.find_all("div", class_="container-results large-images")
            for ad in ads:
                bedrooms = self.extract_bedrooms_info(
                    self._extract_text_or_no_info(
                        ad.find_next("span", class_="bedrooms")
                    )
                )
                location = ad.find_next("div", class_="location")
                city = location.find_next("span", class_="")
                date = location.find_next("span", class_="date-posted")
                image = ad.find_next("source")
                title = ad.find_next("div", class_="title")
                price = ad.find_next("div", class_="price")
                description = ad.find_next("div", class_="description")
                parsed_price = self.parse_price(
                    self._extract_text_or_no_info(price)
                )

                result.append(
                    {
                        "image_url": self._find_attr_in_tag_or_no_info(
                            image, "srcset"
                        ),
                        "ad_link": self.domain
                        + self._find_attr_in_tag_or_no_info(
                            title.find("a"), "href"
                        ),
                        "title": self._extract_text_or_no_info(title),
                        "currency": parsed_price["currency"],
                        "price": parsed_price["price"],
                        "city": self._extract_text_or_no_info(city),
                        "date": self.convert_date_format(
                            self._extract_text_or_no_info(date)
                        ),
                        "description": self._extract_text_or_no_info(
                            description
                        ),
                        "bedrooms": bedrooms,
                    }
                )

            with self.session() as session:
                session.bulk_insert_mappings(ParsedData, result)
                session.commit()
                print(
                    "Parsed data of this page has been inserted to database."
                )
            path = soup.find("div", class_="pagination").find_next(
                "a", title='Next'
            )
            if path is None:
                print("No more pages. Parsing was stopped.")
                break
            else:
                path = path["href"]


if __name__ == '__main__':
    print(
        "To start parser script please run python entrypoint.py [page number]"
    )
