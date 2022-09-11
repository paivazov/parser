from main import Parser

if __name__ == '__main__':
    # with open("source.html", "r", encoding="utf-8") as file:
    #     parse_html(file.read())

    # print(convert_date_format())
    # parse_html()
    parser = Parser(start_page=1)
    parser.parse_html_page()
    # print(parse_price('No information'))