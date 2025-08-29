import fitz # PyMuPDF
import os 
from datetime import datetime
from dotenv import load_dotenv
import mimetypes
import httpx, time
from supabase import create_client, Client
load_dotenv()
url= os.environ.get("SUPABASE_URL_BUCKET")
key = os.environ.get("SUPABASE_KEY_BUCKET")
supabase= create_client(url, key)


# def extract_text_from_pdf(uploaded_file):
#     print("uploaded file type",type(uploaded_file))
#     print("uploaded file",uploaded_file.name)
#     filename=os.path.basename(uploaded_file.name)
#     print("filename",filename)
#     path_supabase= f"CVS/{filename}"
#     print("path supabase",path_supabase)
#     mime_type=mimetypes.guess_type(uploaded_file.name)[0]
#     print("mime type",mime_type)
    
#     with open(uploaded_file.name,"rb") as f:
#         response=(
#             supabase.storage
#             .from_("users-resumes")
#             .upload(
#                 file=f,
#                 path=path_supabase,
#                 file_options={"cache-control": "3600",
#                               "upsert": "false",
#                               "content-type": mime_type},
#             )
#         )
#     doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
#     text = ""
#     for page in doc:
#         text += page.get_text()
#     return text

# with open("Z:\\Job_system\\resources\\BidhanCV.pdf", "rb") as f:
#     resume_text = extract_text_from_pdf(f)
#     print(resume_text)



def extract_text_from_pdf(uploaded_file):
    # print("uploaded file type",type(uploaded_file))
    # print("uploaded file",uploaded_file.name)
    filename=os.path.basename(uploaded_file.name)
    # print("filename",filename)
    timestamp=datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    path_supabase= f"CVS/{filename}_{timestamp}"
    # print("path supabase",path_supabase)
    mime_type=mimetypes.guess_type(uploaded_file.name)[0]
    # print("mime type",mime_type)
    temp_path = f"temp_{filename}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())  # write BytesIO to disk
        
        
        # doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    doc=fitz.open(temp_path)  # open from disk
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    
    ## uploading with  retry logic
    max_retries =3
    retry_delay = 2
    
    
    for attempt in range(max_retries):
        try:
             with open(temp_path,"rb") as f:
                response=(
                    supabase.storage
                    .from_("users-resumes")
                    .upload(
                        file=f,
                        path=path_supabase,
                        file_options={"cache-control": "3600",
                                    "upsert": "true",
                                    "content-type": mime_type},
                    )
                )
                break
        except httpx.RemoteProtocolError as e:
            if attempt < max_retries - 1:
                print(f"Upload failed (attempt {attempt + 1}/{max_retries}). Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                print("Max retries reached. Upload failed.")
            
                
                
    ## clean up the temporary file
    try:
        os.remove(temp_path)  
    except Exception as e:
        print(f"Error deleting temporary file: {e}")
    return text







## when we upload a pdf file in streamlit using st.file_uploader, it returns an UploadedFile object which often behaves like a BytesIO object.
## But in case of the with open the return type is  a io._io.BufferedReader object , and for compatibity to upload in the supabase we convert it into a io.BufferReader object 
## so becausse of this we convert the UploadedFile object into a BufferedReader object by writing it to a temporary filee
## check for pdf2 reader, it may accept  a file like object directly without converting
