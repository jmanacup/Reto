from textual.app import App, ComposeResult
from textual.widgets import Input, Header, Footer, Button, Static
from textual.widget import Widget
from textual.binding import Binding
from textual.reactive import reactive

import asyncio

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class Result(Widget):

    result = reactive("")

    def render(self) -> str:
        return self.result


class Reto(App):

    job_name = ''
    job_location = ''
    page_count = ''
    file_name = ''

    BINDINGS = [
        Binding(key="escape", action="quit", description="Quit the app"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Input(placeholder="Insert Job Name here...", classes="box", name="jobName")
        yield Input(placeholder="Insert Location here...", classes="box", name="jobLocation")
        yield Input(placeholder="How many pages...", classes="box", name="pageCount")
        yield Input(placeholder="Filename for the file...", classes="box", name="fileName")
        yield Button(label="Get Jobs", classes="submitBtn")
        # yield TextLog(classes="result")
        yield Result(classes="result")

    def on_input_changed(self, event: Input.Changed) -> None:

        match(event.input.name):
            case "jobName": self.job_name = event.value
            case "jobLocation": self.job_location = event.value
            case "pageCount": self.page_count = event.value
            case "fileName": self.file_name = event.value

    async def on_button_pressed(self, event: Button.Pressed) -> None:

        self.query_one(Result).result = 'Retrieving jobs now...'
        await self.get_listing(self.job_name, self.job_location,
                               self.file_name, int(self.page_count))

        self.query(Input).refresh()
        self.query_one(Result).result = 'Jobs successfully retrieved!'

    async def get_listing(self, job_title, location, filename, pages):

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
        await asyncio.sleep(2)

        # input the job title
        driver.find_element("xpath",
                            '//*[@id="text-input-what"]').send_keys(job_title)
        await asyncio.sleep(1)

        # input the location; we need to clear out the inputs first
        driver.find_element(
            "xpath", '//*[@id="text-input-where"]').send_keys(Keys.CONTROL + 'a')
        await asyncio.sleep(1)

        driver.find_element(
            "xpath", '//*[@id="text-input-where"]').send_keys(location)

        driver.find_element(
            "xpath", '//*[@id="jobsearch"]/button').send_keys(Keys.ENTER)

        await asyncio.sleep(2)

        df = pd.DataFrame(columns=['Job Title', 'Company', 'Location', 'Link'])

        for i in range(pages):

            job_listings = driver.find_elements(
                By.CLASS_NAME, "job_seen_beacon")

            for job in job_listings:

                job_title = job.find_element(By.CLASS_NAME, "jobTitle").text
                company_name = job.find_element(
                    By.CLASS_NAME, "companyName").text

                # removes newline as well as comments
                location = job.find_element(By.CLASS_NAME, "companyLocation").text.replace(
                    '\n', " ").split('+', 1)[0]

                link = url + "viewjob?jk=" + \
                    job.find_element(By.TAG_NAME, "a").get_attribute("data-jk")
                link = '=HYPERLINK("' + link + '","' + link + '")'

                df.loc[len(df.index)] = [job_title,
                                         company_name, location, link]

            driver.find_element(
                "xpath", "//*[@data-testid=\"pagination-page-next\"]").click()

            await asyncio.sleep(2)

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
    app = Reto(css_path="style.css")
    app.run()
