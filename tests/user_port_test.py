# /usr/bin/env python
# -*- coding: utf-8 -*-
"""
user接口单元测试
"""
import pytest
import requests

Token = ''
test_email = "jiangzheng@bilibili.com"
password = "123"


class TestProject(object):
    """ 接口单元测试
    """

    def test_verify_code(self):
        url = "http://localhost:8000/user/verify/code"
        data_json = {
            "email": test_email
        }
        response = requests.get(url=url, params=data_json)
        assert response.status_code == 200
        assert response.json()['code'] == 0
        assert response.json()['msg'] == 'success'

    def test_user_login(self):
        url = "http://localhost:8000/user/login"
        data_json = {
            "email": test_email,
            "password": password
        }
        response = requests.post(url=url, json=data_json)
        assert response.status_code == 200
        assert response.json()['code'] == 0
        assert response.json()['data']['Token'] != ''
        global Token
        Token = response.json()['data']['Token']

    def test_user_update(self):
        url = "http://localhost:8000/user/update"
        data_json = {
            "email": test_email,
            "role": "root",
            "status": 1
        }
        headers = {
            "Authorization": "Bearer {}".format(Token)
        }
        response = requests.put(url=url, json=data_json, headers=headers)
        assert response.status_code == 200
        assert response.json()['code'] == 0
        assert response.json()['data']['info'] == 'update success!'

    def test_user_status(self):
        url = "http://localhost:8000/user/status"
        headers = {
            "Authorization": "Bearer {}".format(Token)
        }
        response = requests.get(url=url, headers=headers)
        assert response.status_code == 200
        assert response.json()['code'] == 0
        assert response.json()['data']['data']['email'] == test_email

    def test_admin_search_user_status(self):
        url = "http://localhost:8000/user/admin-status"
        data_json = {
            "user_id": test_email
        }
        headers = {
            "Authorization": "Bearer {}".format(Token)
        }
        response = requests.get(url=url, params=data_json, headers=headers)
        assert response.status_code == 200
        assert response.json()['code'] == 0
        assert response.json()['data']['data']['email'] == test_email


if __name__ == "__main__":
    pytest.main(["-s", "user_port_test.py"])
