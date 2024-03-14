import logging
import random
import time

import requests
from bs4 import BeautifulSoup
from celery import Celery
from celery.schedules import crontab
from lxml import html
from retrying import retry

from db_utilities.models import Category, Tag, PostTags
from db_utilities.models import Post, Author, KeywordResult, Keyword, KeywordResultItem
from local_settings import SEARCH_URL, MAGAZINE_URL, DUPLICATED_POST_NUMBER, RANDOM_TILL_WAIT_TIME_BETWEEN_REQUESTS, \
    CELERY_BROKER

app = Celery('tasks', broker=CELERY_BROKER)

# Set Celery logging level to DEBUG
app.conf.update(
    result_expires=3600,
    timezone='Asia/Tehran',
    worker_log_format='[%(asctime)s: %(levelname)s/%(processName)s] %(message)s',
)


# Retry decorator to make a resilient HTTP request
@retry(stop_max_attempt_number=3, wait_fixed=100)
def make_request(url):
    """ Make get request
    """
    time.sleep(random.randint(1, RANDOM_TILL_WAIT_TIME_BETWEEN_REQUESTS))
    response = requests.get(url, timeout=(3, 10))
    response.raise_for_status()
    return response


# Function to crawl Libgen for a given keyword
@app.task
def crawl_techcrunch():
    dpn = DUPLICATED_POST_NUMBER
    # for page in range(1, 501):
    for page in range(1, 4):
        url = MAGAZINE_URL.format(PAGE_NUMBER=page)
        response = make_request(url=url)

        posts = response.json()
        for post in posts:
            post_id = post["id"]
            link = post["link"]
            title = post["title"]["rendered"]
            author_name = post["yoast_head_json"]["author"]

            category_name = post["primary_category"]["name"]
            tags_id = post["tags"]
            tags_name = post["yoast_head_json"]["schema"]["@graph"][0]["keywords"]

            category_object = Category.get_or_create(name=category_name)[0]
            author_object = Author.get_or_create(name=author_name)[0]
            post_objects = Post.get_or_create(
                id=post_id, link=link, title=title, category=category_object, author=author_object
            )
            if not post_objects[1]:
                # Post exist
                dpn -= 1

            post_object = post_objects[0]
            for number, tag_id in enumerate(tags_id):
                tag_object = Tag.get_or_create(id=tag_id, name=tags_name[number])[0]
                PostTags.get_or_create(tag=tag_object, post=post_object)

        if dpn <= 0:
            break


@app.task
def search_in_techcrunch(keyword):
    # return "Hasan Sadeghi"
    keyword_object = Keyword.get_or_create(name=keyword)[0]
    keywordResult_object = KeywordResult.get_or_create(keyword=keyword_object)[0]

    page_number = 1

    while True:
        url = SEARCH_URL.format(KEYWORD=keyword, PAGE_NUMBER=1)
        response = make_request(url=url)

        soup = BeautifulSoup(response.text, 'html.parser')
        root = html.fromstring(str(soup))

        # Extract information for each book
        posts = root.xpath("/html/body/div//div/ol/li/div/ul/li")
        if posts:
            for post in posts[:-1]:
                logging.info(f'Post {post} found!. Lets extract its info :>')
                title = post.xpath("./div/h4/a")[0].text_content()
                author = post.xpath("./div/div/p/span[1]")[0].text_content()

                link = post.xpath("./div[2]/h4/a/@href")[0]

                response = make_request(url=link)
                soup = BeautifulSoup(response.text, 'html.parser')
                root = html.fromstring(str(soup))
                post_id = int(root.xpath(
                    "/html/head/link[contains(@href,'https://techcrunch.com/wp-json/wp/v2/posts')]/@href"
                )[0].replace("https://techcrunch.com/wp-json/wp/v2/posts/", ""))

                try:
                    category = root.xpath("/html//header/div/div/a[contains(@href, 'category')]")[0].text_content()

                except IndexError:
                    category = "Article"

                category_object = Category.get_or_create(name=category)[0]
                author_object = Author.get_or_create(name=author)[0]
                post_object = Post.get_or_create(
                    id=post_id, link=link, title=title, category=category_object, author=author_object
                )[0]
                KeywordResultItem.get_or_create(KeywordResult=keywordResult_object, post=post_object)

            page_number += 10
        else:
            logging.info('New posts stored successfully!')
            break


# Worker configuration
app.conf.beat_schedule = {
    'everyday-task': {
        'task': 'tasks.crawl_techcrunch',  # Path to your task function
        'schedule': crontab(hour=0, minute=0),  # Run every midnight
    },
}
