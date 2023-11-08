

#------------------------------AWESOME ALIGN--------------------------

#=================================
# Neoplasm
#=================================

#TRAIN

# (DeepL)

#python3 app.py \
#--source_dataset SpanishExperiments/projections/deepl_awesome/neoplasm/pprocessed_train.tsv \
#--en_dataset SpanishExperiments/neoplasm/train.tsv \
#--target_sentences SpanishExperiments/neoplasm/train_deepl.txt \
#--output_dataset SpanishExperiments/output/neoplasm_train_awesome_deepl_manual.tsv

# (Opus)

#python3 app.py \
#--source_dataset SpanishExperiments/projections/opus_awesome/neoplasm/pprocessed_train.tsv \
#--en_dataset SpanishExperiments/neoplasm/train.tsv \
#--target_sentences SpanishExperiments/neoplasm/train_opus.txt \
#--output_dataset SpanishExperiments/output/neoplasm_train_awesome_opus_manual.tsv

#TEST

# (DeepL)
#python3 app.py \
#--source_dataset SpanishExperiments/projections/deepl_awesome/neoplasm/pprocessed_test.tsv \
#--en_dataset SpanishExperiments/neoplasm/test.tsv \
#--target_sentences SpanishExperiments/neoplasm/test_deepl.txt \
#--output_dataset SpanishExperiments/output/neoplasm_test_awesome_deepl_manual.tsv

# (Opus)
#python3 app.py \
#--source_dataset SpanishExperiments/projections/opus_awesome/neoplasm/pprocessed_test.tsv \
#--en_dataset SpanishExperiments/neoplasm/test.tsv \
#--target_sentences SpanishExperiments/neoplasm/test_opus.txt \
#--output_dataset SpanishExperiments/output/neoplasm_test_awesome_opus_manual.tsv

# DEV

#(DeepL)
#python3 app.py \
#--source_dataset SpanishExperiments/projections/deepl_awesome/neoplasm/pprocessed_dev.tsv \
#--en_dataset SpanishExperiments/neoplasm/dev.tsv \
#--target_sentences SpanishExperiments/neoplasm/dev_deepl.txt \
#--output_dataset SpanishExperiments/output/neoplasm_dev_awesome_deepl_manual.tsv

# (Opus)
#python3 app.py \
#--source_dataset SpanishExperiments/projections/opus_awesome/neoplasm/pprocessed_test.tsv \
#--en_dataset SpanishExperiments/neoplasm/dev.tsv \
#--target_sentences SpanishExperiments/neoplasm/dev_opus.txt \
#--output_dataset SpanishExperiments/output/neoplasm_dev_awesome_opus_manual.tsv

#=================================
# Glaucoma
#=================================

#(DeepL)

#python3 app.py \
#--source_dataset SpanishExperiments/projections/deepl_awesome/glaucoma/pprocessed_test.tsv \
#--target_sentences SpanishExperiments/glaucoma/glaucoma_deepl.txt \
#--en_dataset SpanishExperiments/glaucoma/test.tsv \
#--output_dataset SpanishExperiments/output/glaucoma_deepl_awesome_manual.tsv

# (Opus)
#python3 app.py \
#--source_dataset SpanishExperiments/projections/opus_awesome/glaucoma/pprocessed_test.tsv \
#--target_sentences SpanishExperiments/glaucoma/glaucoma_opus.txt \
#--en_dataset SpanishExperiments/glaucoma/test.tsv \
#--output_dataset SpanishExperiments/output/glaucoma_opus_awesome_manual.tsv


#=================================
# Mixed
#=================================

# (DeepL)

#python3 app.py \
#--source_dataset SpanishExperiments/projections/deepl_awesome/mixed/pprocessed_test.tsv \
#--en_dataset SpanishExperiments/mixed/test.tsv \
#--target_sentences SpanishExperiments/mixed/mixed_deepl.txt \
#--output_dataset SpanishExperiments/output/mixed_awesome_deepl_manual.tsv

# (Opus)

#python3 app.py \
#--source_dataset SpanishExperiments/projections/opus_awesome/mixed/pprocessed_test.tsv \
#--en_dataset SpanishExperiments/mixed/test.tsv \
#--target_sentences SpanishExperiments/mixed/mixed_opus.txt \
#--output_dataset SpanishExperiments/output/mixed_awesome_opus_manual.tsv


#------------------------------SIMALIGN-------------------------------------------------


#=================================
# Neoplasm
#=================================

#TRAIN

# (DeepL)

#python3 app.py \
#--source_dataset SpanishExperiments/projections/deepl_simalign/neoplasm/pprocessed_train.tsv \
#--en_dataset SpanishExperiments/neoplasm/train.tsv \
#--target_sentences SpanishExperiments/neoplasm/train_deepl.txt \
#--output_dataset SpanishExperiments/output/neoplasm_train_simalign_deepl_manual.tsv

# (Opus)

#python3 app.py \
#--source_dataset SpanishExperiments/projections/opus_simalign/neoplasm/pprocessed_train.tsv \
#--en_dataset SpanishExperiments/neoplasm/train.tsv \
#--target_sentences SpanishExperiments/neoplasm/train_opus.txt \
#--output_dataset SpanishExperiments/output/neoplasm_train_simalign_opus_manual.tsv

#TEST

# (DeepL)
#python3 app.py \
#--source_dataset SpanishExperiments/projections/deepl_simalign/neoplasm/pprocessed_test.tsv \
#--en_dataset SpanishExperiments/neoplasm/test.tsv \
#--target_sentences SpanishExperiments/neoplasm/test_deepl.txt \
#--output_dataset SpanishExperiments/output/neoplasm_test_simalign_deepl_manual.tsv

# (Opus)
#python3 app.py \
#--source_dataset SpanishExperiments/projections/opus_simalign/neoplasm/pprocessed_test.tsv \
#--en_dataset SpanishExperiments/neoplasm/test.tsv \
#--target_sentences SpanishExperiments/neoplasm/test_opus.txt \
#--output_dataset SpanishExperiments/output/neoplasm_test_simalign_opus_manual.tsv

# DEV

#(DeepL)
#python3 app.py \
#--source_dataset SpanishExperiments/projections/deepl_simalign/neoplasm/pprocessed_dev.tsv \
#--en_dataset SpanishExperiments/neoplasm/dev.tsv \
#--target_sentences SpanishExperiments/neoplasm/dev_deepl.txt \
#--output_dataset SpanishExperiments/output/neoplasm_dev_simalign_deepl_manual.tsv

# (Opus)
#python3 app.py \
#--source_dataset SpanishExperiments/projections/opus_simalign/neoplasm/pprocessed_test.tsv \
#--en_dataset SpanishExperiments/neoplasm/dev.tsv \
#--target_sentences SpanishExperiments/neoplasm/dev_opus.txt \
#--output_dataset SpanishExperiments/output/neoplasm_dev_simalign_opus_manual.tsv

#=================================
# Glaucoma
#=================================

#(DeepL)

#python3 app.py \
#--source_dataset SpanishExperiments/projections/deepl_simalign/glaucoma/pprocessed_test.tsv \
#--target_sentences SpanishExperiments/glaucoma/glaucoma_deepl.txt \
#--en_dataset SpanishExperiments/glaucoma/test.tsv \
#--output_dataset SpanishExperiments/output/glaucoma_deepl_simalign_manual.tsv

# (Opus)
#python3 app.py \
#--source_dataset SpanishExperiments/projections/opus_simalign/glaucoma/pprocessed_test.tsv \
#--target_sentences SpanishExperiments/glaucoma/glaucoma_opus.txt \
#--en_dataset SpanishExperiments/glaucoma/test.tsv \
#--output_dataset SpanishExperiments/output/glaucoma_opus_simalign_manual.tsv


#=================================
# Mixed
#=================================

# (DeepL)

python3 app.py \
--source_dataset SpanishExperiments/projections/deepl_simalign/mixed/pprocessed_test.tsv \
--en_dataset SpanishExperiments/mixed/test.tsv \
--target_sentences SpanishExperiments/mixed/mixed_deepl.txt \
--output_dataset SpanishExperiments/output/mixed_simalign_deepl_manual.tsv

# (Opus)

#python3 app.py \
#--source_dataset SpanishExperiments/projections/opus_simalign/mixed/pprocessed_test.tsv \
#--en_dataset SpanishExperiments/mixed/test.tsv \
#--target_sentences SpanishExperiments/mixed/mixed_opus.txt \
#--output_dataset SpanishExperiments/output/mixed_simalign_opus_manual.tsv
