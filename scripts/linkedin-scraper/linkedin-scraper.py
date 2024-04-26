import time
import itertools
import os
import yaml
import tqdm

from bs4 import BeautifulSoup
from lxml import html

from selenium import webdriver
from selenium.webdriver.common.by import By

from typing import Optional, List
from dataclasses import dataclass
from pprint import pprint
from argparse import ArgumentParser
from random import randint

if 'LINKEDIN_SCRAPER_EMAIL' not in os.environ:
    print('LINKEDIN_SCRAPER_EMAIL is not set, please set it before running')
    exit(1)

if 'LINKEDIN_SCRAPER_PASSWORD' not in os.environ:
    print('LINKEDIN_SCRAPER_PASSWORD is not set, please set it before running')
    exit(1)

EMAIL = os.environ['LINKEDIN_SCRAPER_EMAIL']
PASSWORD = os.environ['LINKEDIN_SCRAPER_PASSWORD']

@dataclass
class Experience:
    title: str
    company: str
    duration: str

    def __str__(self):
        return f'{self.title}, {self.company}, self.duration'

@dataclass
class ProfileData:
    image_url: str
    title: str
    current_position: Optional[Experience]
    top_skills: Optional[List[str]]

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

def get_section_data_div(tree, section_id):
    """
    Finds all section tags, checks if the first div has an id of 'experience'. If so, returns the div containing the 
    experience data.
    """
    sections = tree.iter("section")
    for section in sections:
        children = section.getchildren()

        for child in children:
            if 'id' in child.attrib and child.attrib['id'] == section_id:
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
    sign_in_button = driver.find_element(By.XPATH, r"""//*[@id="public_profile_contextual-sign-in"]/div/section/div/div/div/div[1]/button""")
    sign_in_button.click()

    username = driver.find_element(By.ID, "public_profile_contextual-sign-in_sign-in-modal_session_key")
    password = driver.find_element(By.ID, "public_profile_contextual-sign-in_sign-in-modal_session_password")

    username.send_keys(EMAIL)
    password.send_keys(PASSWORD)

    driver.find_element(By.XPATH, "/html/body/div[2]/div/div/section/div/div/form/div[2]/button").click()

def scrape_profile(driver, url):
    driver.get(url)
    
    time.sleep(5)
    
    if is_join_page(driver.page_source):
        join_page_log_in(driver)
        time.sleep(5)
        driver.get(url)
    
    profile_page_source = driver.page_source

    # Should be at the profile by now
    tree = html.fromstring(profile_page_source)

    # profile_page_source = None
    # with open('Taher Mohamed _ LinkedIn.html') as f:
    #     profile_page_source = f.read()
    #
    # tree = html.fromstring(profile_page_source)
    
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

    assert(len(images) == 1)
    assert(len(titles) == 1)

    image_url = images[0].attrib['src']
    title = titles[0].text_content().strip()

    current_position = get_current_position(tree)

    top_skills = None
    if about_section is not None:
        top_skills = get_top_skills(about_section[-1])

    return ProfileData(image_url, title, current_position, top_skills)


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument("class_yaml_file")

    args = arg_parser.parse_args()

    class_yaml_file = open(args.class_yaml_file, "r")
    class_yaml = yaml.load(class_yaml_file, Loader=yaml.Loader)
    class_yaml_file.close()

    # Who wrote this yaml file??
    class_students = class_yaml[0]['items'][0]['items']

    options = webdriver.ChromeOptions()
    #options.add_argument("--headless=new")
    options.add_argument(
        '--user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"')
    driver = webdriver.Chrome(options=options)

    MAX_PROFILES_BEFORE_CHROME_RELOAD = 20

    try:
        for i, student in tqdm.tqdm(enumerate(class_students)):
            if (i + 1) % MAX_PROFILES_BEFORE_CHROME_RELOAD == 0:
                driver.close()
                driver = webdriver.Chrome(options=options)

            print(student['name'])

            profile_url = student['linkedin_url']

            if profile_url == 'https://www.linkedin.com/in/':
                time.sleep(randint(1, 5))
                continue

            profile_data = scrape_profile(driver, profile_url)

            student['image'] = profile_data.image_url
            student['title'] = profile_data.title

            if profile_data.top_skills:
                student['top_skills'] = '.'.join(profile_data.top_skills)
            else:
                student['top_skills'] = None

            if profile_data.top_skills:
                student['current_position'] = str(profile_data.current_position)
            else:
                student['current_position'] = None

            time.sleep(randint(1, 5))

        print(yaml.dump(class_students))
        with open('test.yaml', "w") as f:
            f.write(yaml.dump(class_students))
    finally:
        driver.close()
