# Transformer-based Argument Mining

In this repository you find the code which was used for the experiments in our paper [Transformer-based Argument Mining for Healthcare Applications](https://hal.archives-ouvertes.fr/hal-02879293/document) (ECAI 2020).

In our work, we evaluate various transformer models for 
1) Argument Component Detection (Sequence Tagging Task), and
2) Argument Relation Classification (Sequence Classification Task)

on clinical trials.

# Requirements/Setup
The code runs under Python 3.6 or higher. The required packages are listed in the requirements.txt, which can be directly installed from the file:

```
pip install -r /path/to/requirements.txt
```

Our code is based on the transformer library version 2.3.0. See https://github.com/huggingface/transformers for more details.


# Usage

To fine-tune a transformer model, execute the following script. Models, tasks and hyper-parameters can be specified within the script.

```
sh run_train.sh
```



Evaluation can be done in a similar fashion by running the script below. Trained models, tasks and the testset can be changed in the script. 

```
sh run_evaluate.sh
```


# Data
The experiments in the paper are based on our AbstRCT corpus, which can be found [here](https://gitlab.com/tomaye/abstrct).
For the argument component detection the data has to be in the CoNLL format.
Relation classification requires the data to be in a tsv format. For converting Brat annotation files into tsv format, see [create_tsv_from_brat.py](/preprocessing/create_tsv_from_brat.py). 
 
 # Citation
If you use our code or would like to refer to it, please cite the following paper: 
>Tobias Mayer, Elena Cabrio and Serena Villata (2020),
[Transformer-based Argument Mining for Healthcare Applications](https://hal.archives-ouvertes.fr/hal-02879293/document).
In Proceedings of the 24th European Conference on Artificial Intelligence (ECAI 2020), Santiago de Compostela, Spain.
