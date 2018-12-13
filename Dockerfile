# this is an official Python runtime, used as the parent image
FROM python:3.6.5-slim


# add the current directory to the container as /app
COPY . /app

# set the working directory in the container to /app

WORKDIR /app

RUN pip install --upgrade pip

# execute everyone's favorite pip command, pip install -r
RUN pip install --trusted-host pypi.python.org -r requirements.txt


ENTRYPOINT ["python"]
# execute the Flask app
CMD ["api.py"]