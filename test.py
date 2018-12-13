import unittest
from api import app
import json
import time


class APITest(unittest.TestCase):
    IMAGE_DATA = {
            "urls": [
                "https://farm3.staticflickr.com/2879/11234651086_681b3c2c00_b_d.jpg",
                "https://farm4.staticflickr.com/3790/11244125445_3c2f32cd83_k_d.jpg"
            ]
    }

    JSON_HEADER = {'Content-type': 'application/json'}

    JOB_ID = ""

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass
    
    def test_images_upload_with_text_content(self):
       
        response = self.app.post('/v1/images/upload/', data=self.IMAGE_DATA, follow_redirects=False)
        response_json = response.get_json()
        self.assertEqual(response.status_code, 404)  #should be bad request

    def test_images_upload(self):
       
        response = self.app.post('/v1/images/upload', data=json.dumps(self.IMAGE_DATA), headers=self.JSON_HEADER, follow_redirects=True)
        json_data = json.loads(response.data)
        job_id_available =  "jobId" in json_data
        if job_id_available:
            self.__class__.JOB_ID = json_data["jobId"]

        self.assertEqual(response.status_code, 200)
        assert job_id_available

    
    def test_job_status(self):
        if self.__class__.JOB_ID != "":
            response = self.app.get('/v1/images/upload/'+self.__class__.JOB_ID, follow_redirects=True)
            json_data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            assert "id" in json_data
            assert json_data["status"] in "in-progress"
        else:
            assert False


    def test_images(self):
        response = self.app.get('/v1/images', follow_redirects=True)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        assert "uploaded" in json_data
        assert len(json_data["uploaded"]) > 0  #it should fail here


 
if __name__ == "__main__":
    unittest.main()
