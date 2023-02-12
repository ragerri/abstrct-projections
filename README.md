# antidote-projections
This repository contains a medical corpus of argument mining [AbstRCT corpus](https://gitlab.com/tomaye/abstrct) (a dataset of clinical abstracts annotated for argument mining in English), and generation of the dataset in Spanish by translation and projection using word alignment tools, such as Awesome align and Simalign. 

Consider running `pip install requirements.txt` before running the scripts below.

Table of contents:

- [Data](#data)
- [Translation](#translation)
- [Projection and correction](#projection-and-correction)
- [Compare](#compare)
- [Argument Mining](#argument-mining)


# Data

The dataset consists of abstracts of 5 disease types for argument component detection and argument relation classification:

- neoplasm: 350 train, 100 dev and 50 test abstracts
- glaucoma_test: 100 abstracts
- mixed_test: 100 abstracts (20 on glaucoma, 20 on neoplasm, 20 on diabetes, 20 on hypertension, 20 on hepatitis) 


As a result of corpus generation in Spanish, there are 4 versions of the translated and projected data for argument components, which are produced by a combination of each MT and word alignment systems. Argument relations required only a translation step.

Inside `data` folder: 
  - `neoplasm`, `glaucoma`, `mixed` - original English data of argument components and relations
  
  - `argument_components`

      - `projections` - post-processed projections in Spanish
      - `manual_projections` - manually corrected projections in Spanish
      - `multilingual` - merged English and Spanish train and dev sets
      
  - `argument_relations` 
      - `neoplasm` - argument relations in Spanish  
      - `glaucoma`- argument relations in Spanish
      - `mixed` - argument relations in Spanish
      - `multilingual` - merged English and Spanish train and dev sets
  
  
 # Translation
 In order to generate the corpus in Spanish, we first translate it with either [OPUS-MT](https://github.com/Helsinki-NLP/Opus-MT) or [DeepL](https://www.deepl.com/). To run the translation script:

```
sh translation/run_translate.sh
```

# Projection and correction

Projection is a step to transfer the annotations from the original corpus to the desired one. To run projections:

- Auto projection ([source](https://github.com/ikergarcia1996/Easy-Label-Projection))

(<i>Awesome align</i> requires parallel corpora, preferably domain-specific, which is stored in `biomedical-translation-parallel` folder)

```
sh projection/run_projection.sh
```

- Correct misalignments automatically: 

```
sh correction/post_processing/run_corrections.sh
```

- Correct misalignments manually ([source](https://github.com/ikergarcia1996/Annotation-Projection-App)):
```
sh correction/manual_correction/train-execute.sh
```

# Compare

To compare the projection outputs by different correction levels run the following line on the generated corpus:

```
py compare_projections.py
```

# Argument Mining

Fine-tuning transformer model for argument mining is done for argument component identification (sequence tagging task) and argument relation classification (sequence classification task). To do so execute the following script: <br>
<i>Models, tasks and hyper-parameters can be specified within the script.</i>
```
sh argument_mining/run_train.sh
```

Evaluation can be done in a similar fashion by running the script below. <br>
<u>Trained models, tasks and the test set can be changed in the script.</u>
```
sh argument_mining/run_evaluate.sh
```