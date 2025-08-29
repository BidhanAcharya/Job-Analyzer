import fitz # PyMuPDF
import os 
from datetime import datetime
from dotenv import load_dotenv
import mimetypes
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
    print("uploaded file type",type(uploaded_file))
    print("uploaded file",uploaded_file.name)
    filename=os.path.basename(uploaded_file.name)
    print("filename",filename)
    timestamp=datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    path_supabase= f"CVS/{filename}_{timestamp}"
    print("path supabase",path_supabase)
    mime_type=mimetypes.guess_type(uploaded_file.name)[0]
    print("mime type",mime_type)
    temp_path = f"temp_{filename}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())  # write BytesIO to disk
    
    with open(temp_path,"rb") as f:
        response=(
            supabase.storage
            .from_("users-resumes")
            .upload(
                file=f,
                path=path_supabase,
                file_options={"cache-control": "3600",
                              "upsert": "false",
                              "content-type": mime_type},
            )
        )
    # doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    doc=fitz.open(temp_path)  # open from disk
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    os.remove(temp_path)  # clean up the temp file
    return text







## when we upload a pdf file in streamlit using st.file_uploader, it returns an UploadedFile object which often behaves like a BytesIO object.
## But in case of the with open the return type is  a io._io.BufferedReader object , and for compatibity to upload in the supabase we convert it into a io.BufferReader object 
## so becausse of this we convert the UploadedFile object into a BufferedReader object by writing it to a temporary filee
## check for pdf2 reader, it may accept  a file like object directly without converting
