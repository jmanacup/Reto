import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def main():

    place = input("What occupation you wanted to search? : ")
    location = input("What location you want the job to be at? : ")
    pages = input(
        "How many pages would you want? (1 page is roughly ~13 entries) : ")
    filename = input("Name of the .xlsx file to be saved : ")
    get_listing(place, location, filename, int(pages))


def get_listing(job_title, location, filename, pages=1):

    url = "https://www.indeed.com/"

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

    options = webdriver.ChromeOptions()
    options.headless = True

    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # options.add_argument('--log-level=3')
    options.add_argument('user-agent={0}'.format(user_agent))

    # start the driver
    driver = webdriver.Chrome(options=options)

    # go to the url
    driver.get(url)
    time.sleep(2)

    # input the job title
    driver.find_element("xpath",
                        '//*[@id="text-input-what"]').send_keys(job_title)
    time.sleep(2)

    # input the location; we need to clear out the inputs first
    driver.find_element(
        "xpath", '//*[@id="text-input-where"]').send_keys(Keys.CONTROL + 'a')
    time.sleep(1)

    driver.find_element(
        "xpath", '//*[@id="text-input-where"]').send_keys(location)

    driver.find_element(
        "xpath", '//*[@id="jobsearch"]/button').send_keys(Keys.ENTER)

    time.sleep(2)

    df = pd.DataFrame(columns=['Job Title', 'Company', 'Location', 'Link'])

    for i in range(pages):

        job_listings = driver.find_elements(By.CLASS_NAME, "job_seen_beacon")

        for job in job_listings:

            job_title = job.find_element(By.CLASS_NAME, "jobTitle").text
            company_name = job.find_element(By.CLASS_NAME, "companyName").text

            # removes newline as well as comments
            location = job.find_element(By.CLASS_NAME, "companyLocation").text.replace(
                '\n', " ").split('+', 1)[0]

            link = url + "viewjob?jk=" + \
                job.find_element(By.TAG_NAME, "a").get_attribute("data-jk")
            link = '=HYPERLINK("' + link + '","' + link + '")'

            df.loc[len(df.index)] = [job_title, company_name, location, link]

        driver.find_element(
            "xpath", "//*[@data-testid=\"pagination-page-next\"]").click()

        time.sleep(2)

    writer = pd.ExcelWriter(filename + ".xlsx", engine='xlsxwriter')
    # loop through `dict` of dataframes
    df.to_excel(writer, sheet_name="jobs",
                index=False)  # send df to writer
    worksheet = writer.sheets["jobs"]  # pull worksheet object
    for idx, col in enumerate(df):  # loop through all columns
        series = df[col]
        max_len = max((
            series.astype(str).map(len).max(),  # len of largest item
            len(str(series.name))  # len of column name/header
        )) + 1  # adding a little extra space

        if (col == "Link"):
            worksheet.set_column(idx, idx, max_len//2)
        else:
            worksheet.set_column(idx, idx, max_len)  # set column width

    writer.save()


if __name__ == "__main__":
    main()
