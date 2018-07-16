import requests, json
def train_apisimpl(input_data, learning_rate,steps, model_path, validation_percentage,
                   test_percentage,batch,optimizer):
    print('train_apisimpl.....')
    user_info = {'input_data': input_data,'learning_rate':learning_rate,'steps':steps,'model_path':model_path,
                 'validation_percentage':validation_percentage,'test_percentage':test_percentage,'batch':batch,'optimizer':optimizer}
    headers = {'content-type': 'application/json'}
    print('train_apisimpl.....')
    r = requests.post("http://127.0.0.1:5000/traincnn", data=json.dumps(user_info), headers=headers)
    print('train_apisimpl.....')
