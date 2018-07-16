#-*- coding:utf-8-*-
import requests, json
def evaluate_apisimpl(input_data, model_path,qualified_samples_upload,degraded_samples_upload):
    print('开始检测....')

    user_info = {'input_data': input_data,'model_path':model_path,
                 'qualified_samples_upload':qualified_samples_upload,'degraded_samples_upload':degraded_samples_upload}
    headers = {'content-type': 'application/json'}
    print('evaluate_apisimpl.....')

    r = requests.post("http://127.0.0.1:8081/evaluatecnn", data=json.dumps(user_info), headers=headers)
    print('evaluate_apisimpl.....')
