from argparse import ArgumentParser

from app.parser import Parser

if __name__ == '__main__':

    ap = ArgumentParser()
    ap.add_argument(
        'start_page', type=int, help='Page which parser starts work from.'
    )

    try:
        args = ap.parse_args()
        parser = Parser(start_page=args.start_page)
        parser.parse_site()
    except Exception as e:
        print(e)
        ap.print_help()
