## Build stage 
# Use an official Python runtime as a parent image
FROM python:3.8-slim AS python

# Set the working directory to /app
WORKDIR /app

# Install gcc as it is needed to build wordcloud  
RUN apt-get update -y && \
    apt-get install -y gcc 

COPY requirements.txt /tmp/

# Install required Python libraries
RUN pip install -r /tmp/requirements.txt

# Copy data inside the Docker container data
COPY data/ /data

# Copy the current directory contents into the container at /app
COPY src/ /app
                                                                                                                                                                                                                                                                                                                               
# Run Python script to generate the graphs 
RUN python app.py && mkdir /images && mv *.png /images/


## Production stage
# Use an official ngix image for the static website                       
FROM nginx:stable-alpine

# Copy the dataset into nginx containers
COPY data/ /usr/share/nginx/html/ 

# Copy the output of images from app.py into nginx containers
COPY --from=python /images/ /usr/share/nginx/html/ 

# Copy html and css files into nginx containers
COPY html/ /usr/share/nginx/html/