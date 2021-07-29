import boto3
from botocore.config import Config
import os,uuid
class Boss:
    def __init__(self):
        self.bucket_name = 'ep_misc'
        self.expiration = 60 * 60 * 24 * 7
        self.aws_access_key_id = 'd55d2ce2574c322f'
        self.aws_secret_access_key = 'c61bec6abfb843b8e0e7129af62256ed'
        self.endpoint_url = 'http://uat-boss.bilibili.co'

        self.my_config = Config(
            region_name='uat',
            signature_version='s3v4',
            retries={
                'max_attempts': 10,
                'mode': 'standard'
            }
        )

        s3_session = boto3.Session(aws_access_key_id=self.aws_access_key_id,
                                   aws_secret_access_key=self.aws_secret_access_key)
        self._client = s3_session.client(service_name='s3', config=self.my_config, endpoint_url=self.endpoint_url)

    def upload_file(self, file_path: str, need_presigned: bool = True):
        """
        :param file_path: File to upload
        :param need_presigned: Whether need a presigned URL
        :param expiration: Expiration duration
        :return: The presigned URL if needed
        """
        name_pieces = os.path.basename(file_path).split('.')
        base_name = len(name_pieces) == 1 and name_pieces[0] or '.'.join(name_pieces[:-1])
        ext_name = len(name_pieces) > 1 and name_pieces[-1] or ''
        obj_name = f'{base_name}-{uuid.uuid1().hex[0:12]}'
        if ext_name:
            obj_name += f'.{ext_name}'
        self._client.upload_file(file_path, self.bucket_name, obj_name)
        if need_presigned:
            presigned_link = self._client.generate_presigned_url(ClientMethod='get_object',
                                                                 Params={
                                                                     'Bucket': self.bucket_name,
                                                                     'Key': obj_name
                                                                 },
                                                                 ExpiresIn=self.expiration)
            return presigned_link.split('?')[0]

    def upload_data(self,content_data,file_name, need_presigned: bool = True):
        obj_name = f'{uuid.uuid1().hex[0:4]}'+file_name
        self._client.upload_fileobj(content_data, self.bucket_name, obj_name)
        if need_presigned:
            presigned_link = self._client.generate_presigned_url(ClientMethod='get_object',
                                                                 Params={
                                                                     'Bucket': self.bucket_name,
                                                                     'Key': obj_name
                                                                 },
                                                                 ExpiresIn=self.expiration)
            return presigned_link.split('?')[0]
