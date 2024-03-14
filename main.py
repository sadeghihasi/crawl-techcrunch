import argparse
import logging
import os

from db_utilities.database_manager import DatabaseManager
from db_utilities.models import Post, PostTags, Tag, Author, Category, KeywordResult, Keyword, KeywordResultItem
from local_settings import DATABASE, BASE_DIR
from tasks import search_in_techcrunch
from tasks import app


# Main block to handle command-line arguments
if __name__ == "__main__":
    logging.basicConfig(filename=os.path.join(BASE_DIR, 'time_log.log'),
                        encoding='utf-8', level=logging.DEBUG)
    logging.info('main.py started!')

    database_manager = DatabaseManager(
        database_name=DATABASE['NAME'],
        user=DATABASE['USER'],
        password=DATABASE['PASSWORD'],
        host=DATABASE['HOST'],
        port=DATABASE['PORT'],
    )

    models = (Post, PostTags, Tag, Author, Category, Keyword, KeywordResult, KeywordResultItem)
    database_manager.create_tables(models)

    # Parsing command-line arguments
    parser = argparse.ArgumentParser(description='Keyword to search and report in the techcrunch site')
    parser.add_argument('--keyword', '-k', required=False, help='Keyword to search in the techcrunch site!')
    args = parser.parse_args()

    # Perform actions based on command-line arguments
    keyword = args.keyword
    if keyword:
        logging.info(f'Lets report. keyword is [{keyword}]')
        search_in_techcrunch.delay(keyword=keyword)
    else:
        app.start()
