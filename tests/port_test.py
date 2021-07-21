# /usr/bin/env python
# -*- coding: utf-8 -*-
"""
接口单元测试
"""
import pytest
import requests


class TestProject(object):
    """ 接口单元测试
    """
    def test_user_register(self):
        url = "http://localhost:8000/user/xxx"
        data_json = {
                    }
        response = requests.post(url=url, json=data_json)
        assert response.status_code == 200
        assert response.json()['code'] == 0
        assert response.json()['data'] == 'xxxxx'


if __name__ == "__main__":
    pytest.main(["-s", "port_test.py"])

