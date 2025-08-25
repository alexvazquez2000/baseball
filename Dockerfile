# Use an official Python runtime as a base image
FROM python:3.13.7

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
#COPY . .  ## don't copy anything - only copy run.py so we have something.  It will run with the live dir mounted as /app/data
COPY run.py .

# Expose the port Flask will run on
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "run.py"]


#Google: run flask and mysql in a docker container

#To build the docker image
## docker build -t baseball-flask-app .

#To run the image as a container
## docker run -p 5000:5000 baseball-flask-app

#Run the Docker Container with Volume Mounting:
## docker run -p 5000:5000 -v C:/Users/alexv/workspace/baseball/:/app/data -it --workdir /app/data baseball-flask-app

#---------------

#Run the Docker Container with Volume Mounting: detached
#docker run -d -p 5000:5000 -v /Users/alexv/workspace/baseball:/app/data -it --workdir /app/data baseball-flask-app

#To get the containerID - CONTAINERID
## docker ps

#To get access to the detached image
## docker exec -it CONTAINERID bash

#to view the logs use (-f makes it run continuous -  remove the -f to see just once)
## docker logs -f CONTAINERID

#To stop the detached image 
## docker kill CONTAINERID

