import argparse
from tqdm import tqdm
from easynmt import EasyNMT
import deepl


def to_sentence(input_file, output_file):
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


def translate_opus(source_file, output_file):
    model = EasyNMT('opus-mt')
    num_sentences = len(open(source_file).readlines())
    translate_file = open(source_file, 'r')
    write_translation = open(output_file, 'w')
    
    for _, text in zip(tqdm(range(num_sentences)) ,translate_file):
        write_translation.write(model.translate(text, target_lang='es'))
    
    return

def translate_deepl(source_file, output_file, auth_key):

    translator = deepl.Translator(auth_key)
    num_sentences = len(open(source_file, 'r').readlines())
    file = open(source_file, 'r')
    wr = open(output_file, 'w')

    for _, line in zip(tqdm(range(num_sentences)),file):

        translation = translator.translate_text(line, target_lang="ES")
        wr.write(translation.text)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--data_path",
        type=str,
        required=True,
        help="Path to the annootated .tsv file",
    )
    parser.add_argument(
        "--output_path",
        type=str,
        required=True,
        help="Path to save output of sentences from .tsv file",
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
      default='opus-mt',
      help='Translation model: opus-mt or deepL'
    )
    parser.add_argument(
      '--deepl_key',
      type=str,
      required=False,
      default='',
      help='Auth key for DeepL API'
    )


    args = parser.parse_args()

    to_sentence(
      input_file=args.data_path,
      output_file=args.output_path,
    )
    if args.model == 'opus-mt':
      translate_opus(
        source_file=args.output_path,
        output_file=args.save_translation_file
      )
    elif args.model == 'deepl':
      translate_deepl(
        source_file=args.output_path,
        output_file=args.save_translation_file,
        auth_key=args.deepl_key
      )
