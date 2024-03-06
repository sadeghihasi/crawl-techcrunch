from db_utilities.database_manager import DatabaseManager
from db_utilities.models import Post, PostTags, Tag, Author, Category, KeywordResult, Keyword, KeywordResultItem
from settings import DATABASE


def create_table(model):
    database_manager = DatabaseManager(
        database_name=DATABASE['NAME'],
        user=DATABASE['USER'],
        password=DATABASE['PASSWORD'],
        host=DATABASE['HOST'],
        port=DATABASE['PORT'],
    )

    database_manager.create_tables(models=model)


if __name__ == "__main__":
    create_table([Post, PostTags, Tag, Author, Category, Keyword, KeywordResult, KeywordResultItem])
