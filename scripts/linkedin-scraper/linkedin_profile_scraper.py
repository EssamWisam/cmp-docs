import json
from linkedin_api import Linkedin
from requests.cookies import RequestsCookieJar
from typing import Optional, List, Dict, Union

def load_cookies_from_json(filename: str) -> RequestsCookieJar:
    """
    Load cookies from a JSON file into a RequestsCookieJar object suitable for use with requests.

    Args:
        filename (str): The path to the JSON file containing cookies in a specific format.

    Returns:
        RequestsCookieJar: An object containing cookies parsed from the JSON file.
    """
    # Create a RequestsCookieJar object to store cookies
    jar = RequestsCookieJar()

    # Open and load the JSON file containing cookies
    with open(filename, 'r') as f:
        cookie_data = json.load(f)

    # Iterate over each cookie in the data and add it to the jar
    for cookie in cookie_data:
        # Ensure the cookie has required keys before adding it to the jar
        if all(key in cookie for key in ('name', 'value', 'domain', 'path')):
            jar.set(
                name=cookie['name'],
                value=cookie['value'],
                domain=cookie['domain'],
                path=cookie['path']
            )
        else:
            raise ValueError("A Cookie entry is missing required keys: 'name', 'value', 'domain', or 'path'.")

    return jar

def get_linkedin_public_id(url: str) -> Union[str, None]:
    """
    Extracts the public ID from a LinkedIn profile URL.

    Args:
        url (str): The LinkedIn profile URL.

    Returns:
        str: The public ID of the profile, or None if the URL is invalid.
    """
    # Split the URL on '/' to get individual segments
    url_parts = url.split("/")

    # Check if the URL structure is valid (in/username)
    if len(url_parts) >= 5 and url_parts[3] == "in":
        return url_parts[4]
    else:
        return None

class LinkedProfileScraper:
    """
    A class for scraping LinkedIn profile information using an authenticated API session.

    Attributes:
        api: An instance of the Linkedin API for fetching profile data.
    """

    def __init__(self, email: Optional[str] = None, password: Optional[str] = None, cookies: Optional[RequestsCookieJar] = None):
        """
        Initializes the LinkedProfileScraper with authentication credentials or cookies.

        Args:
            email (Optional[str]): The email address for LinkedIn authentication.
            password (Optional[str]): The password for LinkedIn authentication.
            cookies (Optional[RequestsCookieJar]): Cookies for an authenticated LinkedIn session.
        """
        self.api = Linkedin(email, password, cookies=cookies)

    def get_profile_headline(self, profile: Dict[str, Union[str, List[Dict[str, str]]]]) -> Optional[str]:
        """
        Extracts the headline from a LinkedIn profile.

        Args:
            profile (Dict[str, Union[str, List[Dict[str, str]]]]): The LinkedIn profile data.

        Returns:
            Optional[str]: The profile headline, if available; otherwise, None.
        """
        # Extract the headline if it exists in the profile
        return profile['headline'] if 'headline' in profile else None

    def get_profile_picture(self, profile: Dict[str, str]) -> Optional[str]:
        """
        Extracts the profile picture URL from a LinkedIn profile.

        Args:
            profile (Dict[str, str]): The LinkedIn profile data.

        Returns:
            Optional[str]: The complete profile picture URL, if available; otherwise, None.
        """
        # Combine display picture URL and image suffix to create a full image URL
        return profile['displayPictureUrl'] + profile['img_200_200'] if 'displayPictureUrl' in profile and 'img_200_200' in profile else None

    def get_current_position(self, profile: Dict[str, Union[str, List[Dict[str, str]]]]) -> Optional[str]:
        """
        Extracts the current position from a LinkedIn profile.

        Args:
            profile (Dict[str, Union[str, List[Dict[str, str]]]]): The LinkedIn profile data.

        Returns:
            Optional[str]: The current position as "title, companyName", if available; otherwise, None.
        """
        # Check if 'experience' exists and contains entries
        if 'experience' in profile and isinstance(profile['experience'], list) and len(profile['experience']) > 0:
            current_experience = profile['experience'][0]
            # Return formatted current position
            return f"{current_experience['title']}, {current_experience['companyName']}"
        else:
            return None

    def get_top_skills(self, profile: Dict[str, List[Dict[str, str]]]) -> Optional[List[str]]:
        """
        Extracts the top skills from a LinkedIn profile.

        Args:
            profile (Dict[str, List[Dict[str, str]]]): The LinkedIn profile data.

        Returns:
            Optional[List[str]]: A list of top skills (up to 5), if available; otherwise, None.
        """
        # Check if 'skills' exist and extract up to 5 skills
        if 'skills' in profile and len(profile['skills']) >= 4:
            return [skill['name'] for skill in profile['skills'][:5]]
        elif 'skills' in profile:
            return [skill['name'] for skill in profile['skills']]
        else:
            return None

    def get_all_student_details(self, student_url: str) -> Optional[Dict[str, Union[str, List[str]]]]:
        """
        Extracts all relevant details for a single student profile.

        Args:
            student_url (str): The LinkedIn URL of the student's profile.

        Returns:
            Optional[Dict[str, Union[str, List[str]]]]: A dictionary of student details, if available; otherwise, None.
        """
        # Extract the public ID from the LinkedIn URL and fetch the profile
        public_id = get_linkedin_public_id(student_url)
        profile = self.api.get_profile(public_id)
        
        if public_id:
            # Collect relevant profile data
            student_data = {
                'linkedin_url': student_url,
                'image': self.get_profile_picture(profile),
                'title': self.get_profile_headline(profile),
                'top_skills': self.get_top_skills(profile),
                'current_position': self.get_current_position(profile)
            }
            return student_data
        else:
            print("Invalid LinkedIn URL format.")
            return None

    def batch_get_all_student_details(self, student_urls: List[str]) -> List[Optional[Dict[str, Union[str, List[str]]]]]:
        """
        Extracts details for multiple student profiles in a batch.

        Args:
            student_urls (List[str]): A list of LinkedIn URLs for student profiles.

        Returns:
            List[Optional[Dict[str, Union[str, List[str]]]]]: A list of dictionaries containing student details.
        """
        # Initialize a list to store data for multiple students
        students_data = []
        for student_url in student_urls:
            # Append details for each student profile to the list
            student_data = self.get_all_student_details(student_url)
            students_data.append(student_data)
        return students_data

if __name__ == '__main__':
    
    cookies_file = 'cookies.json'
    cookies = load_cookies_from_json(cookies_file)
    
    lps = LinkedProfileScraper(cookies=cookies)
    students_data = lps.batch_get_all_student_details([
        "https://www.linkedin.com/in/iten-elhak/",
    ])
    print(students_data)