import os
import json
from linkedin_profile_scraper import LinkedProfileScraper
from newest_linkedin_script import load_cookies_from_json, get_class_data

# Define the target directory
target_dir = "./public/department/Extras/Classes"

# List of extensions and words to ignore
ignored_extensions = ["_ar.yaml"]
ignored_word = "XX" 


def is_ignored(filename):
	"""Checks if the filename should be ignored based on extension or word."""
	for ext in ignored_extensions:
		if filename.endswith(ext):
			return True
	return ignored_word.lower() in filename.lower()

if __name__ == '__main__':
	# Loop through files in the directory
	cookies_file = './scripts/linkedin-scraper/cookies.json'
	cookies = load_cookies_from_json(cookies_file)

	lps = LinkedProfileScraper(cookies=cookies)
  
	for filename in os.listdir(target_dir):
		if not is_ignored(filename):

			name, _ = os.path.splitext(filename)
			# Construct full path
			full_path = os.path.join(target_dir, filename)
			
			profiles_data, raw_profiles_data = get_class_data(full_path, lps)

			# Write the dictionary to a JSON file
			with open(f"./scripts/linkedin-scraper/data/{name}_summary.json", 'w') as f:
				json.dump(profiles_data, f, indent=4)  
				
			# Write the dictionary to a JSON file
			with open(f"./scripts/linkedin-scraper/data/{name}_raw.json", 'w') as f:
				json.dump(raw_profiles_data, f, indent=4)

	print("Finished processing files.")
