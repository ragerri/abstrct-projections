# AbstRCT-projections
This repository contains a medical corpus for argument mining [AbstRCT](https://gitlab.com/tomaye/abstrct) (a dataset of clinical abstracts annotated for argument mining in English), and generation of the dataset in Spanish, French and Italian by translation and projection using word alignment tools, such as Awesome align and Simalign. 

Table of contents:

- [Data](#data)
- [Cross-lingual argument mining](#cross-lignual-argument-mining)
    - [Translation](#translation)
    - [Projection and correction](#projection-and-correction)
    - [Argument Mining](#argument-mining)

Before running the scripts below, consider running `pip install -r requirements.txt` first.

# Data

The dataset consists of abstracts of 5 disease types for argument component detection and argument relation classification:

- `neoplasm`: 350 train, 100 dev and 50 test abstracts
- `glaucoma_test`: 100 abstracts
- `mixed_test`: 100 abstracts (20 on glaucoma, 20 on neoplasm, 20 on diabetes, 20 on hypertension, 20 on hepatitis) 


As a result of corpus generation in Spanish, French and Italian, there are several versions of the translated and projected data for argument components, which are produced by a combination of different MT and word alignment systems. 
Therefore, we store the data used in the experiments and all generated data separately.
<!-- Argument relations required only a translation step. -->

Inside `data/data_for_experiments/$LANG` folder: 
  - `neoplasm`, `glaucoma`, `mixed` - original English data of argument components and relations
  
  - `argument_components/$MT_$projection/`

      - `automatic_projections` - post-processed projections in Spanish
      - `manual_revision` - manually corrected projections in Spanish
      - `postprocessed` - merged English and Spanish train and dev sets 
      

  - `argument_relations` (Only English and Spanish)
      - `neoplasm` - argument relations in Spanish  
      - `glaucoma`- argument relations in Spanish
      - `mixed` - argument relations in Spanish
      - `multilingual` - merged English and Spanish train and dev sets
  
 # Cross-lignual Argument Mining

In order to generate data in another language, the data is first translated to the target language, then the annotations from the source data are projected to the newly translated target data. 
 <!-- In order to generate data from the source to target language we should translate the text and project the labels.  -->
 
 ```
cd cross-lingual-argument-mining
```

 # Translation
 To generate the corpus, we first translate it with either [OPUS-MT](https://github.com/Helsinki-NLP/Opus-MT) or [DeepL](https://www.deepl.com/). To run the translation script:

```
sh translation/run_translate.sh
```

Additionally, we used [NLLB](https://arxiv.org/abs/2207.04672). Check [this repo](https://github.com/ikergarcia1996/Easy-Translate) for more.

# Projection and correction

Projection is a step to transfer the annotations from the original corpus to the desired one. To run projections:

- Label projection ([source](https://github.com/ikergarcia1996/Easy-Label-Projection))

(<i>Awesome align</i> requires parallel corpora, preferably domain-specific, which is stored in `biomedical-translation-parallel` folder)

```
sh projection/run_projection.sh
```

- Correct misalignments produced during automatic projection: 

```
sh correction/post_processing/run_corrections.sh
```

- Correct misalignments manually ([source](https://github.com/ikergarcia1996/Annotation-Projection-App)):
```
sh correction/manual_correction/train-execute.sh
```

# Compare

To compare the projection outputs by different correction levels (i.e., before running correction script and after) run the following line on the generated corpus:

```
python compare_projections.py
```

# Argument Mining

Fine-tuning transformer model for argument mining is done for argument component identification (sequence tagging task) and argument relation classification (sequence classification task). To do so execute the following script: <br>
<i>Models, tasks and hyper-parameters can be specified within the script.</i>
```
sh ACTA/run_train.sh
```

Evaluation can be done similarly by running the script below. <br>
<u>Trained models, tasks and the test set can be changed in the script.</u>
```
sh ACTA/run_evaluate.sh