#!/usr/bin/env bash

# ACTIVATE VIRTUAL ENVIRONMENT
#source activate test

# SELECT TASK

# 1) SEQUENCE TAGGING
export TASK_NAME=seqtag
export MODELTYPE=bert-seqtag

#2) RELATION CLASSIFICATION
#export TASK_NAME=relclass
#export MODELTYPE=bert
#export MODELTYPE=xlm-roberta

# 3) MULTIPLE CHOICE (requires that train_multiplechoice.py is executed instead of train.py, see below)
#export TASK_NAME=multichoice
#export MODELTYPE=bert-multichoice


# PATH TO TEST DATA
#(relation classification)

#export DATA_DIR=../data/neoplasm
#export DATA_DIR=../data/glaucoma
#export DATA_DIR=../data/mixed

#rel_clf_es
#export DATA_DIR=../data/argument_relations/neoplasm
#export DATA_DIR=../data/argument_relations/glaucoma
#export DATA_DIR=../data/argument_relations/mixed 

#(seqtag)
#export DATA_DIR=../data/neoplasm/
#export DATA_DIR=../data/glaucoma/
#export DATA_DIR=../data/mixed/

#directly projected
#export DATA_DIR=../data/projected/deepl_simalign/neoplasm/
#export DATA_DIR=../data/projected/deepl_simalign/glaucoma/
#export DATA_DIR=../data/projected/deepl_simalign/mixed/ 

#export DATA_DIR=../data/projected/opus_simalign/neoplasm/
#export DATA_DIR=../data/projected/opus_simalign/glaucoma/
#export DATA_DIR=../data/projected/opus_simalign/mixed/

#export DATA_DIR=../data/projected/deepl_awesome/neoplasm/
#export DATA_DIR=../data/projected/deepl_awesome/mixed/ 
#export DATA_DIR=../data/projected/deepl_awesome/glaucoma/

#export DATA_DIR=../data/projected/opus_awesome/mixed/
#export DATA_DIR=../data/projected/opus_awesome/glaucoma/
#export DATA_DIR=../data/projected/opus_awesome/neoplasm/    

#postprocessed
#export DATA_DIR=../data/auto_corrected/deepl_simalign/neoplasm/
#export DATA_DIR=../data/auto_corrected/deepl_simalign/glaucoma/
#export DATA_DIR=../data/auto_corrected/deepl_simalign/mixed/

#export DATA_DIR=../data/auto_corrected/deepl_awesome/neoplasm/
#export DATA_DIR=../data/auto_corrected/deepl_awesome/mixed/
#export DATA_DIR=../data/auto_corrected/deepl_awesome/glaucoma/

#export DATA_DIR=../data/auto_corrected/opus_simalign/neoplasm/
#export DATA_DIR=../data/auto_corrected/opus_simalign/glaucoma/
#export DATA_DIR=../data/auto_corrected/opus_simalign/mixed/

#export DATA_DIR=../data/auto_corrected/opus_awesome/neoplasm/
#export DATA_DIR=../data/auto_corrected/opus_awesome/glaucoma/
#export DATA_DIR=../data/auto_corrected/opus_awesome/mixed/


# manual projections
#export DATA_DIR=../data/manual_projections/deepl/awesome/neoplasm 
#export DATA_DIR=../data/manual_projections/deepl/awesome/glaucoma
#export DATA_DIR=../data/manual_projections/deepl/awesome/mixed

#export DATA_DIR=../data/manual_projections/deepl/simalign/neoplasm 
#export DATA_DIR=../data/manual_projections/deepl/simalign/glaucoma
#export DATA_DIR=../data/manual_projections/deepl/simalign/mixed

#export DATA_DIR=../data/manual_projections/opus/awesome/neoplasm
#export DATA_DIR=../data/manual_projections/opus/awesome/glaucoma
#export DATA_DIR=../data/manual_projections/opus/awesome/mixed

#export DATA_DIR=../data/manual_projections/opus/simalign/neoplasm
#export DATA_DIR=../data/manual_projections/opus/simalign/glaucoma
export DATA_DIR=../data/manual_projections/opus/simalign/mixed

# MAXIMUM SEQUENCE LENGTH
export MAXSEQLENGTH=128

# EVALUATE MODEL:
export MODEL=output/seqtag+128/
#export MODEL=output/relclass+128/ 

export OUTPUTDIR=$MODEL

#python train_multiplechoice.py \
python train.py \
  --model_type $MODELTYPE \
  --model_name_or_path $MODEL \
  --output_dir $OUTPUTDIR \
  --task_name $TASK_NAME \
  --do_eval \
  --do_lower_case \
  --data_dir $DATA_DIR \
  --max_seq_length $MAXSEQLENGTH \
  --overwrite_output_dir \
  --overwrite_cache \
  --per_gpu_train_batch_size 32 \
  --learning_rate 5e-5 \
  --num_train_epochs 1.0 \
  --save_steps 1000
