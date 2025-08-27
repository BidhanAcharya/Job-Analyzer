import streamlit as st
from src.gemini_helper import text_generator, job_keyword
from src.text_extractor import extract_text_from_pdf
from src.sapi import fetch_jobs

def run_app():
    st.set_page_config(page_title="Job Recommender", layout="wide")
    st.title("AI Job Recommender")
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
                print("Number of jobs fetched:", len(jobs))
                
                
            
                if jobs:
                    st.subheader("🎯 Job Recommendations")
                    for job in jobs:
                     with st.container():
                            st.markdown(f"### {job['job_title']}")
                            st.write(f"**Company:** {job['company_name']}")
                            st.write(f"**Location:** {job['location']}")
                            st.write(f"**Employment Type:** {job['employment_type']}")
                            st.markdown(f"[Apply Here]({job['job_link']})")
                            st.markdown("---")
                            
                else:
                    st.warning("No jobs found.")

run_app()
