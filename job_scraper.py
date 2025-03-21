from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient
import time


client = MongoClient("mongodb+srv://mrpooja01:Pooja1211@cluster0.frfsy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["cedars_sinai_jobs"]
collection = db["job_listings"]
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://careers.cshs.org/search-jobs")
wait = WebDriverWait(driver, 20)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "section#search-results-list ul li a")))

time.sleep(3)
def extract_detail(label):
    try:
        xpath = f"//b[contains(text(), '{label}')]/following-sibling::text()[1]"
        detail = driver.execute_script(
            "return document.evaluate(arguments[0], document, null, XPathResult.STRING_TYPE, null).stringValue;",
            xpath
        )
       
        return detail.replace('"', '').strip(" :\\n")
    except Exception:
        return "Not available"
job_elements = driver.find_elements(By.CSS_SELECTOR, "section#search-results-list ul li a")[:10]

job_data = []
num_scraped = 0

while num_scraped < 10:
   
    job_elements = driver.find_elements(By.CSS_SELECTOR, "section#search-results-list ul li a")

    if num_scraped >= len(job_elements):
        print("No more unique job listings available to scrape.")
        break

    job = job_elements[num_scraped]

    link = job.get_attribute("href")
    title = job.find_element(By.CSS_SELECTOR, "h2").text.strip()
    location = job.find_element(By.CSS_SELECTOR, "span.job-location").text.strip()


    driver.get(link)

    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.ajd_header__job-title, div.job-heading-block")))
    except TimeoutException:
        print(f"Timeout waiting for details of: {title}")
        driver.back()
        num_scraped += 1
        continue

    time.sleep(3)
    department = extract_detail("Department")

    

    try:
        responsibilities = driver.find_element(By.XPATH, "//section[@id='anchor-responsibilities']").text.strip()
    except:
        responsibilities = "Not available"

    try:
        qualifications = driver.find_element(
            By.CSS_SELECTOR, 
            "div.job-details__description-content[data-bind*='job.qualifications']"
        ).text.strip()
    except NoSuchElementException:
        qualifications = "Not available"


    job_record = {
        "title": title,
        "location": location,
        "department": department,
        "responsibilities": responsibilities,
        "qualifications": qualifications,
        "url": link
    }

    job_data.append(job_record)
    print(f"Scraped ({num_scraped + 1}): {title}")
    driver.back()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "section#search-results-list ul li a")))
    time.sleep(2)
    num_scraped += 1


if job_data:
    collection.insert_many(job_data)
    print("Successfully stored data in MongoDB!")
else:
    print("No data scraped!")

driver.quit()
client.close()
