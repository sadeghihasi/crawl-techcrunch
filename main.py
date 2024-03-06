import argparse

import requests
from retrying import retry

from db_utilities.models import Post, PostTags, Tag, Author, Category

# Define the output file path for the report
REPORT_OUTPUT_FILE_PATH = 'output.tsv'


# Retry decorator to make a resilient HTTP request
@retry(stop_max_attempt_number=3, wait_fixed=100)
def make_request(url):
    """ Make get request
    """
    response = requests.get(url, timeout=(3, 10))
    response.raise_for_status()
    return response


# Function to crawl Libgen for a given keyword
def crawl_techcrunch():
    for page in range(1, 501):
        url = f"https://techcrunch.com/wp-json/tc/v1/magazine?page{page}&es=true&cachePrevention=0"
        response = make_request(url=url)

        posts = response.json()
        for post in posts:
            post_id = post["id"]
            link = post["link"]
            title = post["title"]["rendered"]
            author_id = post["author"]
            author_name = post["yoast_head_json"]["author"]

            category_id = post["primary_category"]["term_id"]
            category_name = post["primary_category"]["name"]
            tags_id = post["tags"]
            tags_name = post["yoast_head_json"]["schema"]["@graph"][0]["keywords"]

            category_object_id = Category.get_or_create(id=category_id, name=category_name)
            author_object_id = Author.get_or_create(id=author_id, author_name=author_name)
            post_object_id = Post.get_or_create(
                id=post_id, link=link, title=title, category=category_object_id, author=author_object_id
            )
            for number, tag_id in enumerate(tags_id):
                tag_id_object = Tag.get_or_create(id=tag_id, name=tags_name[number])
                PostTags.get_or_create(tag=tag_id_object, post=post_object_id)


def search_in_techcrunch(keyword):
    pass


# Main block to handle command-line arguments
if __name__ == "__main__":
    # Parsing command-line arguments
    parser = argparse.ArgumentParser(description='Keyword to search and report in the techcrunch site')
    parser.add_argument('--keyword', '-k', required=False, help='Keyword to search in the techcrunch site!')
    args = parser.parse_args()

    # Perform actions based on command-line arguments
    if args.keyword:
        search_in_techcrunch(args.keyword)
    else:
        crawl_techcrunch()
