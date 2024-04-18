# antidote-projections
This repository contains a medical corpus of argument mining [AbstRCT corpus](https://gitlab.com/tomaye/abstrct) (a dataset of clinical abstracts annotated for argument mining in English), and generation of the dataset in Spanish by translation and projection using word alignment tools, such as Awesome align and Simalign. 

Consider running `pip install requirements.txt` before running the scripts below.

Table of contents:

- [Data](#data)
- [Cross-lingual argument mining](https://github.com/ragerri/antidote-projections/tree/main/cross-lingual-argument-mining)


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
  