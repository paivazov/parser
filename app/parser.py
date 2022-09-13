import re
import time
from datetime import datetime
from typing import Union

import requests
from bs4 import BeautifulSoup, Tag
from fake_user_agent import user_agent
from requests import Response
from requests.exceptions import ChunkedEncodingError
from sqlalchemy import select

from db import get_session
from app.models import ParsedData


class Parser:
    def __init__(self, start_page: int = 1):
        self.page = start_page
        self.__NO_INFO = "No information"
        self.domain = 'https://www.kijiji.ca'
        self.session = get_session()

    def get_response(self, path) -> Union[Response, str]:
        """Processes request in path
        Args:
            path: URL path without domain
        """
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
        """Parses string in definite format and
        converts date to required datestamp.
        Args:
            date: date in format dd/mm/yyyy
        """
        date_stamp = "%d-%m-%Y"
        if date == self.__NO_INFO:
            return self.__NO_INFO
        try:
            return datetime.strptime(date, "%d/%m/%Y").strftime(date_stamp)
        except ValueError:
            return datetime.now().strftime(date_stamp)

    def parse_price(self, price: str) -> dict:
        """Parses price string and decomposes it onto
        dict with attrs 'currency' and 'price'
        Args:
            price: Price string
        """
        re_price = re.search(r"(\$)(\d+,\d+)", price)
        result = {"currency": self.__NO_INFO, "price": self.__NO_INFO}
        if re_price is not None:
            parsed_price = re_price.groups()
            result.update(currency=parsed_price[0], price=parsed_price[1])
            return result
        return result

    def extract_bedrooms_info(self, bedrooms_text: str) -> str:
        """
        Args:
            bedrooms_text: string of bedrooms content
        Returns:
            number of bedrooms, generic text or 'no info' message
        """
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

    def create_prepared_datarecord(self, ad_tag: Tag) -> dict:
        """Decomposes advertisement tag and extracts data from it
        Args:
             ad_tag: advertisement bs4 tag
        Returns:
            dict of extracted and decomposed data
        """
        bedrooms = self.extract_bedrooms_info(
            self._extract_text_or_no_info(
                ad_tag.find_next("span", class_="bedrooms")
            )
        )

        location_tag = ad_tag.find_next("div", class_="location")
        city = self._extract_text_or_no_info(
            location_tag.find_next("span", class_="")
        )
        date = self.convert_date_format(
            self._extract_text_or_no_info(
                location_tag.find_next("span", class_="date-posted")
            )
        )

        image = ad_tag.find_next("div", class_="image")
        image_url = self._find_attr_in_tag_or_no_info(
            image.find_next("source"), "data-srcset"
        )

        title_tag = ad_tag.find_next("div", class_="title")
        ad_path = self._find_attr_in_tag_or_no_info(
            title_tag.find("a"), "href"
        )
        title = self._extract_text_or_no_info(title_tag)

        description = self._extract_text_or_no_info(
            ad_tag.find_next("div", class_="description")
        )

        price = ad_tag.find_next("div", class_="price")
        parsed_price = self.parse_price(self._extract_text_or_no_info(price))

        return {
            "bedrooms": bedrooms,
            "image_url": image_url,
            "ad_link": self.domain + ad_path,
            "title": title,
            "currency": parsed_price["currency"],
            "price": parsed_price["price"],
            "city": city,
            "date": date,
            "description": description,
        }

    def parse_site(self):
        path = f"/b-apartments-condos/city-of-toronto/page-{self.page}/c37l1700273"

        while True:
            print(f"\nParsing page.")

            response = self.get_response(path)
            time.sleep(2)
            if isinstance(response, str):
                print(response)
                break
            else:
                soup = BeautifulSoup(response.text, "lxml")

            ads = soup.find_all("div", class_="clearfix")
            for ad in ads:
                with self.session() as session:
                    """It's better to have bulk update.
                    Nevertheless, this two queries is being used to check
                    if each record is already in database"""
                    record = ParsedData(**self.create_prepared_datarecord(ad))

                    existing_record = session.execute(
                        select(ParsedData).where(
                            ParsedData.ad_link == record.ad_link
                        )
                    )
                    if existing_record.fetchone() is None:
                        session.add(record)
                        session.commit()
                    else:
                        print(f"{record.ad_link} is already on db.")

            print("Parsed data of this page has been inserted to database.")
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
