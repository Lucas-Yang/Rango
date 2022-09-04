# /usr/bin/env python
# -*- coding: utf-8 -*-
"""
task接口单元测试
"""
import json
import time

import pytest
import requests

task_id = ''
fid = ''


class TestProject(object):
    """ 接口单元测试
    """

    def test_get_task_id(self):
        url = "http://localhost:8000/video/get-task-id"
        response = requests.get(url=url)
        assert response.status_code == 200
        assert response.text != ""
        global task_id
        task_id = response.text.replace("\"", "")

    def test_create_task(self):
        url = "http://localhost:8000/video/tagging/task"
        data_json = {
            "task_id": task_id,
            "job_name": "jz_test",
            "user": "aaa@xxx.com",
            "job_type": "tagging",
            "questionnaire_num": 100
        }
        response = requests.post(url=url, json=data_json)
        assert response.status_code == 200
        assert response.json()['code'] == 0
        assert response.json()['msg'] == 'success'
        assert response.json()['data']['task_id'] == task_id

    def test_update_task(self):
        url = "http://localhost:8000/video/tagging/task"
        data_json = {
            "task_id": task_id,
            "job_name": "jz_test_update",
            "user": "aaa@xxx.com",
            "job_type": "tagging",
            "questionnaire_num": 50
        }
        response = requests.put(url=url, json=data_json)
        assert response.status_code == 200
        assert response.json()['code'] == 0
        assert response.json()['msg'] == 'success'
        assert response.json()['data']['modify_num'] == 1

    # def test_query_task(self):
    #     url = "http://localhost:8000/video/tagging/task/status"
    #     data_json = {
    #         "task_id": task_id
    #     }
    #     response = requests.get(url=url, params=data_json)
    #     assert response.status_code == 200
    #     assert response.json()['code'] == 0
    #     assert response.json()['msg'] == 'success'
    #     assert response.json()['data']['task_info']['task_id'] == task_id

    def test_query_task_by_user(self):
        url = "http://localhost:8000/video/tagging/task-status"
        data_json = {
            "user": "aaa@xxx.com"
        }
        response = requests.get(url=url, params=data_json)
        assert response.status_code == 200
        assert response.json()['code'] == 0
        assert response.json()['msg'] == 'success'
        assert response.json()['data']['task_info'][0]['task_id'] == task_id
        assert response.json()['data']['count'] > 0

    def test_video_upload(self):
        url = "http://localhost:8000/video/task-file/upload"
        data_json = {
            "task_id": task_id,
            "group_id": 1,
            "video_index": 1
        }
        files = {"file": open('./README.md', 'rb')}
        response = requests.post(url=url, params=data_json, files=files)
        assert response.status_code == 200
        assert response.json()['code'] == 0
        assert response.json()['msg'] == 'success'
        assert response.json()['data']['file_name'] == 'README.md'
        assert response.json()['data']['file_address'] != ""
        file_info = eval(response.json()['data']['file_address'])
        global fid
        fid = file_info['fid']

    def test_task_score(self):
        url = "http://localhost:8000/video/tagging/group/score"
        data_json = {
            "task_id": task_id,
            "group_id": 1,
            "scores": [5],
            "user": "aaa@xxx.com"
        }
        response = requests.post(url=url, json=data_json)
        assert response.status_code == 200
        assert response.json()['code'] == 0
        assert response.json()['msg'] == 'success'
        assert response.json()['data']['insert_info']['task_id'] == task_id

    def test_video_record_task_user(self):
        url = "http://localhost:8000/video/tagging/task/user"
        data_json = {
            "task_id": task_id,
            "status": "do",
            "user": "aaa@xxx.com"
        }
        response = requests.post(url=url, json=data_json)
        assert response.status_code == 200
        assert response.json()['code'] == 0
        assert response.json()['msg'] == 'success'
        assert response.json()['data']['insert_info'] == "aaa@xxx.com"

    def test_compute_task_score(self):
        url = "http://localhost:8000/video/tagging/task/score"
        data_json = {
            "task_id": task_id
        }
        response = requests.post(url=url, params=data_json)
        assert response.status_code == 200
        assert response.json()['code'] == 0
        assert response.json()['msg'] == 'success'
        assert response.json()['data']['insert_info'] == [[5.0]]

    def test_query_task_score(self):
        url = "http://localhost:8000/video/tagging/task/score"
        data_json = {
            "user": "aaa@xxx.com"
        }
        response = requests.get(url=url, params=data_json)
        assert response.status_code == 200
        assert response.json()['code'] == 0
        assert response.json()['msg'] == 'success'
        assert response.json()['data']['count'] > 0

    def test_video_delete(self):
        url = "http://localhost:8000/video/task-file/delete"
        data_json = {
            "fid": fid
        }
        response = requests.delete(url=url, params=data_json)
        assert response.status_code == 200
        assert response.json()['code'] == 0
        assert response.json()['msg'] == 'success'
        assert response.json()['data']['task_delete_info'] == 1

    def test_task_delete(self):
        url = "http://localhost:8000/video/tagging/task"
        data_json = {
            "task_id": task_id
        }
        response = requests.delete(url=url, params=data_json)
        assert response.status_code == 200
        assert response.json()['code'] == 0
        assert response.json()['msg'] == 'success'
        assert response.json()['data']['task_delete_info'] == 1


if __name__ == "__main__":
    pytest.main(["-s", "task_port_test.py"])
