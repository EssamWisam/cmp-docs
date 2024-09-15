import time
import itertools
import os
import yaml
import tqdm
import sys

from bs4 import BeautifulSoup
from lxml import html

from selenium import webdriver
from selenium.webdriver.common.by import By

from typing import Optional, List
from dataclasses import dataclass
from argparse import ArgumentParser
from random import randint
from pathlib import Path

from arabic_mapper import map_en_to_ar_yaml

"""
USAGE:
    LINKEDIN_SCRAPER_EMAIL=<email> LINKEDIN_SCRAPER_PASSWORD=<password> python3 linkedin-scraper.py <path to class yaml>

    or

    export LINKEDIN_SCRAPER_EMAIL=<email>
    export LINKEDIN_SCRAPER_PASSWORD=<password>
    python3 linkedin-scraper.py <path to class yaml>
"""

# TODO: Check for the suspicious activity page (otherwise we crash)
# TODO: Check for the "profile doesn't exist" page (otherwise we crash)

# https://stackoverflow.com/a/14981125
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


if 'LINKEDIN_SCRAPER_EMAIL' not in os.environ:
    eprint('LINKEDIN_SCRAPER_EMAIL is not set, please set it before running')
    exit(1)

if 'LINKEDIN_SCRAPER_PASSWORD' not in os.environ:
    eprint('LINKEDIN_SCRAPER_PASSWORD is not set, please set it before running')
    exit(1)

EMAIL = os.environ['LINKEDIN_SCRAPER_EMAIL']
PASSWORD = os.environ['LINKEDIN_SCRAPER_PASSWORD']

@dataclass
class Experience:
    title: str
    company: str
    duration: str

    def __str__(self):
        return f'{self.title}, {self.company}, {self.duration}'

@dataclass
class ProfileData:
    image_url: str
    title: str
    current_position: Optional[Experience]
    top_skills: Optional[List[str]]


class RetryFailed(Exception):
    pass

# https://stackoverflow.com/a/64030200
def retry(times, exceptions):
    """
    Retry Decorator
    Retries the wrapped function/method `times` times if the exceptions listed
    in ``exceptions`` are thrown
    :param times: The number of times to repeat the wrapped function/method
    :type times: Int
    :param Exceptions: Lists of exceptions that trigger a retry attempt
    :type Exceptions: Tuple of Exceptions
    """
    def decorator(func):
        def newfn(*args, **kwargs):
            attempt = 0
            while attempt < times:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    eprint(f'Calling {func} with args ({args}), kwargs ({kwargs}) failed with exception: {type(e).__name__}:{e}')
                    attempt += 1

            eprint(f'Failed to run {func}, for {times} attempts')
            raise RetryFailed
        return newfn
    return decorator

def is_join_page(html):
    # TODO: Use lxml so we don't need beautiful soup 
    bs = BeautifulSoup(html, "html.parser")
    h1_tags = bs.find_all("h1")

    return any(tag.text == "Join LinkedIn" for tag in h1_tags)

def sign_in_modal_open(root):
    modal_node = root.xpath("""//*[@id="public_profile_contextual-sign-in"]""")
    return modal_node is not None and len(modal_node) > 0 and len(modal_node[0].getchildren()) > 0

def parse_single_position(experience_li):
    company_xpath = "div/div[2]/div[1]/div[1]/span[1]/span[1]/text()"
    duration_xpath = "div/div[2]/div[1]/div[1]/span[2]/span[1]/text()"
    title_xpath = "div/div[2]/div[1]/div[1]/div/div/div/div/span[1]/text()"

    return [Experience(
        experience_li.xpath(title_xpath)[0],
        experience_li.xpath(company_xpath)[0],
        experience_li.xpath(duration_xpath)[0],
    )]        

def parse_multiple_positions(experience_li, multi_position_company_xpath):
    company_name = experience_li.xpath(f"{multi_position_company_xpath}/text()")[0]
    inner_positions_xpath = "div/div[2]/div[2]/ul"
    positions_ul = experience_li.xpath(inner_positions_xpath)[0]

    def parse_multi_position_entry(position_li, company_name):
        def employment_type_exists(position_li):
            # Some profiles can have the position listed as (title, employment type (full, part, etc..), duration)
            # Others have it as only (title, duration)
            # This little hack ASSUMES that the employment type is optional, but the duration is not.
            # So if two span elements exist, both must exist. If one span element exists, then it's the duration
            position_children = position_li.xpath("div/div[2]/div[1]/a")[0]
            count_span = sum(1 for html_element in position_children if html_element.tag == 'span')
            return count_span >= 2

        def get_position_duration(position_li):
            if employment_type_exists(position_li):
                return position_li.xpath("div/div[2]/div[1]/a/span[2]/span[2]/text()")[0]
            else:
                return position_li.xpath("div/div[2]/div[1]/a/span[1]/span[1]/text()")[0]

        position_title = position_li.xpath("div/div[2]/div[1]/a/div/div/div/div/span[1]/text()")[0]
        position_duration = get_position_duration(position_li)

        return Experience(position_title, company_name, position_duration)

    return [parse_multi_position_entry(position_li, company_name) for position_li in positions_ul]

def flatten(nested_list):
    return list(itertools.chain(*nested_list))

def has_data_div(node, section_id):
    if type(node) is not str and hasattr(node, 'attrib') and 'id' in node.attrib:
        # print(node.tag, node.attrib)

        if node.attrib['id'] == section_id:
            return True
        else:
            return False
    else:
        return any(has_data_div(child, section_id) for child in node.getchildren())

def get_section_data_div(tree, section_id):
    """
    Finds all section tags, checks if the first div has an id of 'experience'. If so, returns the div containing the 
    experience data.
    """
    sections = tree.iter("section")
    for section in sections:
        for child in section.getchildren():
            if has_data_div(child, section_id):
                return section

    return None

def get_current_position(tree) -> Optional[Experience]:
    """
    Given the root HTML node, figures out which section tag contains the experience info and parses each position.
    """

    def parse_experience_entry(experience_li) -> List[Experience]:
        """
        Given on entry (li) from the experience list, figures out whether it's a single position or multiple positions 
        under one company. Returns a list of parsed positions.
        """

        multi_position_company_xpath = 'div/div[2]/div[1]/a/div/div/div/div/span[1]'

        def has_multiple_positions(experience_li):
            """
            By examining the HTML of a single experience element (li inside ul), if the entry has multiple positions 
            under one company, the company's name comes first at the specified XPath
            """
            return experience_li.find(multi_position_company_xpath) is not None

        multiple_positions = has_multiple_positions(experience_li)

        if not multiple_positions:
            return parse_single_position(experience_li)
        else:
            return parse_multiple_positions(experience_li, multi_position_company_xpath)

    exp_div = get_section_data_div(tree, 'experience')
    if exp_div is not None:
        exp_div = exp_div[-2]
    else:
        return None

    experience_ul = exp_div.getchildren()[1]
    experiences = flatten([parse_experience_entry(experience_li) for experience_li in experience_ul])
    current_positions = [e for e in experiences if "Present" in e.duration]

    if len(current_positions) == 0:
        return None
    else:
        return current_positions[0]

def get_top_skills(about_div):
    top_skills = about_div.xpath("""div/ul/li/div/div/div[2]/div/div[1]/div[2]/div/div/span[1]""")

    if len(top_skills) == 0:
        return None

    return top_skills[0].text_content().split(' • ')

def join_page_log_in(driver):
    sign_in_button = driver.find_element(By.XPATH, r"""//*[@id="main-content"]/div/form/p/button""")
    sign_in_button.click()

    username = driver.find_element(By.ID, "session_key")
    password = driver.find_element(By.ID, "session_password")

    username.send_keys(EMAIL)
    password.send_keys(PASSWORD)

    driver.find_element(By.XPATH, "/html/body/div/main/div/div/form/div[2]/button").click()

def sign_in_modal_log_in(driver):
    sign_in_button = driver.find_element(
        By.XPATH, r"""//*[@id="public_profile_contextual-sign-in"]/div/section/div/div/div/div[1]/button""")
    sign_in_button.click()

    username = driver.find_element(By.ID, "public_profile_contextual-sign-in_sign-in-modal_session_key")
    password = driver.find_element(By.ID, "public_profile_contextual-sign-in_sign-in-modal_session_password")

    username.send_keys(EMAIL)
    password.send_keys(PASSWORD)

    driver.find_element(By.XPATH, "/html/body/div[2]/div/div/section/div/div/form/div[2]/button").click()

class NoProfileImageException(Exception):
    pass

class NoTitleException(Exception):
    pass

@retry(3, exceptions=(NoProfileImageException, NoTitleException, Exception))
def scrape_profile(driver, url):
    driver.get(url)

    time.sleep(10)
    time.sleep(randint(5, 10))

    if is_join_page(driver.page_source):
        join_page_log_in(driver)
        time.sleep(randint(5, 10))
        driver.get(url)
        time.sleep(randint(5, 10))

    profile_page_source = driver.page_source

    # Should be at the profile by now
    tree = html.fromstring(profile_page_source)

    if sign_in_modal_open(tree):
        sign_in_modal_log_in(driver)
        profile_page_source = driver.page_source
        tree = html.fromstring(profile_page_source)

    profile_image_xpath = \
        "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[1]/div[1]/div/button/img"
    title_xpath = \
        "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[2]"

    # .xpath returns a list, but since we're using the XPATH corresponding to the profile image 
    # (no other things share it) we're guaranteed to have one element only.
    images = tree.xpath(profile_image_xpath)
    titles = tree.xpath(title_xpath)
    about_section = get_section_data_div(tree, 'about')

    if len(images) != 1:
        raise NoProfileImageException

    if len(titles) != 1:
        raise NoTitleException

    image_url = images[0].attrib['src']
    title = titles[0].text_content().strip()

    current_position = get_current_position(tree)

    top_skills = None
    if about_section is not None:
        top_skills = get_top_skills(about_section[-1])

    return ProfileData(image_url, title, current_position, top_skills)


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument("class_yaml_file", help="Path to the YAML file (mandatory)")
    arg_parser.add_argument("--start-no", help="Optional starting number", type=int, default=1)

    args = arg_parser.parse_args()

    class_yaml_file = open(args.class_yaml_file, "r", encoding="utf-8")
    class_yaml = yaml.load(class_yaml_file, Loader=yaml.Loader)
    class_yaml_file.close()

    start_no = args.start_no
    # Who wrote this yaml file??
    class_students = class_yaml[0]['items'][0]['items']
    new_class_students = class_students

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new") # Comment this line if you want to see the script in action with UI.
    driver = webdriver.Chrome(options=options)

    MAX_PROFILES_BEFORE_CHROME_RELOAD = 100

    try:
        for i, student in enumerate(class_students):

            if start_no is not None and i < start_no-1:
                continue

            # Need to restart chrome every so often since it seems to leak memory.
            # Otherwise, we'd run out of memory.
            if (i + 1) % MAX_PROFILES_BEFORE_CHROME_RELOAD == 0:
                driver.close()
                driver = webdriver.Chrome(options=options)

            profile_url = student['linkedin_url'] if 'linkedin_url' in student.keys() else 'https://www.linkedin.com/in/'

            # Skip invalid profile URLs
            # We sleep a random amount of time as a precaution so Linkedin doesn't detect our bot
            if profile_url == 'https://www.linkedin.com/in/' or profile_url is None:
                eprint(f"Skipping: {student['name']} due to invalid URL ({profile_url})")
                new_class_students[i]['linkedin_url'] = 'https://www.linkedin.com/in/'
                new_class_students[i]['title'] = None
                new_class_students[i]['image'] = None
                new_class_students[i]['top_skills'] = None
                new_class_students[i]['current_position'] = None
                new_class_students[i]['markdown'] = student['markdown'] if 'markdown' in student.keys() else None
                # time.sleep(randint(1, 5))
                continue

            try:
                profile_data = scrape_profile(driver, profile_url)
            except RetryFailed:
                eprint(f"Failed to scrape profile URL ({profile_url}), skipping")
                continue

            new_class_students[i]['title'] = profile_data.title

            if profile_data.image_url is not None and profile_data.image_url != "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7":
                new_class_students[i]['image'] = profile_data.image_url
            else:
                new_class_students[i]['image'] = None

            if profile_data.top_skills:
                new_class_students[i]['top_skills'] = ', '.join(profile_data.top_skills)
            else:
                new_class_students[i]['top_skills'] = None

            if profile_data.current_position:
                new_class_students[i]['current_position'] = str(profile_data.current_position)
            else:
                new_class_students[i]['current_position'] = None

            if 'markdown' not in student.keys():
                new_class_students[i]['markdown'] = None

            time.sleep(randint(5, 10))

        class_yaml[0]['items'][0]['items'] = new_class_students
        with open(args.class_yaml_file, "w", encoding="utf-8") as f:
            f.write(yaml.dump(class_yaml, sort_keys=False, allow_unicode=True))

    finally:
        driver.close()

    file_path = Path(args.class_yaml_file)

    if not file_path.exists():
        print("The YAML file does not exist!")
        exit()

    ar_yaml_path = args.class_yaml_file.replace(".yaml", "_ar.yaml")
    arabic_file_path = Path(ar_yaml_path)

    if not arabic_file_path.exists():
        print("The Arabic YAML file does not exist! Should have the same path as English yaml and same name but ending with _ar.yaml instead!")
        exit()

    class_yaml_file = open(args.class_yaml_file, "r", encoding="utf-8")
    class_yaml = yaml.load(class_yaml_file, Loader=yaml.Loader)
    class_yaml_file.close()

    ar_class_yaml_file = open(ar_yaml_path, "r", encoding="utf-8")
    ar_class_yaml = yaml.load(ar_class_yaml_file, Loader=yaml.Loader)
    ar_class_yaml_file.close()

    new_ar_class_yaml = map_en_to_ar_yaml(class_yaml,ar_class_yaml)

    with open(ar_yaml_path, "w", encoding="utf-8") as f:
        f.write(yaml.dump(new_ar_class_yaml, sort_keys=False, allow_unicode=True))
        print("Arabic YAML mapped successfully!")