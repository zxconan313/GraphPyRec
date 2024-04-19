# GraphPyRec
This project can target Python implementation code recommendations. The main approach is to achieve complete parsing of contextual semantics by characterizing Python programs as graphs.This README contains two parts, the first part is the main program and how to use the interface; the second part is the description of the relevant data.
## 1.Program
`code2graph__v1.py` is to parse the code into a graph. 
    The input of this is the code base address: `code_path = ''`.
    The output is the graph data storage address: `path2 = ''`.

`model.py` is the network of GGNN and Bert

`main.py` is the main program used to train the code recommendation model, which requires the addresses of the training and test data to be entered. 

```python
train_dataset = myDataset(opt.dataroot, True) 
test_dataset = myDataset(opt.dataroot2, False)
```

## 2.Data
- `Code.zip` contains all the Python used in this article.
- `Data.zip` contains the training and test data used in experiment of this paper.
- `Fasttext.vector` is the set of parameters with the best experimental results for fasttext word embeddings.
