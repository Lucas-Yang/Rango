from jsonschema import validate

from app.common.logger import LogManager


class FormatCheck(object):
    """
    输入格式检查
    """

    def __init__(self):
        self.__loger = LogManager().logger

    def mock_fuzz_format_check(self, input_json):
        """ mock-server输入接口 参数校验
        :param input_json:
        :return:
        """
        json_schema = {
            "type": "object",
            "requiredv": True,
            "properties": {
                "rule_id": {"type": "integer"},
                "env_id": {
                    "description": "env_id is wrong",
                    "type": "string",
                    "minLength": 1
                },
                "host": {
                    "type": "string",
                    "minLength": 1},
                "tag": {
                    "type": "string",
                    "minLength": 1},
                "path": {
                    "type": "string",
                    "minLength": 1},
                "fuzz_response": {
                    "type": "string",
                    "minLength": 1},
                "fuzz_keys": {
                    "type": "string"},
                "status": {
                    "type": "integer",
                    "enum": [1, -1]},
                "creator": {
                    "type": "string",
                    "minLength": 1}
            },
            "required": [
                "rule_id",
                "env_id",
                "host",
                "tag",
                "path",
                "fuzz_response",
                "fuzz_keys",
                "creator"
            ]
        }
        try:
            validate(input_json, json_schema)
        except BaseException as err:
            self.__loger.error(err)
            return False
        return True
