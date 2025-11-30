from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time, csv, random

# ------------------- CONFIG -------------------
BASE_URL = "https://www.naukri.com/data-analyst-jobs-in-navi-mumbai-{}"
OUTPUT_FILE = "naukri_full_200_pages.csv"

MAX_PAGES = 200
MAX_SCROLLS = 10
SCROLL_PAUSE = 1.2
HEADLESS = False
# ----------------------------------------------

# Setup Chrome
options = Options()
if HEADLESS:
    options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--log-level=3")
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 20)

all_jobs = []

# -------------------- PAGINATION LOOP --------------------
for page in range(1, MAX_PAGES + 1):

    url = BASE_URL.format(page)
    print(f"\n📄 Scraping Page {page}: {url}")

    driver.get(url)
    time.sleep(random.uniform(2, 4))

    # Check if job cards exist
    try:
        wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div.srp-jobtuple-wrapper")
        ))
    except:
        print("⚠️ No more pages found. Stopping.")
        break

    # Scroll to load all jobs (usually 20)
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(MAX_SCROLLS):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    job_cards = driver.find_elements(By.CSS_SELECTOR, "div.srp-jobtuple-wrapper")
    print(f"📊 Found {len(job_cards)} jobs")

    # ---------------- SCRAPE EACH JOB LISTING ----------------
    for card in job_cards:

        # Basic fields from listing page
        try:
            title_el = card.find_element(By.CSS_SELECTOR, "a.title")
            title = title_el.text.strip()
            job_link = title_el.get_attribute("href")
        except:
            title, job_link = "N/A", ""

        try:
            company = card.find_element(By.CSS_SELECTOR, "a.comp-name").text.strip()
        except:
            company = "N/A"

        try:
            location = card.find_element(By.CSS_SELECTOR, ".locWdth").text.strip()
        except:
            location = "N/A"

        try:
            experience = card.find_element(By.CSS_SELECTOR, ".expwdth").text.strip()
        except:
            experience = "N/A"

        # -------------- OPEN JOB PAGE IN NEW TAB --------------
        driver.execute_script("window.open(arguments[0], '_blank');", job_link)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(random.uniform(2, 4))

        # -------- Salary --------
        try:
            salary = driver.find_element(By.CSS_SELECTOR, "div.styles_jhc__salary__jdfEC span").text.strip()
        except:
            salary = "N/A"

        # -------- Skills --------
        skills = []
        try:
            skill_elements = driver.find_elements(By.CSS_SELECTOR, "a.styles_chip__7YCfG span")
            skills = [s.text.strip() for s in skill_elements]
        except:
            pass

        # -------- INDUSTRY TYPE --------
        try:
          industry_type = driver.find_element(
        By.XPATH,
        "//div[@class='styles_details__Y424J'][.//label[contains(text(), 'Industry Type')]]//span/a"
    ).text.strip()
        except:
         industry_type = "N/A"

        # -------- Date Posted --------
        try:
            date_posted = driver.find_element(By.CSS_SELECTOR,
                "div.styles_jhc__jd-stats__KrId0 span span"
            ).text.strip()
        except:
            date_posted = "N/A"

        # Close tab & return
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        # Save row
        all_jobs.append({
            "Title": title,
            "Company": company,
            "Location": location,
            "Experience": experience,
            "Salary": salary,
            "Skills": ", ".join(skills),
            "Date Posted": date_posted,
            "Industry type":industry_type,
            "Job Link": job_link
        })

        time.sleep(random.uniform(1, 2))

# -------------------- SAVE CSV --------------------
if all_jobs:
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_jobs[0].keys())
        writer.writeheader()
        writer.writerows(all_jobs)

    print(f"\n✅ Successfully scraped {len(all_jobs)} total jobs!")
    print(f"📁 CSV saved as: {OUTPUT_FILE}")
else:
    print("⚠ No data scraped!")

driver.quit()
