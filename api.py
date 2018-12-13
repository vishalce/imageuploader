import flask
from flask import request, request, jsonify, abort
import threading
import datetime
from imgurpython import ImgurClient
import uuid
import os
from urllib.request import urlretrieve
import json
import configparser


app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.url_map.strict_slashes = False

'''
imgur configuration
'''
config = configparser.ConfigParser()
config.read('APP_CONFIG')

CLIENT_ID = config.get('credentials','CLIENT_ID')
CLIENT_SECRET = config.get('credentials','CLIENT_SECRET')

client = ImgurClient(CLIENT_ID, CLIENT_SECRET)


jobs = {}
uploaded_images = [] #list of uploaded images 

DOWNLOAD_FOLDER = os.path.basename('downloads')



def upload_failed():
    while True:
        for job_id in jobs:
            if job[job_id]['status'] == 'failed' or len(job[job_id]['uploaded']['failed']) >0 :
                for image in job[job_id]['uploaded']['failed']:
                    image_file_name = image_url[image_url.rfind("/")+1:]  
                    image_path = DOWNLOAD_FOLDER+"/"+image_file_name
                    uploaded_image = client.upload_from_path(image_path, config=None, anon=True)

'''
process upload task

'''
def process_upload(image_urls, job_id):
    
    '''
    getting resutl set of current job
    '''
    result = jobs[job_id]
    result['status'] = 'in-progress'
    jobs[job_id] = result

    '''
    processing each urls
    '''
    
    for image_url in image_urls:
        try:
            '''
            creating download directory if it does not exist
            '''

            if not os.path.exists(DOWNLOAD_FOLDER):
                os.makedirs(DOWNLOAD_FOLDER)

            '''
            downloading image
            '''
            image_file_name = image_url[image_url.rfind("/")+1:]  
            image_path = DOWNLOAD_FOLDER+"/"+image_file_name
           
            urlretrieve(image_url, image_path)

            '''
            uploading image 
            '''
            try:
                uploaded_image = client.upload_from_path(image_path, config=None, anon=True)
            except Exception as ex:
                uploaded_image = client.upload_from_path(image_path, config=None, anon=True)

                
            if "link" in uploaded_image:
                result['uploaded']['complete'].append(uploaded_image["link"])
                uploaded_images.append(uploaded_image["link"])
            else:
                result['uploaded']['failed'].append(image_url)

        except Exception as exception:
            result['uploaded']['failed'].append(image_url)
            print(exception)
        
        result['uploaded']['pending'].remove(image_url)
        jobs[job_id] = result
       
    result['status'] ='complete'
    result['finished']  = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    jobs[job_id] = result
    pass


'''
API starts here
'''
@app.route('/', methods=['GET'])
def index():
    return jsonify({"hello":"world"})


@app.route('/v1/images', methods=['GET'])
def list_all_uploaded_images():
    return jsonify({"uploaded":uploaded_images})


@app.route('/v1/images/upload/', methods=['POST'])
def upload():
    if request.get_json() == None:
        abort(404)
    image_urls = request.get_json()['urls']
    image_urls = set(image_urls) #removing duplicate urls from the list
    job_id = str(uuid.uuid1()) #generating unique job id
    
    result = {}  #creating result dict
    result['id'] =  job_id
    result['created'] = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    result['finished'] = None
    result['status'] = 'pending'
    result['uploaded'] = {
        'pending': list(image_urls),
        'complete':[],
        'failed':[]
    }
    jobs[job_id] = result
    threading.Thread(target=process_upload, args= (image_urls,job_id,)).start()
    return jsonify({'jobId':job_id})


@app.route('/v1/images/upload/<job_id>', methods=['GET'])
def get_job_status(job_id):
    if job_id not in jobs:
        return jsonify({"error":"JobId not available"})

    return jsonify(jobs[job_id])


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
    
    threading.thread(target=uploaded_failed).start()








