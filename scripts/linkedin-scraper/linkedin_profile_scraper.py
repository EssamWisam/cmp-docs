from linkedin_api import Linkedin
from requests.cookies import RequestsCookieJar
from typing import Optional, List, Dict, Union

from utils import load_cookies_from_json, get_linkedin_public_id, get_latest_position

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
            current_position = get_latest_position(profile['experience'])
            # Return formatted current position =>
            # {title}, {company} · {start_month} {start_year} - Present · {total_years} yr {total_months} mos
            experience_string = f"{current_position['title'].strip()}" if current_position['title'] is not None else ""
            experience_string += f", {current_position['company'].strip()} ·" if current_position['company'] is not None else " ·"
            experience_string += f" {current_position['start_month']} {current_position['start_year']} - Present" if current_position['start_month'] is not None and current_position['start_year'] is not None else " - Present"
            experience_string += f" · {current_position["years"]} yr" if current_position["years"] is not None and current_position["years"] != 0 else ""
            experience_string += f" {current_position["months"]} mos" if current_position["months"] is not None and current_position["months"] != 0 else ""
            experience_string = experience_string.strip("· ,")
            return experience_string
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
        # TODO: Use get_profile_skills() from the API instead to access all profile skills.
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
            Optional[Dict[str, Union[str, List[str]]]]: A dictionary of all the student profile details as returned by the LinkedIn API, if available; otherwise, None.
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
            return student_data, profile
        else:
            print("Invalid LinkedIn URL format.")
            return None, None

    def batch_get_all_student_details(self, student_urls: List[str]) -> List[Optional[Dict[str, Union[str, List[str]]]]]:
        """
        Extracts details for multiple student profiles in a batch.

        Args:
            student_urls (List[str]): A list of LinkedIn URLs for student profiles.

        Returns:
            List[Optional[Dict[str, Union[str, List[str]]]]]: A list of dictionaries containing student details.
            List[Optional[Dict[str, Union[str, List[str]]]]]: A list of dictionaries of all the students profile details as returned by the LinkedIn API, if available.
        """
        # Initialize a list to store data for multiple students
        students_data = []
        students_profiles = []
        for student_url in student_urls:
            # Append details for each student profile to the list
            student_data, student_profile = self.get_all_student_details(student_url)
            students_data.append(student_data)
            students_profiles.append(student_profile)
        return students_data, students_profiles

if __name__ == '__main__':
    
    cookies_file = 'cookies.json'
    cookies = load_cookies_from_json(cookies_file)
    
    lps = LinkedProfileScraper(cookies=cookies)
    # students_data = lps.get_all_student_details("https://www.linkedin.com/in/iten-elhak/")
    # print(students_data)
    
    students_data, students_profiles = lps.batch_get_all_student_details([
        "https://www.linkedin.com/in/iten-elhak/",
    ])
    print(students_data)
    
    # import json
    # # Write the dictionary to a JSON file
    # with open("all_data.json", 'w') as f:
    #     json.dump(students_profiles, f, indent=4)  