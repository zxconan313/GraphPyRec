import argparse
import random
import time

import torch
import torch.nn as nn
import torch.optim as optim

from model import GGNN
from utils.train import train
from utils.test import test
from utils.data.dataset import myDataset
from utils.data.dataloader import myDataloader

parser = argparse.ArgumentParser()
parser.add_argument('--workers', type=int, help='number of data loading workers', default=2)
parser.add_argument('--batchSize', type=int, default=64, help='input batch size')
parser.add_argument('--state_dim', type=int, default=64, help='GGNN hidden state size')
parser.add_argument('--n_steps', type=int, default=1, help='propogation steps number of GGNN')
parser.add_argument('--niter', type=int, default=20, help='number of epochs to train for')
parser.add_argument('--lr', type=float, default=0.01, help='learning rate')
parser.add_argument('--cuda', default='True', action='store_true', help='enables cuda')
parser.add_argument('--verbal', default='True', action='store_true', help='print training info or not')
parser.add_argument('--manualSeed', type=int, help='manual seed')
parser.add_argument('--debug', action='store_true', help='print debug')

opt = parser.parse_args()
# print(opt)

if opt.manualSeed is None:
    opt.manualSeed = random.randint(1, 10000)
# print("Random Seed: ", opt.manualSeed)
random.seed(opt.manualSeed)
torch.manual_seed(opt.manualSeed)

opt.dataroot = r'E:\python_projects\zongxing\zx1\data\rem2_data_10.31'
opt.dataroot2 = r'E:\python_projects\zongxing\zx1\data\rem2_data_10.31'

if opt.cuda:
    torch.cuda.manual_seed_all(opt.manualSeed)


def main(opt):

    train_dataset = myDataset(opt.dataroot, True)
    train_dataloader = myDataloader(train_dataset, batch_size=opt.batchSize, shuffle=True, num_workers=2)

    test_dataset = myDataset(opt.dataroot2, False)
    test_dataloader = myDataloader(test_dataset, batch_size=opt.batchSize, shuffle=False, num_workers=2)

    opt.annotation_dim = 1
    opt.n_edge_types = train_dataset.n_edge_types
    opt.n_node = train_dataset.n_node

    net = GGNN(opt)
    net.double()
    print(net)

    criterion = nn.CrossEntropyLoss()

    if opt.cuda:
        net.cuda()
        criterion.cuda()

    optimizer = optim.Adam(net.parameters(), lr=opt.lr)

    for epoch in range(0, opt.niter):
        train(epoch, train_dataloader, net, criterion, optimizer, opt)
        start_time = time.time()  # 程序开始时间
        test(test_dataloader, net, criterion, optimizer, opt)
        end_time = time.time()  # 程序结束时间
        run_time = end_time - start_time  # 程序的运行时间，单位为秒
        print(run_time)


if __name__ == "__main__":
    main(opt)
