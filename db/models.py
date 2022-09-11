from sqlalchemy import Column, String, Text, Date

from . import Base


class ParsedData(Base):
    __tablename__ = "parsed_data"

    ad_link = Column(String(250), primary_key=True)
    image_url = Column(String(250))
    title = Column(String(250))
    currency = Column(String(15))
    price = Column(String(15))
    city = Column(String(50))
    description = Column(Text)
    bedrooms = Column(String)
    date = Column(String(10))





