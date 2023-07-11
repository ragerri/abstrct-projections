import argparse
from tqdm import tqdm
from easynmt import EasyNMT
import deepl


def to_sentence(input_file, output_file):
  '''
  Collect sequences in .tsv file into lines and save it into .txt file
  '''
  sentence = ''
  file = open(input_file, 'r')
  write_file = open(output_file, 'w')
  for line in file:
      if line != '\n':
        token = line.split(' ')[0]
        sentence += token + ' '
      else:
        write_file.write(sentence + '\n')
        sentence = ''
  return write_file


def translate_opus(source_file, output_file, target_language):
  
    model = EasyNMT('opus-mt')
    num_sentences = len(open(source_file).readlines())
    translate_file = open(source_file, 'r')
    write_translation = open(output_file, 'w')
    
    for _, text in zip(tqdm(range(num_sentences)) ,translate_file):
        write_translation.write(model.translate(text, target_lang=target_language))
    
    return

def translate_deepl(source_file, output_file, target_language,auth_key):

    translator = deepl.Translator(auth_key)
    num_sentences = len(open(source_file, 'r').readlines())
    file = open(source_file, 'r')
    wr = open(output_file, 'w')

    for _, line in zip(tqdm(range(num_sentences)),file):
        translation = translator.translate_text(line,target_lang=target_language)
        wr.write(translation.text)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--data_path",
        type=str,
        required=True,
        help="Path to the .txt file to tranlsate",
    )
    parser.add_argument(
        "--target_language",
        type=str,
        required=True,
        help="The target language to translate the data",
    )
    parser.add_argument(
        "--save_translation_file",
        type=str,
        required=True,
        help="The file to write the transaltions",
    )
    parser.add_argument(
      '--model',
      type=str,
      required=False,
      help='Translation model: opus-mt or deepl'
    )
    parser.add_argument(
      '--deepl_key',
      type=str,
      required=False,
      default='',
      help='Auth key for DeepL API'
    )


    args = parser.parse_args()

    if args.model == 'opus-mt':
      translate_opus(
        source_file=args.data_path,
        output_file=args.save_translation_file,
        target_language=args.target_language
      )
    elif args.model == 'deepl':
      translate_deepl(
        source_file=args.data_path,
        output_file=args.save_translation_file,
        target_language=args.target_language,
        auth_key=args.deepl_key
      )
