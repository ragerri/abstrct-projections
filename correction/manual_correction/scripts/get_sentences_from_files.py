from typing import TextIO, List


def get_sentence(file: TextIO) -> (List[str], List[str], List[str]):
    sentence: List[str] = []
    tags: List[str] = []

    line: str = file.readline().rstrip().strip()
    while line:
        word: str
        tag: str

        try:
            word, tag = line.split(" ")
            sentence.append(word)
            tags.append(tag)
        except ValueError:
            raise ValueError(f"Error splitting line: {line}")

        line = file.readline().rstrip().strip()

    return sentence, tags


def get_all_sentences(file_path: str):

    sentences = []
    with open(file_path, "r", encoding="utf8") as file:
        words, tags = get_sentence(file)

        while words and tags:
            sentences.append([words, tags])
            words, tags = get_sentence(file)

    return sentences


def build_dictionary(target_file_path: str):
    data = get_all_sentences(target_file_path)
    dictionary = {}
    i = 0
    for words, tags in data:
        s = " ".join(words)
        try:
            dictionary[s].append(i)
        except KeyError:
            dictionary[s] = [i]
        i += 1

    return dictionary, i
    # return {" ".join(s[0]): i for i, s in enumerate(data) if s[0] and s[1]}


def get_sentences_from_file(
    source_file_path: str, target_file_path: str, output_path: str
):
    dictionary, dict_len = build_dictionary(target_file_path=target_file_path)
    sentences = [[] for _ in range(dict_len)]

    with open(source_file_path, "r", encoding="utf8") as source_file:
        words, tags = get_sentence(source_file)
        found = 0
        while words and tags:
            s = " ".join(words)
            if s in dictionary:
                for i in dictionary[s]:
                    sentences[i] = [words, tags]
                found += 1
                if dictionary[s] == 25:
                    print(f"Words: {words}. Tags:{tags}. s: {s}")
            words, tags = get_sentence(source_file)

        if found != len(sentences):
            raise ValueError(
                f"Found {found} sentences, expected to find {len(sentences)}"
            )

    with open(output_path, "w+", encoding="utf8") as output_file:
        i = 0
        try:
            for word_list, tags_list in sentences:
                for w, t in zip(word_list, tags_list):
                    print(f"{w} {t}", file=output_file)
                print(file=output_file)
                i += 1
        except ValueError:
            print(f"Error at index: {i}. Sentences[i]: {sentences[i]}")


get_sentences_from_file(
    source_file_path="/home/iker/Documents/absa_datasets/projections/en2es/DeepL.50000.original.mgiza.test.tsv",
    target_file_path="../100test/en2es.absa.test.SimAlign.txt",
    output_path="../100test/en2es.absa.test.mgiza_original.txt",
)


"""
get_sentences_from_file(
    source_file_path="/home/iker/Documents/absa_datasets/projections/en2es/DeepL.50000.translated.mgiza.test.tsv",
    target_file_path="../100test/en2es.absa.test.SimAlign.txt",
    output_path="../100test/en2es.absa.test.mgiza_translated.txt",
)
"""


get_sentences_from_file(
    source_file_path="/home/iker/Documents/absa_datasets/projections/en2es/DeepL.50000.original.fastalign.test.tsv",
    target_file_path="../100test/en2es.absa.test.SimAlign.txt",
    output_path="../100test/en2es.absa.test.fastalign_original.txt",
)

"""
get_sentences_from_file(
    source_file_path="/home/iker/Documents/absa_datasets/projections/en2es/DeepL.50000.translated.fastalign.test.tsv",
    target_file_path="../100test/en2es.absa.test.SimAlign.txt",
    output_path="../100test/en2es.absa.test.fastalign_translated.txt",
)
"""
