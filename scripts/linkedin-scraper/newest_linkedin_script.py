import json
import time
import yaml
from pathlib import Path
from random import randint

from utils import load_cookies_from_json
from linkedin_profile_scraper import LinkedProfileScraper
from arabic_mapper import map_en_to_ar_yaml

def get_class_data(class_yaml_file_path: str, scraper: LinkedProfileScraper, start_no: int = None, end_no: int = None):
    
    file_path = Path(class_yaml_file_path)

    if not file_path.exists():
        print("The YAML file does not exist!")
        exit()
    
    class_yaml_file = open(class_yaml_file_path, "r", encoding="utf-8")
    class_yaml = yaml.load(class_yaml_file, Loader=yaml.Loader)
    class_yaml_file.close()

    class_students = class_yaml[0]['items'][0]['items']
    new_class_students = class_students
    
    profiles_data = []
    raw_profiles_data = []

    for i, student in enumerate(class_students):

        if start_no is not None and i < start_no-1:
            continue
        
        if end_no is not None and i > end_no:
            break

        profile_url = student['linkedin_url'] if 'linkedin_url' in student.keys() else 'https://www.linkedin.com/in/'

        # Skip invalid profile URLs
        if profile_url == 'https://www.linkedin.com/in/' or profile_url is None:
            print(f"Skipping: {student['name']} due to invalid URL ({profile_url})")
            new_class_students[i]['linkedin_url'] = 'https://www.linkedin.com/in/'
            new_class_students[i]['title'] = None
            new_class_students[i]['image'] = None
            new_class_students[i]['top_skills'] = None
            new_class_students[i]['current_position'] = None
            new_class_students[i]['markdown'] = student['markdown'] if 'markdown' in student.keys() else None
            profiles_data.append(None)
            raw_profiles_data.append(None)
            continue

        try:
            profile_data, raw_profile_data = scraper.get_all_student_details(profile_url)
            profiles_data.append(profile_data)
            raw_profiles_data.append(raw_profile_data)
        except Exception as e:
            profiles_data.append(None)
            raw_profiles_data.append(None)
            print(f"An error occurred: {e}")

        new_class_students[i]['title'] = profile_data['title'] if 'title' in profile_data else None

        if 'image' in profile_data and profile_data['image'] is not None:
            new_class_students[i]['image'] = profile_data['image']
        else:
            new_class_students[i]['image'] = None

        if 'top_skills' in profile_data and profile_data['top_skills'] is not None and len(profile_data['top_skills']) > 0:
            new_class_students[i]['top_skills'] = ', '.join(profile_data['top_skills'])
        else:
            new_class_students[i]['top_skills'] = None

        if "current_position" in profile_data and profile_data["current_position"] is not None:
            new_class_students[i]['current_position'] = str(profile_data["current_position"])
        else:
            new_class_students[i]['current_position'] = None

        if 'markdown' not in student.keys():
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

    new_ar_class_yaml = map_en_to_ar_yaml(class_yaml,ar_class_yaml)

    with open(ar_yaml_path, "w", encoding="utf-8") as f:
        f.write(yaml.dump(new_ar_class_yaml, sort_keys=False, allow_unicode=True))
        print("Arabic YAML mapped successfully!")
        
    return profiles_data, raw_profiles_data
        
if __name__ == '__main__':
    
    cookies_file = './scripts/linkedin-scraper/cookies.json'
    cookies = load_cookies_from_json(cookies_file)
    
    lps = LinkedProfileScraper(cookies=cookies)
    profiles_data, raw_profiles_data = get_class_data("./public/department/Extras/Classes/C2023.yaml", lps)

    # Write the dictionary to a JSON file
    with open("./scripts/linkedin-scraper/data/C2023_summary.json", 'w') as f:
        json.dump(profiles_data, f, indent=4)  
        
    # Write the dictionary to a JSON file
    with open("./scripts/linkedin-scraper/data/C2023_raw.json", 'w') as f:
        json.dump(raw_profiles_data, f, indent=4)