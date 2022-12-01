python3 annotation_projection.py \
--source_test data/neoplasm/train.tsv \
--target_test data/neoplasm/train_deepl.txt \
--source_augmentation biomedical-translation-parallel/en.txt \
--target_augmentation biomedical-translation-parallel/es.txt \
--output_dir output/ --output_name deepl_train_simalign \
--do_awesome

#python3 annotation_projection.py \
#--source_test data/neoplasm/train.tsv \
#--target_test data/neoplasm/train_deepl.txt \
#--source_augmentation biomedical-translation-parallel/en.txt \
#--target_augmentation biomedical-translation-parallel/es.txt \
#--output_dir output/06_03/ --output_name deepl_train_simalign \
#--remove_awesome_model \
#--do_awesome

