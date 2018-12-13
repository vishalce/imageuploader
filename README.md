#  Image Uploader

Image Uploader is an application program interface which helps user to upload images on imgur.com using imgur.com python library.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

Before we start using this app, we need to install Python 3.6.5  and Dockerin the system.

### Installing

Please follow these steps to get a development env running

#### Checkout the Git Repository

```
git clone https://github.com/vishalce/imageuploader.git 
```
and then 

```
cd imageuploader
```

#### Install Virtual Environment

```
pip install virtualenv
```

#### Create Virtual Environment

```
virtaulenv imageuploaderenv
```

#### Activate Virtual Environment

```
source imageuploaderenv/bin/activate
```

#### Install all the dependencies from requirements.txt 

```
pip install -r requirements.txt
```

#### Now build the application using Docker (considering you've started the docker)

```
docker build -t imageuploader:latest .
```

#### Now run the application using Docker

```
docker run -d -p 5000:5000 imageuploader
```

and the application is running on http://localhost:5000. Now you can test the APIs using postman. 



## Running the unit tests

You can run the unit test by executing follwing command under the same directory of the project.
```
python test.py
```

