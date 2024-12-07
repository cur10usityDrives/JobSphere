# import csv
# from jobspy import scrape_jobs

# jobs = scrape_jobs(
#     site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor", "google"],
#     search_term="Computer science, Html5, Photoshop, Php, Cms, Design, Wordpress, Sql, Api, Adobe, Benchmark, Front End Developer",
#     google_search_term="software engineer jobs near San Francisco, CA since yesterday",
#     location="San Francisco, CA",
#     results_wanted=20,
#     hours_old=72,
#     country_indeed='USA',
    
#     # linkedin_fetch_description=True # gets more info such as description, direct job url (slower)
#     # proxies=["208.195.175.46:65095", "208.195.175.45:65095", "localhost"],
# )
# print(f"Found {len(jobs)} jobs")
# print(jobs.head())
# jobs.to_csv("jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False) # to_excel


import pandas as pd
import time
import sys
import json
from urllib.error import HTTPError
from jobspy import scrape_jobs  # type: ignore # Import the JobSpy module

# Get arguments passed from Node.js searchTerm, googleSearchTerm, location
job_title = sys.argv[1]
google_search_term = sys.argv[2]
location = sys.argv[3]

# Fetch jobs based on the parsed resume data
def fetch_jobs(job_title, google_search_term, location): # type: ignore
    retries = 5  # Max retries
    delay = 10  # Delay in seconds before retrying
    
    for attempt in range(retries): # type: ignore
        try:
            jobs = scrape_jobs( # type: ignore
                site_name=["indeed", "zip_recruiter", "glassdoor", "google"],
                search_term=job_title,
                google_search_term=google_search_term,
                location=location,
                results_wanted=20,
                hours_old=72,
                country_indeed='USA'
            )
            

            # Ensure jobs is a DataFrame, and convert it to JSON format
            if isinstance(jobs, pd.DataFrame):
                return jobs.to_json(orient="records")  # type: ignore # Convert DataFrame to JSON
            
            return json.dumps(jobs)  # Return as is if it's already in JSON format
        
        except HTTPError as e:
            if e.response.status_code == 429:  # Handle 429 error (Too Many Requests)
                print(f"Rate limit reached. Retrying in {delay} seconds...")
                time.sleep(delay)  # Wait before retrying
            else:
                raise e  # Re-raise the error if it's not a 429 error
    raise Exception("Max retries exceeded, unable to scrape jobs.")

# Call the function to get jobs and print them as a JSON string
if __name__ == "__main__":
    jobs = fetch_jobs(job_title, google_search_term, location)  # type: ignore
    
    print(jobs)