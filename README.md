# Receipt_Processor
The Receipt Processor is a webservice that fulfils the documented API, it is to process and analyze receipt data. It leverages Docker for containerization, ensuring a consistent and isolated environment for execution.

## Prerequisites
Docker: Install Docker to run the application within a container.
Build the Docker Image:
    docker build -t receipt_processor .
Run the Docker Container:
    docker run --rm receipt_processor

## Project Structure
main.py: The main script to run the application. 

requirements.txt: Lists the Python dependencies.  

Dockerfile: Contains instructions to build the Docker image.
