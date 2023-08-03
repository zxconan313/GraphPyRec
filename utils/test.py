import torch
from torch.autograd import Variable
import gensim
import numpy as np
from pytorch_pretrained_bert import BertModel, BertTokenizer


def MRR(indices, target):
    indices_list = indices.tolist()
    target_list = target.tolist()
    rank_list = []
    for i in range(len(indices_list)):
        target = target_list[i]
        indices_i = indices_list[i]
        if target in indices_i:
            kk = indices_i.index(target)
            ss = 1 / (kk + 1)
            rank_list.append(ss)
    mean = round(sum(rank_list) / len(target_list), 3)
    return mean


def token_embed(token_list, token_model):
    list1 = []
    # 通过模型加载词向量(recommend)
    for line in token_list:
        list2 = []
        for tt in line:
            num1 = token_model.wv[tt]
            list2.append(num1.astype(float))
        list1.append(list2)
    aa = np.array(list1)
    aa = np.transpose(aa, [1, 0, 2])
    return aa


def token_bert(token_list, tokenizer, bert):
    #
    token = torch.Tensor([])
    token = token.cuda()
    for i in range(len(token_list[0])):
        COLUMN = [column[i] for column in token_list]
        tokens = tokenizer.tokenize(str(COLUMN))
        tokens = ["[CLS]"] + tokens + ["[SEP]"]
        ids = torch.tensor([tokenizer.convert_tokens_to_ids(tokens)])
        ids = ids.cuda()
        _, unit_token = bert(ids, output_all_encoded_layers=False)
        token = torch.cat([token, unit_token])
    return token.reshape(64, 1, 768).type(torch.float64)


def sum_error(tensor1, tensor2, list1):
    """
    :param tensor1: 预测结果：128*119
    :param tensor2: 目标：128*1
    :param list1: 错误分类的整合列表
    :return: list1
    """
    _, indices = tensor1.topk(1, dim=1, largest=True, sorted=True)
    # print(indices)
    p_list = indices.cpu().numpy().tolist()
    # print(p_list, type(p_list))
    y_list = tensor2.cpu().numpy().tolist()
    # print(y_list, type(y_list))
    for i in range(len(y_list)):
        if p_list[i][0] != y_list[i]:
            list1.append(y_list[i])
    # print(list1)


def test(dataloader, net, criterion, optimizer, opt):
    test_loss = 0
    error = []
    total = []
    correct, correct5, correct10 = 0, 0, 0
    mrr = 0
    token_model = gensim.models.FastText.load(r'E:\python_projects\zongxing\zx1\fasttext_test.model')
    # tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    # bert = BertModel.from_pretrained('bert-base-uncased').cuda()

    predict = []

    net.eval()
    for i, (adj_matrix, annotation, target, token_list) in enumerate(dataloader, 0):

        t1 = target.numpy().tolist()
        token = token_embed(token_list, token_model)
        # token = token_bert(token_list, tokenizer, bert)
        for n in t1:
            total.append(n)
        init_input = annotation.reshape(opt.batchSize, 49)
        if opt.cuda:
            init_input = init_input.cuda()
            adj_matrix = adj_matrix.cuda()
            annotation = annotation.cuda()
            target = target.cuda()
            token = torch.tensor(token).cuda()
            # token = token.cuda()

        init_input = Variable(init_input)
        adj_matrix = Variable(adj_matrix)
        annotation = Variable(annotation)
        target = Variable(target)
        token = Variable(token)

        output = net(init_input, annotation, adj_matrix, token)
        test_loss += criterion(output, target).item()

        sum_error(output, target, error)

        pred = output.data.max(1, keepdim=True)[1]
        correct += pred.eq(target.data.view_as(pred)).cpu().sum()

        target_resize = target.view(-1, 1)  # top5和top10
        _, pred_5 = output.topk(5, dim=1, largest=True, sorted=True)
        correct5 += torch.eq(pred_5, target_resize).sum().float().item()
        _, pred_10 = output.topk(10, dim=1, largest=True, sorted=True)
        correct10 += torch.eq(pred_10, target_resize).sum().float().item()

        mrr_i = MRR(pred_10, target)
        # print(mrr_i)
        mrr += mrr_i

        predict_temp = pred_10.tolist()
        predict.append(predict_temp)
    test_loss /= len(dataloader.dataset)
    print(
        'Test set: Average loss: {:.14f}, Accuracy: {}/{} ({:.2f}%) top5: ({:.2f}%) top10: ({:.2f}%) MRR:({:.3f})'.format(
            test_loss, correct, len(dataloader.dataset), 100. * correct / len(dataloader.dataset),
                                                         100. * correct5 / len(dataloader.dataset),
                                                         100. * correct10 / len(dataloader.dataset),
                                                         mrr  / 200))
    """acc = 100. * correct / len(dataloader.dataset)
    if acc > 63.5:
        print("正在储存预测结果")
        with open('./predict_result.txt', 'a+') as fr:
            fr.write(str(acc))
            fr.write(str(predict))"""
    return test_loss, correct, len(dataloader.dataset)
