from typing import TextIO, List
import random


def get_sentence_eval_file(file: TextIO) -> (List[str], List[str], List[str]):
    sentence: List[str] = []
    gold_tags: List[str] = []
    pred_tags: List[str] = []

    line: str = file.readline().rstrip().strip()
    while line:
        word: str
        pred_tag: str
        gold_tag: str
        try:
            word, gold_tag, pred_tag = line.split()
            sentence.append(word)
            gold_tags.append(gold_tag)
            pred_tags.append(pred_tag)
        except ValueError:
            raise ValueError(f"Error splitting line: {line}")

        line = file.readline().rstrip().strip()

    return sentence, gold_tags, pred_tags


def get_sentence_projection_file(file: TextIO) -> (List[str], List[str], List[str]):
    sentence: List[str] = []
    tags: List[str] = []

    line: str = file.readline().rstrip().strip()
    while line:
        word: str
        tag: str

        try:
            word, tag = line.split()
            sentence.append(word)
            tags.append(tag)
        except ValueError:
            raise ValueError(f"Error splitting line: {line}")

        line = file.readline().rstrip().strip()

    return sentence, tags


def get_difficult_sentences(
    num_sentences: int,
    eval_file_path: str,
    translation_path: str,
    projection_path: str,
    output_path_source: str,
    output_path_target: str,
    output_projection: str,
):
    with open(eval_file_path, "r", encoding="utf8") as eval_file, open(
        translation_path, "r", encoding="utf8"
    ) as translation_file, open(
        projection_path, "r", encoding="utf8"
    ) as projection_file:

        equal_source_sentences = []
        different_source_sentences = []

        (
            (sentence, gold_tags, pred_tags),
            translated_sentence,
            (projection_words, projections_tags),
        ) = (
            get_sentence_eval_file(eval_file),
            translation_file.readline().strip().rstrip(),
            get_sentence_projection_file(projection_file),
        )

        while sentence and gold_tags and pred_tags:
            if len(set(gold_tags)) > 1:
                if gold_tags == pred_tags:
                    equal_source_sentences.append(
                        [
                            sentence,
                            gold_tags,
                            pred_tags,
                            translated_sentence,
                            projection_words,
                            projections_tags,
                        ]
                    )
                else:
                    different_source_sentences.append(
                        [
                            sentence,
                            gold_tags,
                            pred_tags,
                            translated_sentence,
                            projection_words,
                            projections_tags,
                        ]
                    )

            (
                (sentence, gold_tags, pred_tags),
                translated_sentence,
                (projection_words, projections_tags),
            ) = (
                get_sentence_eval_file(eval_file),
                translation_file.readline().strip().rstrip(),
                get_sentence_projection_file(projection_file),
            )

    random.shuffle(equal_source_sentences)
    random.shuffle(different_source_sentences)

    print(
        f"Same tags sentences: {len(equal_source_sentences)}.\n"
        f"Different tags sentences: {len(different_source_sentences)}."
    )

    with open(output_path_source, "w+", encoding="utf8") as output_source, open(
        output_path_target, "w+", encoding="utf8"
    ) as output_target, open(
        output_projection, "w+", encoding="utf8"
    ) as output_projection:
        for (
            sentence,
            gold_tags,
            pred_tags,
            translated_sentence,
            projection_words,
            projections_tags,
        ) in (
            different_source_sentences[:num_sentences]
            + equal_source_sentences[
                : max(0, num_sentences - len(different_source_sentences))
            ]
        ):
            for word, gold_tag in zip(sentence, gold_tags):
                print(f"{word} {gold_tag}", file=output_source)
            print(file=output_source)

            for word, projections_tag in zip(projection_words, projections_tags):
                print(f"{word} {projections_tag}", file=output_projection)
            print(file=output_projection)

            print(translated_sentence, file=output_target)


get_difficult_sentences(
    num_sentences=100,
    eval_file_path="/home/iker/Documents/CrossTagging/TokenClassification/results/absa/projection/xlm-roberta-base/en2es_DeepL_simalign_original/0/en.absa.test.eval_file.tsv",
    translation_path="/home/iker/Documents/absa_datasets/DeepL/es/en.absa.test.txt",
    projection_path="/home/iker/Documents/absa_datasets/projections/en2es/DeepL.50000.original.simalign.test.tsv",
    output_path_source="../100test/en.absa.test.tsv",
    output_path_target="../100test/en2es.absa.test.DeepL.txt",
    output_projection="../100test/en2es.absa.test.SimAlign.txt",
)
