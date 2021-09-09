"""
evaluation 异步任务
"""
import os

from app.bin.tasks import celery_app
from app.bin.utils.Evaluation import FRVideoEvaluationFactory, NRVideoEvaluationFactory
from app.bin.model import VideoEvaluationNRIndex, VideoEvaluationFRIndex, VideoEvaluationType
from app.common import mongodb_client


@celery_app.task
def evaluation_task(task_id):
    """ 评估任务 worker
    :task_id: 任务id
    task_info_json: {"task_id": xx,
                     "task_name": xx,
                     "task_type": xx,
                     "task_detail":{"index": [psnr, ssim],
                                    "index_type": "FR/NR"
                                    },
                     "groups": {"1": [xxx.mp4, xxx.mp4], "2": []},
                     "user": xxx
                    }
    :return:
    """
    task_info_dict = {}
    task_result_dict = {"task_id": task_id, "task_evaluation_result": {}}
    db = mongodb_client
    collection = db['rango_evaluate_tasks']

    task_info_iter = collection.find({'task_id': task_id})
    for data in task_info_iter:
        task_info_dict = data
    index_type = task_info_dict.get("task_detail", {}).get("index_type", None)
    index_list = task_info_dict.get("task_detail", {}).get("index", None)
    task_user = task_info_dict.get("user", None)
    task_result_dict["index_type"] = index_type
    groups_result_dict = {}
    if index_type == VideoEvaluationType.FR.value:
        for group_id, video_url_list in task_info_dict.get("groups").items():
            FRVideoHandler = FRVideoEvaluationFactory(src_video_url=video_url_list[0],
                                                      target_video_url=video_url_list[1]
                                                      )
            group_result_dict = {}
            for index_name in index_list:
                if index_name == VideoEvaluationFRIndex.PSNR.value:
                    try:
                        psnr_res = FRVideoHandler.get_video_psnr()
                    except Exception as err:
                        psnr_res = {"runtime error": str(err)}
                    group_result_dict[VideoEvaluationFRIndex.PSNR.name] = psnr_res
                elif index_name == VideoEvaluationFRIndex.SSIM.value:
                    try:
                        ssim_res = FRVideoHandler.get_video_ssim()
                    except Exception as err:
                        ssim_res = {"runtime error": str(err)}
                    group_result_dict[VideoEvaluationFRIndex.SSIM.name] = ssim_res
                elif index_name == VideoEvaluationFRIndex.VMAF.value:
                    try:
                        vmaf_res = FRVideoHandler.get_video_vmaf()
                    except Exception as err:
                        vmaf_res = {"runtime error": str(err)}
                    group_result_dict[VideoEvaluationFRIndex.VMAF.name] = vmaf_res
                else:
                    continue
            os.remove(FRVideoHandler.src_video_path)
            os.remove(FRVideoHandler.target_video_path)
            groups_result_dict[group_id] = group_result_dict
    elif index_type == VideoEvaluationType.NR.value:
        for group_id, video_url_list in task_info_dict.get("groups").items():
            group_result_dict = {}
            NRVideoHandler = NRVideoEvaluationFactory(src_video_url=video_url_list[0])
            for index_name in index_list:
                if index_name == VideoEvaluationNRIndex.DEFINITION.value:
                    try:
                        definition_res = NRVideoHandler.get_video_clarity()
                    except Exception as err:
                        definition_res = {"runtime error": str(err)}
                    group_result_dict[VideoEvaluationNRIndex.DEFINITION.name] = definition_res
                elif index_name == VideoEvaluationNRIndex.NIQE.value:
                    try:
                        niqe_res = NRVideoHandler.get_video_niqe()
                    except Exception as err:
                        niqe_res = {"runtime error": str(err)}
                    group_result_dict[VideoEvaluationNRIndex.NIQE.name] = niqe_res
                elif index_name == VideoEvaluationNRIndex.BRISQUE.value:
                    try:
                        brisque_res = NRVideoHandler.get_video_brisque()
                    except Exception as err:
                        brisque_res = {"runtime error": str(err)}
                    group_result_dict[VideoEvaluationNRIndex.BRISQUE.name] = brisque_res
                else:
                    continue
            os.remove(NRVideoHandler.video_local_path)
            groups_result_dict[group_id] = group_result_dict
    else:
        pass
    task_result_dict["task_evaluation_result"] = groups_result_dict
    task_result_dict["user"] = task_user
    result_collection = db["rango_evaluation_task_result"]
    result_collection.insert_one(task_result_dict)


@celery_app.task
def test_task(x, y):
    """
    :return:
    """
    return x + y


if __name__ == '__main__':
    evaluation_task("luka-test1")



