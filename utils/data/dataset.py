import numpy as np


def load_data_from_file(path):
    with open(path, 'r') as f:
        content = f.read()
        data_list = eval(content)
    return data_list


def find_max_edge_id(data_list):
    max_edge_id = 0
    for data in data_list:
        edges = data[0]
        for item in edges:
            if item[1] > max_edge_id:
                max_edge_id = item[1]
    return max_edge_id


def find_max_node_id(data_list):
    max_node_id = 0
    for data in data_list:
        edges = data[0]
        for item in edges:
            if item[0] > max_node_id:
                max_node_id = item[0]
            if item[2] > max_node_id:
                max_node_id = item[2]
    return max_node_id


def create_adjacency_matrix(edges, n_nodes, n_edge_types):
    a = np.zeros([n_nodes, n_nodes * n_edge_types * 2])
    for edge in edges:
        src_idx = edge[0]
        e_type = edge[1]
        tgt_idx = edge[2]
        if e_type == 4:
            e_type = 2
        a[tgt_idx - 1][(e_type - 1) * n_nodes + src_idx - 1] = 1
        a[src_idx - 1][(e_type - 1 + n_edge_types) * n_nodes + tgt_idx - 1] = 1
    return a


def data_convert(data_list, annotation_dim):
    n_nodes = 10
    data = []
    for item in data_list:
        edge_list = item[0]
        node_list = item[1]
        annotation = np.zeros([n_nodes, annotation_dim])
        for i in range(len(node_list)):
            annotation[i][0] = node_list[i]
        target = item[2][0]
        token = item[3]
        data.append([edge_list, annotation, target, token])
    return data


def split_set(data_list, train_size):
    n_examples = len(data_list)
    idx = range(n_examples)
    train = idx[:train_size]
    val = idx[-12800:]
    return np.array(data_list, dtype=object)[train], np.array(data_list, dtype=object)[val]


class myDataset:
    def __init__(self, path, is_train, train_size=128000):
        print("loading data from graph .......")
        all_data = load_data_from_file(path)
        all_data = all_data[:140800]
        print("constracting dataset ......")
        self.n_edge_types = 4
        self.n_node = 49

        train_data, val_data = split_set(all_data, train_size)
        print("train_size:", train_data.shape)
        print("val_size:", val_data.shape)
        if is_train:
            self.data = data_convert(train_data, 1)
            # print(self.data)
        else:
            self.data = data_convert(val_data, 1)

    def __getitem__(self, index):
        am = create_adjacency_matrix(self.data[index][0], self.n_node, self.n_edge_types)
        annotation = self.data[index][1]
        target = self.data[index][2]
        token = self.data[index][3]

        return am, annotation, target, token

    def __len__(self):
        return len(self.data)
