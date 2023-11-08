#!/usr/bin/env bash

# ACTIVATE VIRTUAL ENVIRONMENT
#source activate test

# SELECT TASK

# 1) SEQUENCE TAGGING
export TASK_NAME=seqtag
export MODELTYPE=bert-seqtag
#export MODELTYPE=roberta

# 2) RELATION CLASSIFICATION
#export TASK_NAME=relclass
#export MODELTYPE=bert


# =============================  PATHs TO TRAINING DATA ===============================

# original English data
#export DATA_DIR=../data/neoplasm

# ========= Relation classifications ==============
#   ES
#export DATA_DIR=../data/argument_relations/neoplasm
#  ES+EN
#export DATA_DIR=../data/argument_relations/multilingual

# ========= Sequence classification  ==============
#export DATA_DIR=../data/argument_components/multilingual/


#----------- 1.  Manual projections ---------------
#export DATA_DIR=../data/manual_projections/deepl/awesome
#export DATA_DIR=../data/manual_projections/deepl/simalign  
#export DATA_DIR=../data/manual_projections/opus/awesome 
#export DATA_DIR=../data/manual_projections/opus/simalign


#---------- 2. Automatic projections --------------
#export DATA_DIR=../data/projected/deepl_awesome/neoplasm/auto
#export DATA_DIR=../data/projected/deepl_simalign/neoplasm/auto
#export DATA_DIR=../data/projected/opus_awesome/neoplasm/auto
#export DATA_DIR=../data/projected/opus_simalign/neoplasm/auto

#---------- 3. Post processed projections ---------
#export DATA_DIR=../data/auto_corrected/deepl_awesome/neoplasm/post_processed
#export DATA_DIR=../data/auto_corrected/deepl_simalign/neoplasm/post_processed
#export DATA_DIR=../data/auto_corrected/opus_awesome/neoplasm/post_processed
export DATA_DIR=../data/auto_corrected/opus_simalign/neoplasm/post_processed


# MAXIMUM SEQUENCE LENGTH
export MAXSEQLENGTH=128
export OUTPUTDIR=output/$TASK_NAME+$MAXSEQLENGTH


# SELECT MODEL FOR FINE-TUNING

#export MODEL=bert-base-uncased
#export MODEL=monologg/biobert_v1.1_pubmed
#export MODEL=allenai/scibert_scivocab_uncased

#mBERT
export MODEL=bert-base-multilingual-uncased

# BETO
#export MODEL=dccuchile/bert-base-spanish-wwm-uncased


#python train_multiplechoice.py \
python train.py  --model_type $MODELTYPE \
  --model_name_or_path $MODEL \
  --output_dir $OUTPUTDIR \
  --task_name $TASK_NAME \
  --do_train  \
  --do_eval \
  --do_lower_case \
  --data_dir $DATA_DIR \
  --max_seq_length $MAXSEQLENGTH \
  --overwrite_output_dir \
  --per_gpu_train_batch_size 32 \
  --learning_rate 5e-5 \
  --num_train_epochs 3.0 \
  --save_steps 1000 \
  --overwrite_cache #req for multiple choice
