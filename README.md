# Techcrunch Scraper

## Overview
This Python-based scraper is developed to collect information from the Techcrunch website using appropriate Python tools. The purpose is to allow users to input a keyword and have the scraper retrieve all necessary information about the relation posts and saving it to a database.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contact](#contact)

## Features
- **Keyword Search:** Users can input a keyword of their choice to search in the Techcrunch website.
- **Data Retrieval:** The scraper fetches relevant information about posts from the Techcrunch website.
- **Database Storage:** The retrieved data is stored in a database for easy access.

## Prerequisites
Make sure you have the following installed before running the scraper:
- Python 3.x
- [Required Python Packages]
- Redis server

## Getting Started
1. Clone this repository to your local machine.
   ```bash
   git clone https://github.com/sadeghihasi/crawl-techcrunch
   cd crawl-techcrunch
   ```
2. Install the required Python packages.
   ```bash
   pip install -r requirements.txt
   ```
3. Install Redis server by the following content:
   [https://redis.io/docs/install/install-redis](https://redis.io/docs/install/install-redis)
4. Add python path:
   ```bash
   Windows:
    set PYTHONPATH=C:\path\to\your\project;%PYTHONPATH%
   
   Linux:
    export PYTHONPATH=/path/to/your/project:$PYTHONPATH
   ```
5. Create the tables:
   ```bash
   python db_utilities\create_table.py
   ```
6. Run the scraper script by celery.
   ```bash
   celery -A tasks beat -l info --scheduler celery.beat.PersistentScheduler
   celery -A tasks worker -l info  # In another terminal
   ```
7. Run the scraper script for search.
   ```bash
   python main.py -k [KEYWORD]
   ```

## Usage
1. Execute the scraper script and Enter the desired keyword to search in the website.
2. The scraper will fetch and store the relevant information in the database.

## License
This project is licensed under the [MIT License] - see the [LICENSE.md] file for details.

## Acknowledgments
- Special thanks to the contributors who have helped enhance this scraper.

Feel free to provide feedback, report issues, or contribute to make this techcrunch scraper even better!

<!-- CONTACT -->
## Contact

Hasan Sadeghi - sadeghihasi@gmail.com

Project Link: [https://github.com/sadeghihasi/crawl-techcrunch](https://github.com/sadeghihasi/crawl-techcrunch)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
[github-url]: https://github.com/sadeghihasi
[linkedin-url]: https://linkedin.com/in/sadeghihasi
