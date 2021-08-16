"""
tagging异步任务
"""

from app.bin.tasks import celery_app
from app.bin.utils.Evaluation import FRVideoEvaluationFactory, NRVideoEvaluationFactory
from app.bin.model import VideoEvaluationNRIndex, VideoEvaluationType


@celery_app.task
def evaluation_task(task_id):
    """ 评估任务 worker
    :task_id: 任务id
    task_info_json: {"task_id": xx, "task_name": xx, "task_type": xx,
                             "task_detail":{"index": [psnr, ssim], "index_type": "FR/NR"},
                            "groups": {"1": [xxx.mp4, xxx.mp4], "2": []},
                            "user": xxx
                            }
    :return:
    """
    # 根据task_id 获取 完整的task_info
    task_info_dict = task_info_json
    index_type = task_info_dict.get("task_details", {}).get("index_type")
    index_list = task_info_dict.get("task_detail", {}).get("index")
    if index_type == VideoEvaluationType.FR.value:
        for group_id, video_url_list in enumerate(task_info_dict.get("groups")):
            FRVideoHandler = FRVideoEvaluationFactory(src_video_url=video_url_list[0],
                                                      target_video_url=video_url_list[1]
                                                      )
            for index_name in index_list:
                if index_name == "PSNR":
                    psnr_res = FRVideoHandler.get_video_psnr()
                elif index_name == "SSIM":
                    ssim_res = FRVideoHandler.get_video_ssim()
                elif index_name == "VMAF":
                    vmaf_res = FRVideoHandler.get_video_vmaf()
                else:
                    continue
        # write data to db

    elif index_type == VideoEvaluationType.NR.value:
        for group_id, video_url_list in enumerate(task_info_dict.get("groups")):
            NRVideoHandler = NRVideoEvaluationFactory(src_video_url=video_url_list[0])
            for index_name in index_list:
                if index_name == "DEFINITION":
                    NRVideoHandler.get_video_clarity()
                elif index_name == "NIQE":
                    NRVideoHandler.get_video_NIQE()
                else:
                    continue
        # write data to db

    else:
        pass


@celery_app.task
def test_task(x, y):
    """
    :return:
    """
    return x + y


if __name__ == '__main__':
    celery_app.worker_main()



