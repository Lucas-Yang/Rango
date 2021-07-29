""" 自动评估 组件
"""


class FRVideoEvaluationFactory(object):
    """ 全参考视频质量评估
    """
    def __init__(self, src_video_url: str, target_video_url: str):
        """
        """
        self.__src_video_url = src_video_url
        self.__target_video_url = target_video_url
        self.__src_video_path = self.__video_download()
        self.__target_video_path = self.__video_download()

    def __video_download(self):
        """
        :return:
        """
        return ""

    def get_video_psnr(self):
        """
        :return:
        """

    def get_video_ssim(self):
        """
        :return:
        """

    def get_video_vmaf(self):
        """
        :return:
        """


class NRVideoEvaluationFactory(object):
    """ 无参考视频质量评估
    """
    def __init__(self, src_video_url: str, target_video_url: str=None):
        """
        """
        self.__video_url = src_video_url

        self.__video_local_path = self.__video_download()

    def __video_download(self):
        """
        :return:
        """
        return ""

    def get_video_clarity(self):
        """ 获取视频清晰度评分
        :return:
        """

    def get_video_NIQE(self):
        """ 获取视频niqe评分
        :return:
        """

    def get_video_black_frame(self):
        """ 视频黑屏检测
        :return:
        """

    def get_video_silence_time(self):
        """ 视频静音检测
        :return:
        """

    def get_video_freeze_time(self):
        """ 视频卡顿检测
        :return:
        """

    def get_video_blurred_frame(self):
        """ 视频花屏检测
        :return:
        """


