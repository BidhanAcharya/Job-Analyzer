import streamlit as st
from src.gemini_helper import text_generator, job_keyword,analyze_resume
from src.text_extractor import extract_text_from_pdf
from src.sapi import fetch_jobs

def run_app(supabase):
    st.set_page_config(page_title="Job Recommender", layout="wide")
    st.title("AI Job Recommender")
    tabs=st.tabs(["Upload Resume","Dashboard","Resume vs Job Description Analyzer"])
    with tabs[0]:
        st.markdown("Upload your resume and get job recommendations based on your skills and experience from LinkedIn and Naukri.")
        uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

        if uploaded_file:
            with st.spinner("Extracting text from your resume..."):
                resume_text = extract_text_from_pdf(uploaded_file)

            with st.spinner("Summarizing your resume..."):
                summary = text_generator(f"Summarize this resume highlighting the skills, edcucation, and experience: \n\n{resume_text}")
            
            # Display nicely formatted results
            st.markdown("---")
            st.header("📑 Resume Summary")
            st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{summary}</div>", unsafe_allow_html=True)
            st.success("✅ Analysis Completed Successfully!")
            
            ## Give an option to input location preference
            location = st.text_input("Enter a location e.g., Australia, USA, Germany")




            if st.button("🔎Get Job Recommendations"):

                with st.spinner("Fetching job recommendations..."):
                    import ast
                    keywords = job_keyword( f"""
                    Based on this resume summary, suggest the best job titles and keywords for searching jobs. Only suggest maximum up to 2 keyword that are highly relevant to the candidate's skills and experience.
                    Return the output as a List object strictly following this format:
                    [Keyword1, Keyword2]
                    Do not add any explanation, paragraph, or extra text outside the List.
                    Summary: {summary}
            
            """
        )    
                    print("Raw keywords from Gemini:", keywords)
                    keywords=ast.literal_eval(keywords)
                    print("Extracted keywords list:", keywords)
                st.success(f"Extracted Job Keywords: {keywords}")

                with st.spinner("Fetching jobs from seek"):
                    # seek_jobs = fetch_seek_jobs(keywords)
                    # jobs = fetch_jobs_from_serpapi(keywords, location)
                    jobs=fetch_jobs(keywords, location)
                    print("Fetched jobs:", jobs)
                    
                    
                
                    if jobs:
                        st.subheader("🎯 Job Recommendations")
                        for job in jobs:
                         try:
                            user_id=st.session_state["user_id"]
                            print("User_ID in job loop:", user_id)
                            print("job title",job['job_title'])
                            print("type of job title",type(job['job_title']))
                            print("company name",job['company_name'])
                            print("type of company name",type(job['company_name']))
                            print("location",job['location'])
                            print("type of location",type(job['location']))
                            print("employment type",job['employment_type'])
                            print("type of employment type",type(job['employment_type']))
                            print("job link",job['job_link'])
                            print("type of job link",type(job['job_link']))
                            print("**************")
                            # Save job to Supabase
                            supabase.table("jobs").insert({
                                "user_id":user_id,
                                "job_title":job['job_title'],
                                "company_name":job['company_name'],
                                "location":job['location'],
                                "employment_type":job['employment_type'],
                                "job_link":job['job_link']
                            }).execute()
                            
                         except Exception as e:
                            st.error(f"Failed to save job to database: {e}")
                                    
                        with st.container():
                                st.markdown(f"### {job['job_title']}")
                                st.write(f"**Company:** {job['company_name']}")
                                st.write(f"**Location:** {job['location']}")
                                st.write(f"**Employment Type:** {job['employment_type']}")
                                st.markdown(f"[Apply Here]({job['job_link']})")
                                st.markdown("---")
                                
                    else:
                        st.warning("No jobs found.")
    with tabs[1]:
         st.header("📊 Your Saved Jobs")
         user_id = st.session_state.get("user_id")
         if not user_id:
            st.warning("Please login first to view your dashboard.")
         else:
            try:
                response = supabase.table("jobs").select("*").eq("user_id", user_id).execute()
                jobs = response.data

                if jobs:
                    for job in jobs:
                        with st.container():
                            st.markdown(f"### {job['job_title']}")
                            st.write(f"**Company:** {job['company_name']}")
                            st.write(f"**Location:** {job['location']}")
                            st.write(f"**Employment Type:** {job['employment_type']}")
                            st.markdown(f"[Apply Here]({job['job_link']})")
                            st.markdown("---")
                            
                            if job["applied"]:
                                st.success("✅ Applied")
                                
                                if job["reached_back"]:
                                    st.info("🔵 Reached Back")
                                else:
                                    if st.button("Mark Employer Reached Back 📞", key=f"reached_{job['id']}"):
                                        try:
                                            supabase.table("jobs").update({"reached_back": True}).eq("id", job["id"]).execute()
                                            st.success("Job marked as reached back!")
                                            st.rerun()  # refresh dashboard to reflect change
                                        except Exception as e:
                                            st.error(f"Failed to update job: {e}")
                                
                                
                            else:
                                if st.button(f"Mark as Applied ✅", key=f"apply_{job['id']}"):
                                    try:
                                        supabase.table("jobs").update({"applied": True}).eq("id", job["id"]).execute()
                                        st.success("Job marked as applied!")
                                        st.rerun()  # refresh dashboard to reflect change
                                    except Exception as e:
                                        st.error(f"Failed to update job: {e}")
                            st.markdown("---")      
                                        
                else:
                    st.info("No jobs saved yet.")
            except Exception as e:
                st.error(f"Error fetching jobs: {e}")
    with tabs[2]:
        st.header("Resume vs Job description Analyzer")
        st.markdown("""
                    <style>
                    textarea {
                        border-radius: 12px !important;
                        border: 1px solid #b8a8d5 !important;
                        padding: 15px !important;
                        font-size: 16px !important;
                        background-color: #f3f0fa !important; /* soft lavender */
                        color: #1a1a1a !important;
                        box-shadow: 0 2px 6px rgba(0,0,0,0.15) !important;
                    }
                    textarea::placeholder {
                        color: #6a5acd !important; /* slate blue placeholder */
                        opacity: 0.8 !important;
                        font-style: italic;
                    }
                    label[data-testid="stMarkdownContainer"] > p {
                        font-weight: 600;
                        font-size: 18px;
                        color: #4b3f72; /* deep lavender */
                        margin-bottom: 6px;
                    }
                    </style>
                """, unsafe_allow_html=True)
        
        job_description = st.text_area("Job Description", placeholder="Enter the job description here...")
        resume_text = st.text_area("Resume Text",placeholder="Paste your resume text here...")

        if st.button("Analyze Resume"):
            with st.spinner("Analyzing..."):
                result = analyze_resume(job_description, resume_text)
                with st.container():
                 st.write(result)

        
        
        
        

# run_app()
if __name__=="__main__":
    run_app()