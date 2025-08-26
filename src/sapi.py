import os 
from dotenv import load_dotenv
from serpapi import GoogleSearch
import streamlit as st
load_dotenv()
serp_api_key = os.getenv("SERP_API_KEY")



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

def fetch_jobs_from_serpapi(keywords:list[str], location: str="Australia"):
    all_results = []
    print("keywords:", keywords)
    print("location:", location)
    
    for keyword in keywords:
         params = {
            "engine": "google_jobs",
            "q":f" Vacany of {keyword} jobs in {location}",      
            "hl": "en",
            "location": location,
            "num": 1,
            "api_key": serp_api_key
        }
         search = GoogleSearch(params)
         results = search.get_dict()
        #  all_results.append(results)
         filtered_result={
               "keyword":keyword,
               "google_jobs_url": results.get("search_metadata", {}).get("google_jobs_url"),
               "location_used": results.get("search_parameters", {}).get("location_used")
        }
         all_results.append(filtered_result)
    
    return all_results
         


## to test the function uncomment below lines
# results=fetch_jobs_from_serpapi(["Data Scientist", "Machine Learning Engineer"], "Germany")
# print(results)



