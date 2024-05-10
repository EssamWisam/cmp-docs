import re
import yaml
from pathlib import Path
from argparse import ArgumentParser

def map_en_to_ar_yaml(en_yaml, ar_yaml):

    class_students = en_yaml[0]['items'][0]['items']
    ar_class_students = ar_yaml[0]['items'][0]['items']

    # This assumes that the number and order of the students is the same in both the Arabic and English versions.
    for i, student in enumerate(class_students):
        ar_class_students[i]["image"] = student["image"]
        ar_class_students[i]["linkedin_url"] = student["linkedin_url"] if "linkedin_url" in student.keys() else "https://www.linkedin.com/in/"
        ar_class_students[i]["title"] = student["title"] if "title" in student.keys() else None
        ar_class_students[i]["top_skills"] = student["top_skills"] if "top_skills" in student.keys() else None
        ar_class_students[i]["current_position"] = student["current_position"] if "current_position" in student.keys() else None
        if "[LinkedIn]" in ar_class_students[i]["markdown"] and "[LinkedIn]()" not in ar_class_students[i]["markdown"]:
            pattern = r"\[LinkedIn\]\([^)]+\)"
            ar_class_students[i]["markdown"] = re.sub(pattern, "[LinkedIn]()", ar_class_students[i]["markdown"])

    ar_yaml[0]['items'][0]['items'] = ar_class_students

    return ar_yaml

if __name__ == '__main__':

    arg_parser = ArgumentParser()
    arg_parser.add_argument("class_yaml_file")

    args = arg_parser.parse_args()

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