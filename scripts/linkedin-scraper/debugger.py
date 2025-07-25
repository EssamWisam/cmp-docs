import yaml
from pathlib import Path
from linkedin_profile_scraper import LinkedProfileScraper
from utils import load_cookies_from_json

# Change this to the path of your YAML file
YAML_PATH = "public/department/Extras/Classes/C2023.yaml"
PROFILE_INDEX = 16  # Change this to the index of the student you want to debug

if __name__ == "__main__":
    file_path = Path(YAML_PATH)
    if not file_path.exists():
        print(f"YAML file does not exist: {YAML_PATH}")
        exit(1)
    with open(YAML_PATH, "r", encoding="utf-8") as f:
        class_yaml = yaml.load(f, Loader=yaml.Loader)
    class_students = class_yaml[0]['items'][0]['items']
    if PROFILE_INDEX >= len(class_students):
        print(f"Profile index {PROFILE_INDEX} out of range. Total students: {len(class_students)}")
        exit(1)
    print(f"Total students in class: {len(class_students)}")
    student = class_students[PROFILE_INDEX]
    print(f"Debugging student: {student['name']}")
    profile_url = student.get('linkedin_url', 'https://www.linkedin.com/in/')
    print(f"LinkedIn URL: {profile_url}")
    cookies_file = './scripts/linkedin-scraper/cookies.json'
    cookies = load_cookies_from_json(cookies_file)
    scraper = LinkedProfileScraper(cookies=cookies)
    try:
        profile_data, raw_profile_data = scraper.get_all_student_details(profile_url)
        print(f"Profile data for {student['name']}:")
        print(profile_data)
        # Save raw profile data to a file
        output_path = f"raw_profile_{PROFILE_INDEX}.json"
        with open(output_path, "w", encoding="utf-8") as out_f:
            import json
            json.dump(raw_profile_data, out_f, indent=4, ensure_ascii=False)
        print(f"Raw profile data saved to {output_path}")
    except Exception as e:
        print(f"Error occurred while scraping: {e}")
