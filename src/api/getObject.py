from minio import Minio
from config import ACCESS_KEY_ID, SECRET_KEY_ID, BACKEND, BUCKET

class Pull_Objects:

    def __init__(self):

        try:
            self.minioClient = Minio(BACKEND,
                            access_key=ACCESS_KEY_ID,
                            secret_key=SECRET_KEY_ID,
                            secure=True)
        except Exception as e:
            print(e)
    
    def single_object(self, body):

        try:
            bucket = self.minioClient.bucket_exists(BUCKET)

        except Exception as e:
            return {'code':404, 'Error':"Bucket not found."}
        
        else:

            try:
                version_of_package = body['version']
                ver = list(version_of_package.split('.'))
                first_version, second_version, third_version = ver[0], ver[1], ver[2]

                objects = self.minioClient.list_objects(BUCKET, recursive=True)

                for obj in objects:
                    versions = list(obj.object_name.split('/'))
                    if first_version == versions[0] and second_version == versions[1] and third_version == versions[2]:
                        location = obj.object_name
                        break
                
                result_url = self.minioClient.presigned_get_object(BUCKET, location)

                return {'code':200, 'url':result_url}

            except Exception as e:
                return {'code':404, 'Error':"File not found."}

    def latest_object(self):
        try:
            bucket = self.minioClient.bucket_exists(BUCKET)

        except Exception as e:
            return {'code':404, 'Error':"Bucket not found."}
        
        else:

            try:

                objects = self.minioClient.list_objects(BUCKET, recursive=True)

                last_object = list(objects)[-1].object_name
                
                result_url = self.minioClient.presigned_get_object(BUCKET, last_object)

                return {'code':200, 'url':result_url}

            except Exception as e:
                return {'code':404, 'Error':"File not found."}
    
    def get_All_objects(self):

        try:
            bucket = self.minioClient.bucket_exists(BUCKET)

        except Exception as e:
            return {'code':404, 'Error':"Bucket not found."}
        
        else:

            try:

                objects = self.minioClient.list_objects(BUCKET, recursive=True)
                result_url = {}
                for obj in objects:
                    result_url[obj.object_name] = self.minioClient.presigned_get_object(BUCKET, obj.object_name)

                return {'code':200, 'url':result_url}

            except Exception as e:
                return {'code':404, 'Error':"File not found."}

    def delete_object(self, body):

        try:
            bucket = self.minioClient.bucket_exists(BUCKET)

        except Exception as e:
            return {'code':404, 'Error':"Bucket not found."}
        
        else:
            try:
                version_of_package = body['version']
                ver = list(version_of_package.split('.'))
                first_version, second_version, third_version = ver[0], ver[1], ver[2]

                objects = self.minioClient.list_objects(BUCKET, recursive=True)

                for obj in objects:
                    versions = list(obj.object_name.split('/'))
                    if first_version == versions[0] and second_version == versions[1] and third_version == versions[2]:
                        break
                
                result_url = self.minioClient.remove_object(BUCKET, obj.object_name)

                return {'code':200, 'message':'Object Deleted.'}

            except Exception as e:
                return {'code':404, 'Error':"File not found."}


