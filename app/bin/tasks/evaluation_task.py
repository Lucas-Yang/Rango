from app.bin.tasks import celery_app
from app.bin.utils.Evaluation import FRVideoEvaluationFactory, NRVideoEvaluationFactory


@celery_app.task
def evaluation_task(task_info_dict: dict):
    """ 评估任务 worker
    :param task_info_dict: {"task_id": xx, task_name: xx, task_type: xx,
                             task_detail:{"index": [psnr, ssim], "index_type": "FR/NR"},
                            "groups": {"1": [xxx.mp4, xxx.mp4], "2": []},
                            "user": xxx
                            }
    :return:
    """

    index_type = task_info_dict.get("task_detail").get("index_type")
    index_list = task_info_dict.get("task_detail").get("index")
    if index_type == "FR":
        for group_id, video_url_list in enumerate(task_info_dict.get("groups")):
            FRVideoHandler = FRVideoEvaluationFactory(src_video_url=video_url_list[0],
                                                      target_video_url=video_url_list[1]
                                                      )
            for index_name in index_list:
                if index_name == "psnr":
                    psnr_res = FRVideoHandler.get_video_psnr()
                elif index_name == "ssim":
                    ssim_res = FRVideoHandler.get_video_ssim()
                elif index_name == "vamf":
                    vamf_res = FRVideoHandler.get_video_vmaf()
                else:
                    continue
    elif index_type == "NR":
        for group_id, video_url_list in enumerate(task_info_dict.get("groups")):
            NRVideoHandler = NRVideoEvaluationFactory(src_video_url=video_url_list[0])
            for index_name in index_list:
                pass
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



