<!-- # antidote-projections

This repository contains a medical corpus for argument mining in Spanish that was generated from [AbstRCT corpus](https://gitlab.com/tomaye/abstrct), a dataset of clinical abstracts annotated for argument mining in English), by translating with Opus-MT and DeepL, and projecting using word alignment tools, such as Awesome align and Simalign. After automatic projection, the corpus was post-processed and manually corrected. 

The dataset consists of abstracts of 5 disease types for argument component detection and argument relation classification:

- neoplasm: 350 train, 100 dev and 50 test abstracts
- glaucoma_test: 100 abstracts
- mixed_test: 100 abstracts (20 on glaucoma, 20 on neoplasm, 20 on diabetes, 20 on hypertension, 20 on hepatitis) 


As a result of corpus generation in Spanish, there are 4 versions of the translated and projected data for argument components, which are produced by a combination of each MT and word alignment system. Argument relations required only a translation step, and it was done using Opus-MT.

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
 -->
