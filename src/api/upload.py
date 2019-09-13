from minio import Minio
from minio.error import ResponseError
import os
from config import ACCESS_KEY_ID, SECRET_KEY_ID, BACKEND, BUCKET

def upload_file(body):

    if body:

        try:

            minioClient = Minio(BACKEND,
                                access_key=ACCESS_KEY_ID,
                                secret_key=SECRET_KEY_ID,
                                secure=True)
            
            try:

                bucket = minioClient.bucket_exists(BUCKET)

                if not bucket:

                    try:
                        """
                        Create the bucket if not exists.
                        """
                        minioClient.make_bucket(BUCKET, location='us-east-1')

                        print("Bucket has been created successfully.")

                    except Exception as e:
                        return {'Code':404, 'Error':e}
                
                """
                Upload the object/file.
                """

                file_path = body['uri']
                version_of_package = body['version']

                file_name = list(file_path.split('/'))[-1]

                ver = list(version_of_package.split('.'))

                first_version, second_version, third_version = ver[0], ver[1], ver[2]

                backend_file = first_version+"/"+second_version+"/"+third_version+"/"+file_name

                minioClient.fput_object(BUCKET, backend_file, file_path)

                return {'code':200, 'message':'File uploaded successfully.'}

            
            except Exception as e:
                return {'Code':404, 'Error':e}



        
        except Exception as e:
            print(e)