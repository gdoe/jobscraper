import requests
import xlwt
import xlrd
import datetime, time
from bs4 import BeautifulSoup

SNAGAJOB_BASE_URL = 'http://www.snagajob.com/job-search?ui=true&w='

'''
Scrapes the data from the "Companies" list on the left side bar of a snagajob search page.
'''
def scrape_jobs():
    print("snagajob" + str(datetime.date.today().strftime("%Y-%m-%d")) + ".xls")

    results = xlwt.Workbook(encoding="utf-8")

    city_book = xlrd.open_workbook("City_List.xlsx")
    city_sheet1 = city_book.sheet_by_index(0)
    for row in range(city_sheet1.nrows):
        city = city_sheet1.cell_value(row, 0)
        print(city)
        new_sheet = results.add_sheet(city)
        new_sheet.write(0, 0, "Company")
        new_sheet.write(0, 1, "Jobs")

        # Give a URL and get the HTML data back
        page = requests.get(SNAGAJOB_BASE_URL + city)
        # Turn the HTML data into parsable XML using the Beautiful Soup library modules
        soup = BeautifulSoup(page.content, "lxml")

        # Grab the list object since we know what class to look for
        all_companies = soup.find("ul", class_="company-facet-list")
        if all_companies:
            # Split up each item in the list (items that have the "li" tag)
            companies = all_companies.find_all("li")

            count = 1
            for each in companies:
                # Get the company name from the "a" (link) text
                name = each.a.text
                # Find the number inside of the parenthesis
                number_start = name.rfind('(')
                number_end = name.rfind(')')
                number = int(name[number_start+1:number_end])
                name = name[0:number_start].strip()

                # Print the name and number
                new_sheet.write(count, 0, name)
                new_sheet.write(count, 1, number)
                count += 1

        time.sleep(1)

    results.save("snagajob" + str(datetime.date.today().strftime("%Y-%m-%d")) + ".xls")


scrape_jobs()