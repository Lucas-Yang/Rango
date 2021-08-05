from typing import Optional, Any, Mapping
import requests
from requests.structures import CaseInsensitiveDict
from app.common.logger import LogManager


class RequestUtils:

    @staticmethod
    def __safe_req(method: str, url: str, timeout: int, **kwargs) -> Optional[requests.Response]:
        for i in range(3):
            try:
                res = requests.request(method, url, timeout=timeout, **kwargs)
                print(f'{res.status_code};{res.elapsed.total_seconds()}s;{method.upper()}: {url}')
                if res.status_code != 200:
                    raise requests.RequestException()
                return res
            except requests.RequestException:
                print(f'{method.upper()} fails {(i + 1)}: {url}')
        return None

    @staticmethod
    def safe_head(url: str, timeout: int = 10, **kwargs) -> Optional[CaseInsensitiveDict]:
        kwargs.setdefault('allow_redirects', False)
        res = RequestUtils.__safe_req(
            method='head',
            url=url,
            timeout=timeout,
            **kwargs)
        return res.headers if res is not None and res.status_code == 200 else None

    @staticmethod
    def safe_get(url: str, params: Mapping = None, timeout: int = 10, **kwargs) -> Optional[Any]:
        kwargs.setdefault('allow_redirects', True)
        res = RequestUtils.__safe_req(
            method='get',
            url=url,
            params=params,
            timeout=timeout,
            **kwargs)
        LogManager().logger.info(res.json() if res is not None and res.status_code == 200 else "None")
        return res.json() if res is not None and res.status_code == 200 else None

    @staticmethod
    def safe_get_str(url: str, params: Mapping = None, timeout: int = 10, **kwargs) -> Optional[str]:
        kwargs.setdefault('allow_redirects', True)
        res = RequestUtils.__safe_req(
            method='get',
            url=url,
            params=params,
            timeout=timeout,
            **kwargs)
        return res.content.decode(encoding='utf8') if res is not None and res.status_code == 200 else None

    @staticmethod
    def safe_post(url: str, data: Mapping = None, json: Any = None, timeout: int = 10, **kwargs) -> Optional[Any]:
        LogManager().logger.info(json)
        res = RequestUtils.__safe_req(
            method='post',
            url=url,
            data=data,
            json=json,
            timeout=timeout,
            **kwargs
        )
        LogManager().logger.info(res.json() if res is not None and res.status_code == 200 else "None")
        return res.json() if res is not None and res.status_code == 200 else None

    @staticmethod
    def safe_delete(url: str, timeout: int = 10, **kwargs) -> Optional[Any]:
        res = RequestUtils.__safe_req(
            method='delete',
            url=url,
            timeout=timeout,
            **kwargs
        )
        return res.json() if res is not None and res.status_code == 200 else None
