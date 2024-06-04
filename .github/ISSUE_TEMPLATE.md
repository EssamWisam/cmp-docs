---
title: ⏰ Reminder to Run LinkedIn Scraper
---
It's been two weeks.

It's time to run the LinkedIn script to get the latest titles and current positions of CMP students and graduates.

To run the script follow the steps below and if it's not your first time running the scipt, you can just start from step 4:

### Steps for running the LinkedIn script:
1. Make sure you have Python 3 downloaded on your device. You can check by running the command in your bash terminal and it should display the Python version if it is already installed.
    ```bash
    python --version
    ```
2. Install all the needed Python packages using the `requirements.txt` present in the `scripts/linkedin-scraper` directory.
    ```bash
    pip install -r "scripts/linkedin-scraper/requirements.txt"
    ```
3. Download the Chrome Driver that is compatible with your OS and Chrome Version from this [link](https://getwebdriver.com/chromedriver). It should be a zip file of about 10 MBs or less. Extract it using [WinRAR](https://www.win-rar.com/download.html?&L=0) or a similar archive manager. Then copy the `chromedriver.exe` file to the `scripts/linkedin-scraper` directory.
4. Set the enivronment variables with valid LinkedIn credentials in the bash terminal as following:
    ```bash
    export LINKEDIN_SCRAPER_EMAIL=<email>
    export LINKEDIN_SCRAPER_PASSWORD=<password>
    ```
    and replace `<email>` and `<password>` with the actual LinkedIn credentials. Note, you should probably avoid using your main LinkedIn account credentials to avoid running the risk of it being banned by LinkedIn after multiple scraping.
5. Finally, you can run the script on all the class yaml files using the command below:
    ```bash
    python "scripts/linkedin-scraper/run.py" 
    ```
    and if you want to run the script for a certain class only, use the command below and replace `20XX` with the graduation year of said class:
    ```bash
    python "scripts/linkedin-scraper/linkedin-scraper.py" "public/department/Extras/Classes/C20XX.yaml"
    ```

#### Last Notes:
* If the script doesn't manage to scrap any data, make sure you have the `<email>` and `<password>` written correctly in the environment variables.
* Make sure that you have a _fast and stable internet_ connection while running the script since it will affect the results of the scraping.
* After running the script and updating the yaml files, please create a PR, and assign this issue to it so that it can be closed later on and not forgotten.