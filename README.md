# Cedars-Sinai Job Listings Web Scraper

## Overview

This Python script automates the extraction of job postings from the [Cedars-Sinai careers website](https://careers.cshs.org/search-jobs) and stores the data neatly in a MongoDB database. The scraper retrieves key details from each job posting, including the title, location, department, responsibilities, qualifications, and direct link to the job listing.

## Approach

- **Web Scraping with Selenium:**  
  The Cedars-Sinai careers website dynamically loads content via JavaScript.
  Selenium was chosen as it effectively handles dynamically loaded pages.

- **Data Extraction:**  
  Specific CSS selectors and XPath expressions were used to accurately target and 
  extract details from the DOM structure of job pages.

- **MongoDB Storage:**  
  Extracted data is structured into clear MongoDB documents and stored in a cloud MongoDB Atlas database.

## How to Run the Script

### Step 1: Clone the repository (or copy script)

Place the script (`job_scraper.py`) in your working directory.

### Step 2: Set Up Python Environment

Create and activate a Python virtual environment:

```bash
python -m venv myenv
source myenv/bin/activate  
```

### Step 3: Install Dependencies

Install necessary packages using pip:

```bash
pip install selenium webdriver-manager pymongo
```

### Step 4: MongoDB Setup

1. **Create a MongoDB account:**
   - Visit [MongoDB Atlas](https://cloud.mongodb.com/) and create a free account.

2. **Create a Database and Collection:**
   - Database Name: `cedars_sinai_jobs`
   - Collection Name: `job_listings`

3. **Get MongoDB Connection URI:**
   - Replace the placeholder in the script with your MongoDB Atlas connection URI:

   ```python
   client = MongoClient("YOUR_MONGODB_CONNECTION_STRING")
   ```

### Step 5: Execute the Script

Run the script using Python:

```bash
python job_scraper.py
```

Upon execution, the script will scrape 10 job postings and insert the data into
your MongoDB collection.

## Dependencies

- Python (3.8 or higher recommended)
- Selenium
- Webdriver-manager
- PyMongo

Install with:

```bash
pip install selenium webdriver-manager pymongo
```

## Data Storage Details

Scraped job listings are stored with the following structure:

```json
{
  "title": "Job Title",
  "location": "Job Location",
  "department": "Job Department",
  "responsibilities": "Detailed responsibilities",
  "qualifications": "Job qualifications",
  "url": "Link to the job posting"
}
```

## Verifying Data in MongoDB

You can verify that the data has been inserted successfully:

1. Log in to your MongoDB Atlas.
2. Navigate to your database (`cedars_sinai_jobs`).
3. View your `job_listings` collection to confirm entries.



## Troubleshooting

- **Timeouts:** Increase the wait duration in Selenium if you experience frequent timeout errors.
- **Empty Fields:** Adjust selectors in the script if some fields consistently appear as "Not available."

---




