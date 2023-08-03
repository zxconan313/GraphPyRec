
"""
with open('D:/Py-Project/ZongXing/source_code_recognize/train_data/final_data3', 'r') as f:
    content = f.read()
    list1 = eval(content)
new_list = list1[-12800:]


with open('D:/Py-Project/ZongXing/source_code_recognize/train_data/test_data', 'a+') as f:
    print('数据集大小为：', len(new_list))
    f.write(str(new_list))"""

import gensim

# 通过模型加载词向量(recommend)
model = gensim.models.FastText.load(r'D:\Py-Project\ZongXing\source_code_recognize\fasttext_test.model')

dic = model.wv.index_to_key
# print(dic)

print(model.wv['-pad-'])