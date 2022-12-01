from typing import List, TextIO
import logging
import os
from shlex import quote
import subprocess
from tabulate import tabulate


def evaluate_file(
    original_dataset_path: str,
    predictions_path: str,
    output_dir: str,
    output_name: str,
):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    create_eval_file(
        original_dataset_path=original_dataset_path,
        model_predictions_path=predictions_path,
        output_path=os.path.join(output_dir, f"{output_name}.eval_file.tsv"),
    )

    eval_conlleval(
        input_path=os.path.join(output_dir, f"{output_name}.eval_file.tsv"),
        output_path=os.path.join(output_dir, f"{output_name}.eval_result.txt"),
    )

    generate_dictionary(
        eval_file_path=os.path.join(output_dir, f"{output_name}.eval_file.tsv"),
        output_path=os.path.join(output_dir, f"{output_name}.test_summary.txt"),
        output_path_incorrect_sentences=os.path.join(
            output_dir, f"{output_name}.test_incorrect_sentences.txt"
        ),
    )


def print_sentence(
    output: TextIO,
    words: List[str],
    golds: List[str],
    precs: List[str],
) -> None:
    assert len(words) == len(golds) == len(precs), (
        f"Error, we have a different number of lens for the words,"
        f" tags, golds and predictions lists. words:"
        f" {words}. golds: {golds}. precs: {precs}"
    )

    for word, gold, prec in zip(words, golds, precs):
        print(f"{word} {gold} {prec}", file=output)

    print(file=output)


def create_eval_file(
    original_dataset_path: str,
    model_predictions_path: str,
    output_path: str,
) -> None:

    with open(original_dataset_path, "r", encoding="utf-8") as original_data, open(
        model_predictions_path, "r", encoding="utf-8"
    ) as model_precs, open(output_path, "w+", encoding="utf-8") as output:
        line_precs: str = model_precs.readline()
        golds: List[str] = []
        precs: List[str] = []
        words: List[str] = []
        line_no = 0
        while line_precs:
            line_no += 1
            gold_line: str = original_data.readline()

            if line_precs == "\n":

                print_sentence(output, words, golds, precs)

                while gold_line != "\n" and gold_line:
                    try:
                        word_gold, _, _ = gold_line.rstrip().split("\t")
                    except ValueError:
                        raise ValueError(
                            f"Error in line {line_no}. Unable to split line in 2 fields: [{gold_line}]"
                        )
                    logging.warning(f"No prediction for the word {word_gold}")
                    gold_line = original_data.readline()

                golds = []
                precs = []
                words = []

            else:

                try:
                    word_prec, prec = line_precs.rstrip().split(" ")
                except ValueError:
                    raise ValueError(
                        f"Error in line {line_no}. Unable to split line in 2 fields: [{line_precs}]"
                    )

                try:
                    word_gold, tag_gold, _ = gold_line.rstrip().split("\t")
                except ValueError:
                    raise ValueError(
                        f"Error in line {line_no}. Unable to split line in 2 fields: [{gold_line}]"
                    )

                if word_prec == word_gold:
                    words.append(word_prec)
                    precs.append(prec)
                    golds.append(tag_gold)

                else:
                    raise ValueError(
                        f"Error in line {line_no}. Error reading the files: "
                        f"Line gold data: {gold_line}. Line predictions data: {line_precs}"
                    )

            line_precs = model_precs.readline()

        if words and golds and precs:
            print_sentence(output, words, golds, precs)


def eval_conlleval(
    input_path: str, output_path: str, conlleval_script: str = "./conlleval"
) -> None:
    command: str = (
        f"{quote(conlleval_script)} < {quote(input_path)} > {quote(output_path)}"
    )
    run_bash_command(command)


def get_float(s: str) -> float:
    # "98,1%;" -> 98.1
    return float(s.replace("%", "").replace(";", ""))


def get_f1(result_file_path: str) -> float:
    with open(result_file_path) as f:
        f.readline()
        results_line: str = f.readline().rstrip()
        _, acc, _, p, _, r, _, f1 = results_line.split()
    return get_float(f1)


def run_bash_command(command: str) -> None:
    print(command)
    subprocess.run(["bash", "-c", command])


def generate_dictionary(
    eval_file_path: str, output_path: str, output_path_incorrect_sentences: str
):
    dictionary = {}
    with open(eval_file_path, "r", encoding="utf8") as eval_file, open(
        output_path, "w+", encoding="utf8"
    ) as output, open(
        output_path_incorrect_sentences, "w+", encoding="utf8"
    ) as output_sentences:

        sentence = []
        correct_sentence = True

        for line in eval_file:
            line = line.rstrip().strip()
            try:
                if line:
                    word, gold, pred = line.split()
                    if word in dictionary:
                        dictionary[word]["Occurrences"] += 1
                    else:
                        dictionary[word] = {
                            "TP": 0,
                            "TN": 0,
                            "FP": 0,
                            "FN": 0,
                            "Occurrences": 1,
                        }
                    if gold != pred:

                        correct_sentence = False
                        if gold == "O":
                            sentence.append(f"\033[94m [{word} -- O as T] \033[0m")
                            dictionary[word]["FP"] += 1
                        else:
                            if pred == "O":
                                dictionary[word]["FN"] += 1
                                sentence.append(f"\033[92m [{word} -- T as O \033[0m]")
                            else:
                                sentence.append(word)
                                if gold == "O":
                                    dictionary[word]["TN"] += 1
                                else:
                                    dictionary[word]["TP"] += 1
                    else:
                        sentence.append(word)
                        if gold == "O":
                            dictionary[word]["TN"] += 1
                        else:
                            dictionary[word]["TP"] += 1
                    if pred != "O":
                        sentence.append("*")
                else:
                    if not correct_sentence:
                        print(" ".join(sentence), file=output_sentences)

                    sentence = []
                    correct_sentence = True

            except ValueError:
                raise ValueError(f"Error splitting line: {line}")
        table_entries = []
        for item in sorted(
            dictionary.items(),
            key=lambda x: x[1]["FN"] + x[1]["FP"],
            reverse=True,
        ):
            table_entries.append(
                [
                    item[0],
                    item[1]["TP"],
                    item[1]["TN"],
                    item[1]["FP"],
                    item[1]["FN"],
                    item[1]["Occurrences"],
                ]
            )
        print(
            tabulate(
                table_entries,
                headers=[
                    "Word",
                    "TP",
                    "TN",
                    "FP",
                    "FN",
                    "Occurrences",
                ],
            ),
            file=output,
        )


evaluate_file(
    predictions_path="../100test/en2es.absa.test.SimAlign.txt",
    original_dataset_path="../100test/Iker.tsv",
    output_dir="../100test/SimalignIker",
    output_name="test",
)

evaluate_file(
    predictions_path="../100test/en2es.absa.test.SimAlign.txt",
    original_dataset_path="../100test/Rodrigo.tsv",
    output_dir="../100test/SimalignRodrigo",
    output_name="test",
)

evaluate_file(
    predictions_path="../100test/en2es.absa.test.SimAlign.txt",
    original_dataset_path="../100test/German.tsv",
    output_dir="../100test/SimalignGerman",
    output_name="test",
)

evaluate_file(
    predictions_path="../100test/en2es.absa.test.mgiza_original.txt",
    original_dataset_path="../100test/Rodrigo.tsv",
    output_dir="../100test/Mgiza_originalRodrigo",
    output_name="test",
)
"""
evaluate_file(
    predictions_path="../100test/en2es.absa.test.mgiza_translated.txt",
    original_dataset_path="../100test/Rodrigo.tsv",
    output_dir="../100test/Mgiza_translatedRodrigo",
    output_name="test",
)
"""
evaluate_file(
    predictions_path="../100test/en2es.absa.test.fastalign_original.txt",
    original_dataset_path="../100test/Rodrigo.tsv",
    output_dir="../100test/fastalign_originalRodrigo",
    output_name="test",
)
"""
evaluate_file(
    predictions_path="../100test/en2es.absa.test.fastalign_translated.txt",
    original_dataset_path="../100test/Rodrigo.tsv",
    output_dir="../100test/fastalign_translatedRodrigo",
    output_name="test",
)
"""
