python3 annotation_projection.py \
--source_test .data/neoplasm/train.tsv \
--target_test .data/neoplasm/train_deepl.txt \
--source_augmentation data/biomedical-translation-parallel/en.txt \
--target_augmentation data/biomedical-translation-parallel/es.txt \
--output_dir output/ --output_name deepl_train_simalign \
--do_awesome

