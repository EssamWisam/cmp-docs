import os

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


# Loop through files in the directory
for filename in os.listdir(target_dir):
  if not is_ignored(filename):
    # Construct full path
    full_path = os.path.join(target_dir, filename)
    print(full_path)
    # Call the command with relative path
    command = f"python ./scripts/linkedin-scraper/linkedin-scraper.py {full_path}"
    os.system(command)

print("Finished processing files.")
