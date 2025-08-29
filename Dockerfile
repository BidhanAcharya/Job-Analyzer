## To create a docker image of this app
FROM python:3.11-slim

##set the working directory 
WORKDIR /app
## copy the requirements file
COPY requirements.txt .
## install the dependencies
RUN pip install --no-cache-dir -r requirements.txt
## copy the application(rest of the app) code
COPY . .
##expose the streamlit port
EXPOSE 8501

##command to run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

