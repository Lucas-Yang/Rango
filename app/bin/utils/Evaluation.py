""" 自动评估 组件
"""
import io
import json
import os
import time
import cv2
from typing import Optional
import requests
from app.bin.utils.request_utils import RequestUtils
from app.common.boss import Boss
from app.common.logger import LogManager


class FRVideoEvaluationFactory(object):
    """ 全参考视频质量评估
    """

    def __init__(self, src_video_url: str, target_video_url: str):
        """
        """
        self.__src_video_url = src_video_url
        self.__target_video_url = target_video_url
        self.__src_video_path = self.__src_video_download()
        self.__target_video_path = self.__target_video_download()
        self.logger = LogManager().logger

    def __src_video_download(self):
        """
        :return:
        """
        video_path = os.getcwd()
        video_name = self.__src_video_url.split('/')[-1]
        response = requests.get(self.__src_video_url, stream=True)
        if response.status_code != 200:
            self.logger.error('video download error!')
            return '视频下载出错！'
        with open(video_path + video_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
        return video_path + video_name

    def __target_video_download(self):
        """
        :return:
        """
        video_path = os.getcwd()
        video_name = self.__target_video_url.split('/')[-1]
        response = requests.get(self.__target_video_url, stream=True)
        if response.status_code != 200:
            self.logger.error('video download error!')
            return '视频下载出错！'
        with open(video_path + video_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
        return video_path + video_name

    def get_video_psnr(self):
        """
        :return:
        """
        self.logger.info("Start video psnr detect...")
        try:
            url = "http://hassan.bilibili.co/player/video/psnr1"
            files = [
                ('file_input', open(self.__src_video_path, 'rb')),
                ('file_refer', open(self.__target_video_path, 'rb'))
            ]
            response = requests.post(url=url, files=files)
            os.remove(self.__src_video_path)
            os.remove(self.__target_video_path)
            if response.status_code == 200:
                return json.dumps({"data": {"psnr_score": response.json()["data"]["psnr_score"]}}, ensure_ascii=False)
            else:
                raise RuntimeError("hassan服务返回出错")
        except Exception as e:
            self.logger.error(str(e))
            return json.dumps({"data": {"description": "psnr检测出现错误！"}}, ensure_ascii=False)

    def get_video_ssim(self):
        """
        :return:
        """
        self.logger.info("Start video ssim detect...")
        try:
            url = "http://hassan.bilibili.co/player/video/ssim"
            files = [
                ('file_src', open(self.__src_video_path, 'rb')),
                ('file_target', open(self.__target_video_path, 'rb'))
            ]
            response = requests.post(url=url, files=files)
            os.remove(self.__src_video_path)
            os.remove(self.__target_video_path)
            if response.status_code == 200:
                return json.dumps({"data": {"ssim_score": response.json()["data"]["ssim_score"]}}, ensure_ascii=False)
            else:
                raise RuntimeError("hassan服务返回出错")
        except Exception as e:
            self.logger.error(str(e))
            return json.dumps({"data": {"description": "ssim检测出现错误！"}}, ensure_ascii=False)

    def get_video_vmaf(self):
        """
        :return:
        """
        self.logger.info("Start video vmaf detect...")
        try:
            url = "http://hassan.bilibili.co/player/video/vmaf"
            files = [
                ('file_input', open(self.__src_video_path, 'rb')),
                ('file_refer', open(self.__target_video_path, 'rb'))
            ]
            response = requests.post(url=url, files=files)
            os.remove(self.__src_video_path)
            os.remove(self.__target_video_path)
            if response.status_code == 200:
                return json.dumps({"data": {"vmaf_score": response.json()["data"]["vmaf_score"]}}, ensure_ascii=False)
            else:
                raise RuntimeError("hassan服务返回出错")
        except Exception as e:
            self.logger.error(str(e))
            return json.dumps({"data": {"description": "vmaf检测出现错误！"}}, ensure_ascii=False)


class NRVideoEvaluationFactory(object):
    """ 无参考视频质量评估
    """

    def __init__(self, src_video_url: str, index_types: str = ""):
        """
        """
        self.__video_url = src_video_url
        self.__video_local_path = self.__video_download()
        self.index_types = index_types
        self.task_id = "-1"
        self.logger = LogManager().logger

    def __video_download(self):
        """
        :return:
        """
        video_path = os.getcwd()
        video_name = self.__video_url.split('/')[-1]
        response = requests.get(self.__video_url, stream=True)
        if response.status_code != 200:
            self.logger.error('video download error!')
            return '视频下载出错！'
        with open(video_path + video_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
        return video_path + video_name

    def get_video_clarity(self):
        """ 获取视频清晰度评分
        :return:
        """
        try:
            self.logger.info("Start clarity debug...")
            # 将视频切帧
            img_list = self.video2frame()
            url = "http://hassan.bilibili.co/image/quality/clarity-detect"
            count = 0
            sum_score = 0
            for i in range(len(img_list)):
                try:
                    success, encoded_image = cv2.imencode('.jpg', img_list[i])  # 对数组的图片格式进行编码
                    img_bytes = encoded_image.tobytes()  # 将数组转为bytes用于传输
                    files = [('file', ('file.jpg', img_bytes, 'image/jpg'))]
                    response = RequestUtils.safe_post(url=url, files=files)
                    sum_score += response['data']['judge']
                    count += 1
                except Exception as e:
                    self.logger.error(str(e))
            os.remove(self.__video_local_path)
            if count == 0:
                raise RuntimeError("清晰度检测出现错误！")
            avg_score = sum_score / count
            is_clear = "不清晰"
            avg_score *= 10
            if 0.5 <= avg_score < 0.7:
                is_clear = "较不清晰"
            elif 0.7 <= avg_score < 0.8:
                is_clear = "较清晰"
            elif avg_score >= 0.8:
                is_clear = "清晰"
            return json.dumps({"data": {"is_clear": is_clear, "clarity_score": avg_score}}, ensure_ascii=False)
        except Exception as e:
            self.logger.error(str(e))
            return json.dumps({"data": {"description": "清晰度检测出现错误！"}}, ensure_ascii=False)

    def get_video_NIQE(self):
        """ 获取视频niqe评分
        该功能不能传入时长过长的视频，否则会响应超时
        :return:
        """
        try:
            self.logger.info("Start video niqe detect...")
            url = "http://hassan.bilibili.co/player/video/niqe"
            files = [('file_input', open(self.__video_local_path, 'rb'))]
            response = requests.post(url=url, files=files)
            if response.status_code == 200:
                return json.dumps({"data": {"niqe_score": response.json()["data"]["niqe_score"]}}, ensure_ascii=False)
            else:
                raise RuntimeError("hassan服务返回出错，视频时长可能过长")
        except Exception as e:
            self.logger.error(str(e))
            return json.dumps({"data": {"description": "niqe检测出现错误！"}}, ensure_ascii=False)

    def get_video_black_frame(self, black_threshold=0.999):
        """ 视频黑屏检测
        :return:
        """
        try:
            self.logger.info("Start black frame detect...")
            self.index_types = "BLACKFRAME"
            self.task_id = self.upload(black_threshold)
            black_frame = self.poll_for_detect()
            is_black = "是" if len(black_frame) > 0 else "否"
            if os.path.isfile(self.__video_local_path):
                os.remove(self.__video_local_path)
            return json.dumps({"data": {"is_black": is_black, "black_frame_info": black_frame}}, ensure_ascii=False)
        except Exception as e:
            if os.path.isfile(self.__video_local_path):
                os.remove(self.__video_local_path)
            self.logger.error(str(e))
            return json.dumps({"data": {"description": "黑屏检测出现错误！"}}, ensure_ascii=False)

    def get_video_silence_time(self, is_whole: bool = True):
        """ 视频静音检测
        :return:
        """
        try:
            self.logger.info("Start silence detect...")
            url = "http://hassan.bilibili.co/player/index/silence"
            files = [('file_src', open(self.__video_local_path, 'rb'))]
            response = RequestUtils.safe_post(url=url, files=files)
            os.remove(self.__video_local_path)
            if response and response["code"] == 0:
                silent_frame = response["data"]["silence_timestamps"]
                if is_whole is False:
                    return {"silent_info": silent_frame}
                total_duration = self.get_video_duration()
                is_silent = "否"
                if len(silent_frame) == 1:
                    silence_duration = silent_frame[0]['silence_duration']
                    if 2 >= silence_duration - total_duration >= -2:
                        is_silent = "是"
                if is_silent == "是":
                    return json.dumps({"data": {"is_silent": is_silent, "silent_info": silent_frame}}, ensure_ascii=False)
                else:
                    return json.dumps({"data": {"is_silent": is_silent, "silent_info": []}}, ensure_ascii=False)
            else:
                raise RuntimeError("视音频解析出错")
        except Exception as e:
            self.logger.error(str(e))
            return json.dumps({"data": {"description": "静音检测出现错误！"}}, ensure_ascii=False)

    def get_video_freeze_time(self):
        """ 视频卡顿检测
        :return:
        """
        try:
            self.logger.info("Start freeze frame detect...")
            self.index_types = "FREEZEFRAME"
            self.task_id = self.upload()
            freeze_frame = self.poll_for_detect()
            is_freeze = "是" if len(freeze_frame) > 0 else "否"
            if os.path.isfile(self.__video_local_path):
                os.remove(self.__video_local_path)
            return json.dumps({"data": {"is_freeze": is_freeze, "freeze_frame_info": freeze_frame}}, ensure_ascii=False)
        except Exception as e:
            if os.path.isfile(self.__video_local_path):
                os.remove(self.__video_local_path)
            self.logger.error(str(e))
            return json.dumps({"data": {"description": "卡顿检测出现错误！"}}, ensure_ascii=False)

    def get_video_blurred_frame(self):
        """ 视频花屏检测
        :return:
        """
        blurred_image_list = []
        upload_boss = Boss()
        try:
            self.logger.info("Start blurred debug...")
            # 将视频切帧
            img_list = self.video2frame()
            url = "http://hassan.bilibili.co/image/quality/blurred-detect"
            for i in range(len(img_list)):
                try:
                    success, encoded_image = cv2.imencode('.jpg', img_list[i])  # 对数组的图片格式进行编码
                    img_bytes = encoded_image.tobytes()  # 将数组转为bytes用于传输
                    files = [('file', ('file.jpg', img_bytes, 'image/jpg'))]
                    response = RequestUtils.safe_post(url=url, files=files)
                    if response['data']['judge']:
                        file_content = io.BytesIO(img_bytes)
                        img_url = upload_boss.upload_data(file_content, str(i) + '.jpg')
                        blurred_image_list.append(img_url)
                except Exception as e:
                    self.logger.error(str(e))
            os.remove(self.__video_local_path)
            del upload_boss
            return json.dumps({"data": {"blurred_image_list": blurred_image_list}}, ensure_ascii=False)
        except Exception as e:
            self.logger.error(str(e))
            return json.dumps({"data": {"description": "花屏检测出现错误！"}}, ensure_ascii=False)

    def upload(self, black_threshold=0.999) -> Optional[str]:
        """
        upload video
        """
        self.logger.info("Start uploading video...")
        url = "http://hassan.bilibili.co/player/video/upload"
        payload = {
            'index_types': self.index_types,
            'black_threshold': black_threshold
        }
        files = [
            ('file', open(self.__video_local_path, 'rb'))
        ]

        response = RequestUtils.safe_post(url=url, data=payload, files=files)
        if response["code"] == -1:
            self.logger.error("Status code of uploader is 1!")
            raise RuntimeError("视频上传状态码为1！")
        else:
            self.task_id = response["task_id"]
        self.logger.info("Upload over")
        return self.task_id

    def poll_for_detect(self):
        """
        图像检测的poll方法
        """
        ctr = 0
        while True:
            ctr += 1
            self.logger.info("Request for %d times..." % ctr)
            url = "http://hassan.bilibili.co/player/index/cv?task_id=%s" % self.task_id
            response = RequestUtils.safe_get(url=url)

            self.logger.info("==debug-response:self.task_id:{0}==response:{1}".format(self.task_id, response))
            if response["code"] != -4:
                if self.index_types == "FREEZEFRAME":
                    return response["data"]["freeze_frame_list"]
                elif self.index_types == "BLACKFRAME":
                    return response["data"]["black_frame_list"]
                elif self.index_types == "FIRSTFRAME":
                    return response["data"]["first_frame_time"]
            # 超过120秒视为超时
            if ctr > 120:
                raise TimeoutError("Time out")
            time.sleep(10)

    def video2frame(self):
        """
        将视频按固定时长切帧
        :return: 返回切帧之后的数据
        """
        image_list = []
        vc = cv2.VideoCapture(self.__video_local_path)
        total_frames = vc.get(cv2.CAP_PROP_FRAME_COUNT)
        interval = total_frames / 20  # 按照一定间隔将视频20等分，切成20张图片
        for i in range(20):
            vc.set(cv2.CAP_PROP_POS_FRAMES, i * interval)
            success, image = vc.read()
            image_list.append(image)
        return image_list

    def get_video_duration(self):
        """
        获取视频的总时长
        """
        cap = cv2.VideoCapture(self.__video_local_path)
        rate = cap.get(5)  # 帧速率
        FrameNumber = cap.get(7)  # 视频文件的帧数
        duration = FrameNumber / rate
        return duration


if __name__ == '__main__':
    # fr = FRVideoEvaluationFactory('http://uat-boss.bilibili.co/ep_misc/4948b955c724f3b4aa153bd5c83836d29da4d48c.mp4',
    #                               'http://uat-boss.bilibili.co/ep_misc/c0bb1c645dfae20e874a409432efaec6788f6bf2.mp4')
    # print(fr.get_video_vmaf())
    nr = NRVideoEvaluationFactory('http://uat-boss.bilibili.co/ep_misc/4948b955c724f3b4aa153bd5c83836d29da4d48c.mp4')
    print(nr.get_video_blurred_frame())