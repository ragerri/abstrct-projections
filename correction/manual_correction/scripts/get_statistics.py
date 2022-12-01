from typing import List, TextIO


def cohen_kappa(ann1, ann2):
    """Computes Cohen kappa for pair-wise annotators.
    :param ann1: annotations provided by first annotator
    :type ann1: list
    :param ann2: annotations provided by second annotator
    :type ann2: list
    :rtype: float
    :return: Cohen kappa statistic
    """
    count = 0
    for an1, an2 in zip(ann1, ann2):
        if an1 == an2:
            count += 1
    A = count / len(ann1)  # observed agreement A (Po)
    uniq = set(ann1 + ann2)
    E = 0  # expected agreement E (Pe)
    for item in uniq:
        cnt1 = ann1.count(item)
        cnt2 = ann2.count(item)
        count = (cnt1 / len(ann1)) * (cnt2 / len(ann2))
        E += count

    return round((A - E) / (1 - E), 4)


def get_sentence(file: TextIO) -> (List[str], List[str], List[str]):
    sentence: List[str] = []
    tags: List[str] = []

    line: str = file.readline().rstrip().strip()
    while line:
        word: str
        tag: str

        try:
            word, tag, _ = line.split("\t")
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


def compare(file_paths: List[str], annotators: List[str]):

    annotators_sentences = [get_all_sentences(f) for f in file_paths]

    for x in range(len(file_paths)):
        for i in range(x + 1, len(file_paths)):
            tags_annotator_1 = [
                item
                for sublist in [x[1] for x in annotators_sentences[x]]
                for item in sublist
            ]
            tags_annotator_2 = [
                item
                for sublist in [x[1] for x in annotators_sentences[i]]
                for item in sublist
            ]

            k = cohen_kappa(tags_annotator_1, tags_annotator_2)

            print(f"Cohen Kappa  {annotators[x]} - {annotators[i]} : {k}")

    for i in range(len(annotators_sentences[0])):
        words = annotators_sentences[0][i][0]
        tags = []
        for annotator in annotators_sentences:
            tags.append(annotator[i][1])

        if not all(x == tags[0] for x in tags):
            for i in range(len(words)):
                print(words[i], end=" ")

                for t in tags:
                    print(t[i], end=" ")
                print()
            print()


compare(
    file_paths=[
        "../100test/Iker.tsv",
        "../100test/Rodrigo.tsv",
        "../100test/German.tsv",
    ],
    annotators=["Iker", "Rodrigo", "German"],
)
