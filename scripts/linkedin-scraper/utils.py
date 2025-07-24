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
    Returns the latest/current position info for a LinkedIn profile, handling missing data and summing durations at the same company.
    """
    if not positions or not isinstance(positions, list):
        return None

    current_position = positions[0]
    # Defensive: Check for required keys
    time_period = current_position.get('timePeriod')
    if not time_period or 'startDate' not in time_period:
        return {
            "title": current_position.get('title'),
            "company": current_position.get('companyName'),
            "years": None,
            "months": None,
            "start_year": None,
            "start_month": None,
        }
    # If current position has an end date, it's not current
    if 'endDate' in time_period:
        return None

    current_company_urn = current_position.get('companyUrn')
    current_company_name = current_position.get('companyName')
    current_title = current_position.get('title')
    earliest_start_year = time_period['startDate'].get('year')
    earliest_start_month = time_period['startDate'].get('month')
    total_duration = calculate_duration(time_period)

    # Sum durations for all positions at the same company
    for position in positions[1:]:
        if position.get('companyUrn') == current_company_urn:
            pos_time_period = position.get('timePeriod')
            if not pos_time_period or 'startDate' not in pos_time_period:
                continue
            start_year = pos_time_period['startDate'].get('year')
            start_month = pos_time_period['startDate'].get('month')
            if start_year is not None and start_month is not None:
                if (start_year < earliest_start_year) or (start_year == earliest_start_year and start_month < earliest_start_month):
                    earliest_start_year = start_year
                    earliest_start_month = start_month
            pos_duration = calculate_duration(pos_time_period)
            total_duration['years'] += pos_duration['years']
            total_duration['months'] += pos_duration['months']
    # Normalize months
    if total_duration['months'] >= 12:
        total_duration['years'] += total_duration['months'] // 12
        total_duration['months'] %= 12

    # Format start month
    start_month_str = MONTHS[earliest_start_month - 1] if earliest_start_month and 1 <= earliest_start_month <= 12 else None

    return {
        "title": current_title,
        "company": current_company_name,
        "years": total_duration['years'],
        "months": total_duration['months'],
        "start_year": earliest_start_year,
        "start_month": start_month_str
    }
