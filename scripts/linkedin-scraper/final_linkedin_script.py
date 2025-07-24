import os
import json
import time
import yaml
from pathlib import Path
from random import randint
from argparse import ArgumentParser

from utils import load_cookies_from_json
from linkedin_profile_scraper import LinkedProfileScraper
from arabic_mapper import map_en_to_ar_yaml
import copy

def get_class_data(class_yaml_file_path: str, scraper: LinkedProfileScraper, start_no: int = None, end_no: int = None):
    file_path = Path(class_yaml_file_path)

    if not file_path.exists():
        print("The YAML file does not exist!")
        exit()
    
    class_yaml_file = open(class_yaml_file_path, "r", encoding="utf-8")
    class_yaml = yaml.load(class_yaml_file, Loader=yaml.Loader)
    class_yaml_file.close()

    class_students = class_yaml[0]['items'][0]['items']
    new_class_students = copy.deepcopy(class_students)
    
    profiles_data = []
    raw_profiles_data = []

    for i, student in enumerate(class_students):
        if start_no is not None and i < start_no-1:
            continue
        
        if end_no is not None and i > end_no:
            break

        profile_url = student.get('linkedin_url', 'https://www.linkedin.com/in/')

        # Skip invalid profile URLs
        if profile_url == 'https://www.linkedin.com/in/' or profile_url is None:
            print(f"Skipping: {student['name']} due to invalid URL ({profile_url})")
            new_class_students[i]['linkedin_url'] = 'https://www.linkedin.com/in/'
            new_class_students[i]['title'] = None
            new_class_students[i]['image'] = None
            new_class_students[i]['top_skills'] = None
            new_class_students[i]['current_position'] = None
            new_class_students[i]['markdown'] = student.get('markdown', None)
            profiles_data.append(None)
            raw_profiles_data.append(None)
            continue

        try:
            profile_data, raw_profile_data = scraper.get_all_student_details(profile_url)
            if profile_data is None:
                raise ValueError("Profile data is None (profile inaccessible or not found)")
            profiles_data.append(profile_data)
            raw_profiles_data.append(raw_profile_data)

            new_class_students[i]['title'] = profile_data.get('title', None)
            new_class_students[i]['image'] = profile_data.get('image', None)
            top_skills = profile_data.get('top_skills', None)
            if top_skills and isinstance(top_skills, list) and len(top_skills) > 0:
                new_class_students[i]['top_skills'] = ', '.join(top_skills)
            else:
                new_class_students[i]['top_skills'] = None
            current_position = profile_data.get('current_position', None)
            if current_position:
                new_class_students[i]['current_position'] = str(current_position)
            else:
                new_class_students[i]['current_position'] = None
            if 'markdown' not in student:
                new_class_students[i]['markdown'] = None
        except Exception as e:
            error_type = type(e).__name__
            error_msg = str(e)
            if error_type == 'KeyError':
                print(f"KeyError: Missing key '{error_msg}' for {student['name']}. This usually means the LinkedIn profile is missing expected data.")
            elif error_type == 'TypeError' and "'NoneType' object is not subscriptable" in error_msg:
                print(f"TypeError: Tried to access data from a None object for {student['name']}. This means the profile could not be scraped or is private/inaccessible.")
            elif error_type == 'ValueError' and "Profile data is None" in error_msg:
                print(f"ValueError: Profile data is None for {student['name']}. This means the LinkedIn profile could not be accessed or does not exist.")
            else:
                print(f"An unexpected error occurred ({error_type}: {error_msg}) for {student['name']}. Please check the LinkedIn URL or scraping logic.")
            profiles_data.append(None)
            raw_profiles_data.append(None)
            new_class_students[i]['title'] = None
            new_class_students[i]['image'] = None
            new_class_students[i]['top_skills'] = None
            new_class_students[i]['current_position'] = None
            if 'markdown' not in student:
                new_class_students[i]['markdown'] = None
        time.sleep(randint(1, 10))

    class_yaml[0]['items'][0]['items'] = new_class_students
    
    with open(class_yaml_file_path, "w", encoding="utf-8") as f:
        f.write(yaml.dump(class_yaml, sort_keys=False, allow_unicode=True))

    ar_yaml_path = class_yaml_file_path.replace(".yaml", "_ar.yaml")
    arabic_file_path = Path(ar_yaml_path)

    if not arabic_file_path.exists():
        print("The Arabic YAML file does not exist! Should have the same path as English yaml and same name but ending with _ar.yaml instead!")
        exit()

    ar_class_yaml_file = open(ar_yaml_path, "r", encoding="utf-8")
    ar_class_yaml = yaml.load(ar_class_yaml_file, Loader=yaml.Loader)
    ar_class_yaml_file.close()

    new_ar_class_yaml = map_en_to_ar_yaml(class_yaml, ar_class_yaml)

    with open(ar_yaml_path, "w", encoding="utf-8") as f:
        f.write(yaml.dump(new_ar_class_yaml, sort_keys=False, allow_unicode=True))
        print("Arabic YAML mapped successfully!")
        
    return profiles_data, raw_profiles_data
        
if __name__ == '__main__':
    
    arg_parser = ArgumentParser()
    arg_parser.add_argument("class_yaml_file", help="Path to the YAML file (mandatory)")
    arg_parser.add_argument("--start-no", help="Optional starting index", type=int, default=None)
    arg_parser.add_argument("--end-no", help="Optional stopping index", type=int, default=None)

    args = arg_parser.parse_args()
    yaml_file_path = args.class_yaml_file
    start_no = args.start_no
    end_no = args.end_no
         
    cookies_file = './scripts/linkedin-scraper/cookies.json'
    cookies = load_cookies_from_json(cookies_file)
    
    lps = LinkedProfileScraper(cookies=cookies)
    profiles_data, raw_profiles_data = get_class_data(yaml_file_path, lps, start_no=start_no, end_no=end_no)

    # Get the file name from the full path
    file_name_with_path = os.path.basename(yaml_file_path)

    # Split the file name and extension
    name, _ = os.path.splitext(file_name_with_path)

    # Write the dictionary to a JSON file
    with open(f"./scripts/linkedin-scraper/data/{name}_summary.json", 'w') as f:
        json.dump(profiles_data, f, indent=4)  
        
    # Write the dictionary to a JSON file
    with open(f"./scripts/linkedin-scraper/data/{name}_raw.json", 'w') as f:
        json.dump(raw_profiles_data, f, indent=4)
