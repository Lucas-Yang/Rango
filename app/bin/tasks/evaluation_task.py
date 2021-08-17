"""
evaluation 异步任务
"""
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
    groups_result_dict = {}
    if index_type == VideoEvaluationType.FR.value:
        for group_id, video_url_list in enumerate(task_info_dict.get("groups")):
            FRVideoHandler = FRVideoEvaluationFactory(src_video_url=video_url_list[0],
                                                      target_video_url=video_url_list[1]
                                                      )
            group_result_dict = {}
            for index_name in index_list:
                if index_name == VideoEvaluationFRIndex.PSNR.value:
                    psnr_res = FRVideoHandler.get_video_psnr()
                    group_result_dict[VideoEvaluationFRIndex.PSNR.name] = psnr_res
                elif index_name == VideoEvaluationFRIndex.SSIM.value:
                    ssim_res = FRVideoHandler.get_video_ssim()
                    group_result_dict[VideoEvaluationFRIndex.SSIM.name] = ssim_res
                elif index_name == VideoEvaluationFRIndex.VMAF.value:
                    vmaf_res = FRVideoHandler.get_video_vmaf()
                    group_result_dict[VideoEvaluationFRIndex.VMAF.name] = vmaf_res
                else:
                    continue
            groups_result_dict[group_id] = group_result_dict
    elif index_type == VideoEvaluationType.NR.value:
        for group_id, video_url_list in enumerate(task_info_dict.get("groups")):
            group_result_dict = {}
            NRVideoHandler = NRVideoEvaluationFactory(src_video_url=video_url_list[0])
            for index_name in index_list:
                if index_name == VideoEvaluationNRIndex.DEFINITION.value:
                    definition_res = NRVideoHandler.get_video_clarity()
                    group_result_dict[VideoEvaluationNRIndex.DEFINITION.name] = definition_res
                elif index_name == VideoEvaluationNRIndex.NIQE.value:
                    niqe_res = NRVideoHandler.get_video_NIQE()
                    group_result_dict[VideoEvaluationNRIndex.NIQE.name] = niqe_res
                elif index_name == VideoEvaluationNRIndex.BRISQUE.value:
                    brisque_res = NRVideoHandler.get_video_brisque()
                    group_result_dict[VideoEvaluationNRIndex.BRISQUE.name] = brisque_res
                else:
                    continue
            groups_result_dict[group_id] = group_result_dict
    else:
        pass
    task_result_dict["task_evaluation_result"] = groups_result_dict
    task_result_dict["user"] = task_user
    print(task_result_dict)
    result_collection = db["rango_evaluation_task_result"]
    result_collection.insert_one(task_result_dict)


@celery_app.task
def test_task(x, y):
    """
    :return:
    """
    return x + y


if __name__ == '__main__':
    evaluation_task("1234")



