 # Cross-lignual Argument Minig

 <!-- This folder consists of data generation and argument mining components. 
 In order to generate data from the source to target language we should translate the text and project the labels.  -->
 
 # Translation
 In order to generate the corpus in Spanish, we first translate it with either [OPUS-MT](https://github.com/Helsinki-NLP/Opus-MT) or [DeepL](https://www.deepl.com/). To run the translation script:

```
sh translation/run_translate.sh
```

# Projection and correction

Projection is a step to transfer the annotations from the original corpus to the desired one. To run projections:

- Label projection ([source](https://github.com/ikergarcia1996/Easy-Label-Projection))

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

# ACTA

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