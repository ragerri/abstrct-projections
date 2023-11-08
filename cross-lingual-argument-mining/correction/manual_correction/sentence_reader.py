import os
import logging
from typing import List, TextIO
from utils import count_lines
from tqdm import tqdm


def count_number_of_sentences(input_path: str) -> int:
    if not os.path.exists(input_path):
        return -1
    else:
        num_sentences = 0
        with open(input_path, "r", encoding="utf8") as file:
            s, _, _ = get_sentence(file)
            while s:
                num_sentences += 1
                s, _, _ = get_sentence(file)

        return num_sentences


def get_sentence(file: TextIO) -> (List[str], List[List[int]], List[str]):
    sentence: List[str] = []
    tags: List[List[int]] = []
    tags_types: List[str] = []
    current_tag: List[int] = []

    line: str = file.readline().rstrip().strip()
    while line:
        word: str
        tag: str
        try:
            word, tag = line.split()
        except ValueError:
            try:
                word, tag, q = line.split()
            except ValueError:
                raise ValueError(f"Error splitting line: {line}")

        if tag == "O":
            if len(current_tag) > 0:
                tags.append(current_tag)
                current_tag = []

        elif tag.startswith("B"):
            if len(current_tag) > 0:
                tags.append(current_tag)
                current_tag = []

            current_tag.append(len(sentence))

            try:
                _, t = tag.split("-")
            except ValueError:
                raise ValueError(f"Unable to split tag: {tag} from line: {line}")

            tags_types.append(t)

        elif tag.startswith("I"):
            current_tag.append(len(sentence))

        else:
            raise ValueError(f"Invalid tag. Word: {word}. Tag: {tag}")

        sentence.append(word)

        line = file.readline().rstrip().strip()

    if len(current_tag) > 0:
        tags.append(current_tag)

    return sentence, tags, tags_types


def get_line(file: TextIO) -> (List[str], str):
    # Multiple whitespace 2 whitespace and split
    target_sentence_txt = " ".join(file.readline().rstrip().strip().split())
    return target_sentence_txt.split(), target_sentence_txt


class SentenceReader:

    source_file: TextIO
    en_file: TextIO
    target_file: TextIO
    output_path: str
    sentence_no: int

    source_sentence: List[str]
    source_sentence_tags: List[List[int]]
    en_sentence: List[str]
    en_sentence_tags: List[List[int]]
    target_sentence: List[str]
    target_sentence_txt: str
    target_sentence_tags: List[List[int]]
    target_sentence_tags_types: List[str]
    target_sentence_tags_quality: List[str]
    current_tag: int
    en_cur_tag: int
    total_sentences: int
    en_sentences: int
    pbar: tqdm

    def __init__(self, source_dataset: str, en_dataset: str, target_sentences: str, output_dataset: str):

        self.output_path = output_dataset
        self.total_sentences = count_number_of_sentences(source_dataset)
        total_translated_sentences = count_lines(target_sentences)
        self.en_sentences = count_number_of_sentences(en_dataset)

        if not os.path.exists(os.path.dirname(output_dataset)):
            os.makedirs(os.path.dirname(output_dataset))

        assert self.total_sentences == total_translated_sentences and self.total_sentences == self.en_sentences, (
            f"Number of sentences in the source and target datasets must be the same. "
            f"Number of lines in the source dataset: {self.total_sentences}. "
            f"Number of lines in the target dataset: {total_translated_sentences}."
            f"Number of lines in the english dataset: {self.en_sentences}."
        )
        self.sentence_no = count_number_of_sentences(output_dataset)
        assert self.sentence_no < self.total_sentences, (
            f"There are more sentences in the output dataset that the "
            f"number of sentences in the source dataset!!! Unable to restore "
            f"from checkpoint, are you sure that you are using the correct"
            f"dataset paths?"
        )
        self.source_file = open(source_dataset, "r", encoding="utf8")
        self.en_file = open(en_dataset, "r", encoding="utf8")
        self.target_file = open(target_sentences, "r", encoding="utf8")

        if self.sentence_no >= 1:
            logging.info(
                "Output dataset found, we will restore from the last annotated sentence"
            )

            current_sentence: int = 0
            while current_sentence < self.sentence_no:
                while self.source_file.readline().rstrip().strip():
                    pass
                next(self.target_file)
                current_sentence += 1

            current_sentence: int = 0
            while current_sentence < self.sentence_no:
                while self.en_file.readline().rstrip().strip():
                    pass
                # next(self.target_file)
                current_sentence += 1

        self.pbar = tqdm(total=self.total_sentences - self.sentence_no)
        (
            self.source_sentence,
            self.source_sentence_tags,
            self.source_sentence_tags_types,
        ) = get_sentence(self.source_file)
        (
            self.en_sentence,
            self.en_sentence_tags,
            self.en_sentence_tags_types,
        ) = get_sentence(self.en_file)
        self.current_tag = 0
        self.en_cur_tag = 0
        self.target_sentence, self.target_sentence_txt = get_line(self.target_file)
        self.target_sentence_tags = []
        self.target_sentence_tags_types = []
        self.target_sentence_tags_quality = []

        while len(self.source_sentence_tags) == 0:
            if not self.source_sentence:
                break

            self.write_sentence()
            self.get_next_sentence()
       

        self.skip_sentences()

    def format_app(self):
        source_sentence_start = " ".join(
            self.source_sentence[: self.source_sentence_tags[self.current_tag][0]]
        )

        source_sentence_tag = " ".join(
            self.source_sentence[
                self.source_sentence_tags[self.current_tag][
                    0
                ] : self.source_sentence_tags[self.current_tag][-1]
                + 1
            ]
        )

        source_sentence_end = " ".join(
            self.source_sentence[self.source_sentence_tags[self.current_tag][-1] + 1 :]
        )

        source_sentence_txt = (
            source_sentence_start
            + " [ "
            + source_sentence_tag
            + " ] "
            + source_sentence_end
        )
    
        en_sentence_start = " ".join(
            self.en_sentence[: self.en_sentence_tags[self.en_cur_tag][0]]
        )

        en_sentence_tag = " ".join(
            self.en_sentence[
                self.en_sentence_tags[self.en_cur_tag][
                    0
                ] : self.en_sentence_tags[self.en_cur_tag][-1]
                + 1
            ]
        )

        en_sentence_end = " ".join(
            self.en_sentence[self.en_sentence_tags[self.en_cur_tag][-1] + 1 :]
        )

        en_sentence_txt = (
            en_sentence_start
            + " [ "
            + en_sentence_tag
            + " ] "
            + en_sentence_end
        )
        return (
            source_sentence_txt,
            en_sentence_txt,
            self.target_sentence_txt,
            len(source_sentence_start) + 1,
            len(source_sentence_start) + len(source_sentence_tag) + 5,
            len(en_sentence_start) + 1,
            len(en_sentence_start) + len(en_sentence_tag) + 5,
        )

    def get_next_tag(self):
        if self.current_tag + 1 >= len(self.source_sentence_tags):
            self.write_sentence()
            return self.get_next_sentence()

        self.current_tag += 1
        self.en_cur_tag += 1

    def skip_sentences(self):

        # SKIP SENTENCE IF NO LABELS

        if (
            len(self.source_sentence_tags) == 0
            and self.source_sentence
            and self.target_sentence
        ):
            self.write_sentence()
            self.get_next_sentence()

        # SKIP SENTENCE IF ALL THE SENTENCE IS A LABELLED SEQUENCE

        if (
            len(self.source_sentence_tags) == 1
            and self.source_sentence_tags[0][0] == 0
            and self.source_sentence_tags[0][-1] == len(self.source_sentence) - 1
        ):
            label = self.source_sentence_tags_types[0]
            self.target_sentence_tags_types.append(label)
            self.target_sentence_tags_quality.append("HighQuality")
            self.target_sentence_tags.append(list(range(len(self.target_sentence))))
            self.write_sentence()
            self.get_next_sentence()

    def get_next_sentence(self):
        self.pbar.update(1)
        self.sentence_no += 1
        (
            self.source_sentence,
            self.source_sentence_tags,
            self.source_sentence_tags_types,
        ) = get_sentence(self.source_file)

        (
            self.en_sentence,
            self.en_sentence_tags,
            self.en_sentence_tags_types,
        ) = get_sentence(self.en_file)
        
        self.current_tag = 0
        self.en_cur_tag = 0
        self.target_sentence, self.target_sentence_txt = get_line(self.target_file)
        self.target_sentence_tags = []
        self.target_sentence_tags_types = []
        self.target_sentence_tags_quality = []

        self.skip_sentences()

    def write_sentence(self):
        with open(self.output_path, "a+", encoding="utf8") as output_file:

            flat_target = [
                item for sublist in self.target_sentence_tags for item in sublist
            ]

            if len(flat_target) != len(set(flat_target)):

                raise ValueError(
                    f"Collision between tags, entity overlap not allowed. "
                    f"A word cannot belong to more than one entity. "
                    f"target_sentence_tags: {self.target_sentence_tags}"
                )

            target_tags = ["O\t-"] * len(self.target_sentence)

            for tag_indexes, target_type, target_quality in zip(
                self.target_sentence_tags,
                self.target_sentence_tags_types,
                self.target_sentence_tags_quality,
            ):
                first = True
                for i in sorted(tag_indexes):
                    if first:
                        target_tags[i] = f"B-{target_type}\t{target_quality}"
                        first = False
                    else:
                        target_tags[i] = f"I-{target_type}\t{target_quality}"

            print(
                "\n".join(
                    [
                        f"{word}\t{tag}"
                        for word, tag in zip(self.target_sentence, target_tags)
                    ]
                )
                + "\n",
                file=output_file,
            )

    def step(self, start_index: int, end_index: int, tag_quality: str, en_start_index: int, en_end_index: int,):
        if start_index != -1 and end_index != -1:

            assert start_index < end_index, (
                f"Start index should be < than end index. "
                f"start_index: {start_index} "
                f"end_index: {end_index}"
            )

            assert tag_quality in ["HighQuality", "LowQuality"]

            if en_start_index != -1 and en_end_index != -1:

                assert en_start_index < en_end_index, (
                    f"Start index should be < than end index. "
                    f"start_index: {en_start_index} "
                    f"end_index: {en_end_index}"
            )

            # Get words
            start_word = -1
            end_word = -1

            num_characters = 0

            # Remove whitespaces from start_index
            if start_index < 0:
                start_index = 0
            while self.target_sentence_txt[start_index] == " ":
                start_index += 1
            # Remove whitespaces from  end_index
            end_index -= (
                1  # The cursor is always 1 postion after the last selected word
            )
            if end_index >= len(self.target_sentence_txt):
                end_index = len(self.target_sentence_txt) - 1
            while self.target_sentence_txt[end_index] == " ":
                end_index -= 1

            en_start_word = -1
            en_end_word = -1

            num_characters = 0

            # Remove whitespaces from start_index
            if en_start_index < 0:
                en_start_index = 0
            while self.target_sentence_txt[en_start_index] == " ":
                en_start_index += 1
            # Remove whitespaces from  end_index
            en_end_index -= (
                1  # The cursor is always 1 postion after the last selected word
            )
            if en_end_index >= len(self.target_sentence_txt):
                en_end_index = len(self.target_sentence_txt) - 1
            while self.target_sentence_txt[en_end_index] == " ":
                en_end_index -= 1

            # Find span
            for word_no, word in enumerate(self.target_sentence):
                if num_characters <= start_index <= num_characters + len(word):
                    if start_word >= 0:
                        raise ValueError(
                            "Error getting selected word.\n"
                            f"target_sentence: {self.target_sentence}\n"
                            f"word: {word}\n"
                            f"word_no: {word_no}\n"
                            f"start_index*: {start_index}\n"
                            f"end_index: {end_index}\n"
                            f"start_word: {start_word}\n"
                            f"end_word: {end_word}\n"
                            f"num_characters: {num_characters}\n"
                        )
                    start_word = word_no
                if num_characters <= end_index <= num_characters + len(word):
                    if end_word >= 0:
                        raise ValueError(
                            "Error getting selected word.\n"
                            f"target_sentence: {self.target_sentence}\n"
                            f"word: {word}\n"
                            f"word_no: {word_no}\n"
                            f"start_index: {start_index}\n"
                            f"end_index*: {end_index}\n"
                            f"start_word: {start_word}\n"
                            f"end_word: {end_word}\n"
                            f"num_characters: {num_characters}\n"
                        )
                    end_word = word_no

                num_characters += len(word) + 1

            assert (end_word >= 0 and start_word >= 0) and (start_word <= end_word), (
                "Error getting selected word.\n"
                f"target_sentence: {self.target_sentence}\n"
                f"start_index: {start_index}\n"
                f"end_index: {end_index}\n"
                f"start_word: {start_word}\n"
                f"end_word: {end_word}\n"
            )

            self.target_sentence_tags.append(list(range(start_word, end_word + 1)))
            self.target_sentence_tags_types.append(
                self.source_sentence_tags_types[self.current_tag]
            )

            self.target_sentence_tags_quality.append(tag_quality)

            # print(f"target_sentence_tags: {self.target_sentence_tags}")
            # print(f"target_sentence_tags_types: {self.target_sentence_tags_types}")
            # print(f"target_sentence_tags_quality: {self.target_sentence_tags_quality}")

        self.get_next_tag()

        return (
            self.format_app()
            if self.source_sentence and self.target_sentence
            else (None, None, None, None, None, None, None)
        )
