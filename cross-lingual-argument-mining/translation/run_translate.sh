export INPUT_PATH='../data/full_line_en/np_dev_en.txt'
export MODEL='opus-mt'
export OUTPUT_TRANSLATION_PATH=translated_${MODEL}.txt
export LANGUAGE='es'
export DEEPL_KEY=''

python translate.py \
--data_path=$INPUT_PATH \
--save_translation_file=$OUTPUT_TRANSLATION_PATH \
--target_language=$LANGUAGE \
--model=$MODEL \
--deepl_key=$DEEPL_KEY