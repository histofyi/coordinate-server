
import boto3
from botocore.client import Config

import os


import json
import logging




class localClient():

    def __init__(self, basedir):
        self.basedir = basedir


    def create_file_handle(self, bucket, key):
        file_handle = f'{self.basedir}/{bucket}/{key}'
        return file_handle


    def get_object(self, Bucket='test', Key='test'):
        file_handle = self.create_file_handle(Bucket, Key)
        file_type = Key.rsplit('.', 1)[1]
        data, success, errors = self.fs.get(None, format=file_type, fullpath=file_handle)
        if success:
            try:
                data = json.dumps(data)
            except:
                data = data
        return data


    def put_object(self, Body=None, Bucket=None, Key=None):
        file_handle = self.create_file_handle(Bucket, Key)
        path = file_handle.rsplit('/', 1)[0]
        file_type = Key.rsplit('.', 1)[1]
        os.makedirs(path, exist_ok=True)
        data, success, errors = self.fs.put(None, Body, fullpath=file_handle, format=file_type)
        pass


class s3Provider():

    client = None
    bucket = None

    def __init__(self, aws_config):
        self.client = boto3.client('s3',
            aws_access_key_id = aws_config['aws_access_key_id'],
            aws_secret_access_key = aws_config['aws_access_secret']
        )
        self.bucket = aws_config['s3_bucket']


    def get(self, key, data_format='json'):
        try:
            
            data = self.client.get_object(Bucket=self.bucket, Key=key)['Body'].read()
            if len(data) > 0:
                if data_format == 'json':
                    try:
                        data = json.loads(data)
                        return data, True, []
                    except:
                        return None, False, ['not_json']
                else:
                    return data, True, []
            else:
               return None, False, ['no_data'] 
        except:
            return None, False, ['no_matching_key']


    def put(self, key, contents, data_format='json'):
        if contents:
            if len(contents) > 0:
                if key:
                    if data_format == 'json':
                        try:
                            contents = json.dumps(contents)
                        except:
                            return None, False, ['not_json']
                    else:
                        contents = contents
                    if contents:
                        self.client.put_object(Body=contents, Bucket=self.bucket, Key=key)
                        return contents, True, []
                    else:
                        return None, False, ['unable_to_persist_to_s3']
                else:
                    return None, False, ['no_key_provided']
            else:
                return None, False, ['no_content_provided']
        else:
            return None, False, ['no_content_provided']
    

    def update(self, key, contents, data_format='json'):
        if len(contents) > 0:
            if key:
                if data_format == 'json':
                    try:
                        contents = json.dumps(contents)
                    except:
                        return None, False, ['not_json']
                else:
                    contents = contents
                if contents:
                    self.client.put_object(Body=contents, Bucket=self.bucket, Key=key)
                    return contents, True, []
                else:
                    return None, False, ['unable_to_persist_to_s3']
            else:
                return None, False, ['no_key_provided']
        else:
            return None, False, ['no_content_provided']