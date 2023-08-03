import torch
from torch.autograd import Variable
import gensim
import numpy as np
from pytorch_pretrained_bert import BertModel, BertTokenizer


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
    # 通过模型加载词向量(recommend)
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


def train(epoch, dataloader, net, criterion, optimizer, opt):
    print("training starting ........")
    token_model = gensim.models.FastText.load(r'E:\python_projects\zongxing\zx1\fasttext_test.model')
    # tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    # bert = BertModel.from_pretrained('bert-base-uncased').cuda()

    net.train()
    total_train_loss = 0

    for i, (adj_matrix, annotation, target, token_list) in enumerate(dataloader, 0):

        net.zero_grad()
        init_input = annotation.reshape(opt.batchSize, 49)
        token = token_embed(token_list, token_model)
        # token = token_bert(token_list, tokenizer, bert)

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

        if opt.debug:
            print("init_input", init_input.size())
            print(init_input)

            print("annotation:", annotation.size())
            print(annotation)

            print("output", output.size())
            print(output)

        loss = criterion(output, target)
        total_train_loss += loss

        loss.backward()
        optimizer.step()

        if i % int(len(dataloader) / 10) == 0 and opt.verbal:
            print('[%d/%d][%d/%d] Loss: %.4f' % (epoch, opt.niter, i, len(dataloader), loss.item()))
    print('total_train_loss:',total_train_loss)
