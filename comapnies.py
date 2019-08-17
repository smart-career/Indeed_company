import json
import sys
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome('chromedriver.exe')
driver.set_window_size(1024, 600)
driver.maximize_window()
driver.get("https://www.indeed.com/companies")
input_company_name = " "
input_company_location = " "

input_company_name = input("Please Enter a Company Name: ")
input_company_location = input("Please Enter Location(optional): ")
try:
    search_company = driver.find_element_by_id("exploreCompaniesWhat")
except:
    print("Something Went Wrong. Please try again!")
    sys.exit(1)
try:
    location_company = driver.find_element_by_id("exploreCompaniesWhere")
except:
    print("Something Went Wrong. Please try again!")
    sys.exit(1)

search_company.send_keys(input_company_name)
if len(input_company_location) > 2:
    location_company.send_keys(input_company_location)
try:
    driver.find_element_by_xpath("//button [@class = 'icl-Button icl-Button--primary icl-Button--md icl-WhatWhere-button']").click()
except:
    print("Something Went Wrong. Please try again!")
    sys.exit(1)
try:
    WebDriverWait(driver, 60).until(expected_conditions.presence_of_element_located((By.XPATH, "//div[@class = 'cmp-CompanyWidget-details']/a")))
except:
    print("No Company Found!")
    sys.exit(1)

link = driver.find_elements_by_xpath("//div[@class = 'cmp-CompanyWidget-details']/a")
link = link[0].get_attribute("href")
link = link + "/reviews"

driver.get(link)
time.sleep(6)
company_name = ' '
average_rating = ' '
total_reviews = ' '
category_rating = []
company_jobs = ' '
locations = ' '
salry_reviews = ' '
salary_satisfection = ' '
papular_jobs = [ ]

data = {}
data['Company Detail'] = []
try:
    get_company_name  = driver.find_element_by_xpath("//div[@class = 'cmp-company-name']")
    company_name = get_company_name.text
except:
    print("Something went wrong")
    print("Please try again")
    sys.exit()

try:
    get_rating = driver.find_element_by_xpath("//span[@class = 'cmp-header-rating-average']")
    average_rating = get_rating.text
except:
    average_rating = ' '
    pass

try:
    get_total_reviews = driver.find_element_by_xpath("//div[@class = 'cmp-note']//span")
    total_reviews = get_total_reviews.text
except:
    pass

try:
    get_category_rating = driver.find_elements_by_xpath("//span[@class = 'cmp-review-filter-rating']")

    for i in range(0, len(get_category_rating)):
        if i == 0:
            a = get_category_rating[i].text + " Work-Life Balance "
        if i == 1:
            a = get_category_rating[i].text + " Pay & Benefits "
        if  i == 2:
            a = get_category_rating[i].text + " Job Security & Advancement "
        if i == 3:
            a = get_category_rating[i].text + " Management "
        if i == 4:
            a = get_category_rating[i].text + " Culture"
        category_rating.append(a)
except:
    pass

try:
    get_company_jobs = driver.find_element_by_xpath("//select[@id = 'cmp-job-title-select']")
    company_jobs = get_company_jobs.text
except:
    company_jobs = ' '
    pass

try:
    get_locations = driver.find_element_by_xpath("//select[@id = 'cmp-loc-select']")
    locations = get_locations.text
except:
    locations = ' '

# In Salaries tab
driver.find_element_by_xpath("//li[@class = 'cmp-menu--salaries']/a").click()
try:
    WebDriverWait(driver, 60).until(expected_conditions.presence_of_element_located((By.XPATH, "//li[@class = 'cmp-menu--salaries cmp-menu-selected']")))
    try:
        get_salary_reviews = driver.find_element_by_xpath("//li[@class = 'cmp-menu--salaries cmp-menu-selected']")
        salry_reviews = get_salary_reviews.text
    except:
        pass

    try:
        get_salary_satisfection = driver.find_element_by_xpath("//div[ @class = 'cmp-sal-satisfaction-chart']")
        salary_satisfection = get_salary_satisfection.text
    except:
        salary_satisfection = ' '
        pass

    try:
        get_papular_jobs = driver.find_elements_by_xpath("//div[@class = 'cmp-sal-title']")
        get_papular_salary = driver.find_elements_by_xpath("//div[@class = 'cmp-sal-summary']")
        for i in range(0, len(get_papular_jobs)):
            j_and_s = get_papular_jobs[i].text + " ( average Salary " + get_papular_salary[i].text + " )"
            papular_jobs.append(j_and_s)
    except:
        pass
except TimeoutException as es:
    pass

# Make a string of categories
c_list =" "
for i in range(0, len(category_rating)):
    c_list = c_list + category_rating[i] + ", "

# get company all papular jobs in a string
p_list =" "
for i in range(0, len(papular_jobs)):
    p_list = p_list + papular_jobs[i] + " "

company_name = company_name.translate({ord(i): None for i in '\n'})
average_rating = average_rating.translate({ord(i): None for i in '\n'})
total_reviews = total_reviews.translate({ord(i): None for i in '\n'})
company_jobs = company_jobs.replace("\n", " ")
locations = locations.translate({ord(i): None for i in '\n'})
salry_reviews = salry_reviews.translate({ord(i): None for i in '\n'})
salary_satisfection = salary_satisfection.translate({ord(i): None for i in '\n'})
p_list = p_list.translate({ord(i): None for i in '\n'})

data['Company Detail'].append({
    'Company Name': company_name,
    'Company Overall Rating': average_rating,
    'Total Reviews': total_reviews,
    'Rating By category ': c_list,
    'Company Jobs List': company_jobs,
    'Company All Locations': locations,
    'Total Salary Reviews': salry_reviews,
    'Salary Satisfaction': salary_satisfection,
    'Papular Jobs': p_list
})
with open('Output.json', 'w', encoding='utf-8') as outfile:
    json.dump(data, outfile, indent=4, ensure_ascii=False)

print('\nSTATUS: Scraping complete. Check "Output.json" for scraped data')
print('STATUS: Press any key to exit scraper')
exit = input('')
driver.quit()