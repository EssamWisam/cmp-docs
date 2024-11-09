import json
from datetime import datetime
from requests.cookies import RequestsCookieJar
from typing import Optional, List, Dict, Union

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

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

def calculate_duration(time_period: Dict[str, Dict[str, int]]) -> Dict[str, int]:
    """
    Calculate the duration in years and months between startDate and endDate.
    If the endDate is not provided, the current date is used.

    Args:
        time_period (Dict[str, Dict[str, int]]): A dictionary containing the start and optional end dates.

    Returns:
        Dict[str, int]: A dictionary with the total number of years and months.
    """
    start_year = time_period['startDate']['year']
    start_month = time_period['startDate']['month']
    
    # Use the current date if endDate is not provided
    if 'endDate' in time_period:
        end_year = time_period['endDate']['year']
        end_month = time_period['endDate']['month']
    else:
        current_date = datetime.now()
        end_year = current_date.year
        end_month = current_date.month

    # Calculate total months difference
    total_months = (end_year - start_year) * 12 + (end_month - start_month) + 1 # This 1 is always added by LinkedIn

    # Convert months to years and months
    years = total_months // 12
    months = total_months % 12

    return {
        "years": years,
        "months": months
    }

def get_latest_position(positions: List[Dict]) -> Optional[Dict[str, Union[str, int]]]:
    """
    Calculates the total duration an employee worked at their current company across different positions.
    Also returns the start month and year of the employee's tenure at the company.

    Args:
        positions (List[Dict]): A list of dictionaries representing positions with start and end dates, title, company name, and company URN.

    Returns:
        Optional[Dict[str, Union[str, int]]]: A dictionary containing the title of the current position, company name, total years, months,
        and the start year and month.
        Returns None if the current position has an end date.
    """
    if not positions:
        return None

    # The current position should be the first element in the list
    current_position = positions[0]

    # Check if the current position has an end date (which it shouldn't)
    if 'endDate' in current_position['timePeriod']:
        return None

    # Get the URN and title of the current position
    current_company_urn = current_position['companyUrn']
    current_company_name = current_position['companyName'] if "companyName" in current_position else None
    current_title = current_position['title']
    earliest_start_year = current_position['timePeriod']['startDate']['year']
    earliest_start_month = current_position['timePeriod']['startDate']['month']

    # Calculate the duration of the current position using the current date as the end date
    total_duration = calculate_duration(current_position['timePeriod'])

    # Iterate over the rest of the positions to sum up the duration if the company URN matches
    for position in positions[1:]:
        if position['companyUrn'] == current_company_urn:
            # Check if this position started earlier than the current earliest start date
            start_year = position['timePeriod']['startDate']['year']
            start_month = position['timePeriod']['startDate']['month']

            if (start_year < earliest_start_year) or (start_year == earliest_start_year and start_month < earliest_start_month):
                earliest_start_year = start_year
                earliest_start_month = start_month
            
            # Add the duration of this position to the total duration
            position_duration = calculate_duration(position['timePeriod'])
            total_duration['years'] += position_duration['years']
            total_duration['months'] += position_duration['months']

            # Normalize the months to convert them into years if needed
            if total_duration['months'] >= 12:
                total_duration['years'] += total_duration['months'] // 12
                total_duration['months'] %= 12

    return {
        "title": current_title,
        "company": current_company_name,
        "years": total_duration['years'],
        "months": total_duration['months'],
        "start_year": earliest_start_year,
        "start_month": MONTHS[earliest_start_month - 1]  # Convert month number to abbreviated month name
    }
