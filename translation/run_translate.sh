export INPUT_PATH='./data/neoplasm/dev.tsv'
export OUTPUT_LINE_PATH='test.txt'
export MODEL='deepl'
export OUTPUT_TRANSLATION_PATH=/Users/anaryegen/Desktop/translated_${MODEL}.txt
export DEEPL_KEY=''

python translate.py \
--data_path=$INPUT_PATH \
--output_path=$OUTPUT_LINE_PATH \
--save_translation_file=$OUTPUT_TRANSLATION_PATH \
--model=$MODEL \
--deepl_key=$DEEPL_KEY
