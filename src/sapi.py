import os 
from dotenv import load_dotenv
from serpapi import GoogleSearch
import streamlit as st
load_dotenv()
serp_api_key = os.getenv("SERP_API_KEY")
import requests



# from apify_client import ApifyClient
# from urllib.parse import quote_plus
# apify_client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

## You can use apify seek-australia actor to fetch jobs from seek australia
# # Fetch seek austrlia jobs based on search query and location
# def fetch_seek_jobs(search_query):
#     search_urls = [f"https://www.seek.com.au/jobs?keywords={quote_plus(k)}" for k in search_query]
#     run_input = {
#         "searchUrls": search_urls,
#         "maxItems": 50,
#         "proxyConfiguration": {"useApifyProxy": False},
#     }
#     run = apify_client.actor("sSGRulbObpb1cPos5").call(run_input=run_input)
#     jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
#     return jobs


## fectching job using serp api

# def fetch_jobs_from_serpapi(keywords:list[str], location: str="Australia"):
#     all_results = []
#     print("keywords:", keywords)
#     print("location:", location)
    
#     for keyword in keywords:
#          params = {
#             "engine": "google_jobs",
#             "q":f" Vacany of {keyword} jobs in {location}",      
#             "hl": "en",
#             "location": location,
#             "num": 1,
#             "api_key": serp_api_key
#         }
#          search = GoogleSearch(params)
#          results = search.get_dict()
#         #  all_results.append(results)
#          filtered_result={
#                "keyword":keyword,
#                "google_jobs_url": results.get("search_metadata", {}).get("google_jobs_url"),
#                "location_used": results.get("search_parameters", {}).get("location_used")
#         }
#          all_results.append(filtered_result)
    
#     return all_results
         


## to test the function uncomment below lines
# results=fetch_jobs_from_serpapi(["Data Scientist", "Machine Learning Engineer"], "Germany")
# print(results)


rapid_api_key=os.getenv("RAPID_API")
def fetch_jobs(keywords:list[str], location:str):
    url="https://jsearch.p.rapidapi.com/search"
    headers = {
        "x-rapidapi-key": rapid_api_key,
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }
    all_jobs = []
    for keyword in keywords:
         querystring = {
            "query": f"{keyword} jobs in {location}",
            "page": "1",
            "num_pages": 1,
            "country": location,
            "date_posted": "all"
        }
         response = requests.get(url, headers=headers, params=querystring)
         data = response.json()
         
         if "data" in data:
             jobs = data["data"]
             for job in jobs:
                # try:
                #     print("**************")
                #     print("job title",job['job_title'])
                #     print("type of job title",type(job['job_title']))
                #     print("company name",job['employer_name'])
                #     print("type of company name",type(job['employer_name']))
                #     print("location",job['job_location'])
                #     print("type of location",type(job['job_location']))
                #     print("employment type",job['job_employment_type'])
                #     print("type of employment type",type(job['job_employment_type']))
                #     print("job link",job['job_apply_link'])
                #     print("type of job link",type(job['job_apply_link']))
                #     print("**************")
                # except Exception as e:
                #     print(f"Error printing job details: {e}")
                filtered_job = {
                     "job_title":job.get("job_title") ,
                     "company_name": job.get("employer_name"),
                     "location": job.get("job_location"),
                     "employment_type": job.get("job_employment_type"),
                     "job_link": job.get("job_apply_link"),
                 }
                all_jobs.append(filtered_job)
    
            
    return all_jobs
             

# keywords = ["Software Developer"]
# location = "Chicago"
# jobs = fetch_jobs(keywords, location)
# if jobs:
#             st.subheader( "Job Recommendations")
#             for job in jobs:
#                 with st.container():
#                     st.markdown(f"### {job['job_title']}")
#                     st.write(f"**Company:** {job['company_name']}")
#                     st.write(f"**Location:** {job['location']}")
#                     st.write(f"**Employment Type:** {job['employment_type']}")
#                     st.markdown(f"[Apply Here]({job['job_link']})")
#                     st.markdown("---")
                        
# else:
#             st.warning("No jobs found.")
    
