from torch.utils.data import DataLoader


class myDataloader(DataLoader):

    def __init__(self, *args, **kwargs):
        super(myDataloader, self).__init__(*args, **kwargs)
