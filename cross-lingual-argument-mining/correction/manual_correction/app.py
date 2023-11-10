import tkinter as tk
from tkinter import TclError, messagebox
import tkinter.font as TkFont
from sentence_reader import SentenceReader
import argparse
import sys


class App:
    def __init__(
        self,
        source_dataset: str,
        en_dataset: str,
        target_sentences: str,
        output_dataset: str,
        font_size: int = 22,
    ):

        self.sentence_reader = SentenceReader(
            source_dataset=source_dataset,
            en_dataset=en_dataset,
            target_sentences=target_sentences,
            output_dataset=output_dataset,
        )

        if (
            not self.sentence_reader.source_sentence
            and not self.sentence_reader.target_sentence
        ):
            messagebox.showinfo(title="End of dataset", message="End of dataset")
            sys.exit(0)

        (
            source_sentence_txt,
            en_sentence_txt,
            target_sentence_txt,
            tag_start,
            tag_end,
            en_tag_start,
            en_tag_end,
        ) = self.sentence_reader.format_app()

        root = tk.Tk()
        root.title(f"Manual annotation projection: {target_sentences}")
        try:
            img = tk.PhotoImage(file="AppIcon.png")
            root.tk.call("wm", "iconphoto", root._w, img)
        except:
            pass

        root.tk.call("tk", "scaling", 2.0)

        default_font = TkFont.nametofont("TkDefaultFont")
        default_font.configure(size=font_size, family="Times")

        text_default_font = TkFont.nametofont("TkTextFont")
        text_default_font.configure(size=font_size, family="Times")

        fixed_default_font = TkFont.nametofont("TkFixedFont")
        fixed_default_font.configure(size=font_size, family="Times")

        self.target_font = TkFont.Font(family="Times", size=font_size, weight="bold")

        self.en_text = tk.Text(
            root,
            wrap="word",
            exportselection=0,
            height=8,
            bg="light grey",
            highlightcolor="#32a836",
            highlightbackground="#32a881",
            yscrollcommand=True,
        )
        self.en_text.tag_configure(
            "TARGET", foreground="darkgreen", font=self.target_font
        )
        self.source_text = tk.Text(
            root,
            wrap="word",
            exportselection=0,
            height=8,
            bg="light grey",
            highlightcolor="red",
            highlightbackground="red4",
            yscrollcommand=True,
        )

        self.source_text.tag_configure(
            "TARGET", foreground="orange2", font=self.target_font
        )

        self.source_text.insert("insert", source_sentence_txt)
        self.source_text.pack()
        self.source_text.tag_add("TARGET", f"1.{tag_start}", f"1.{tag_end}")

        self.en_text.insert("insert", en_sentence_txt)
        self.en_text.pack()
        self.en_text.tag_add("TARGET", f"1.{en_tag_start}", f"1.{en_tag_end}")


        self.target_text = tk.Text(
            root,
            wrap="word",
            height=8,
            highlightcolor="blue",
            highlightbackground="blue4",
            selectbackground="orange",
            yscrollcommand=True,
        )

        self.target_text.insert("insert", target_sentence_txt)
        self.target_text.pack()

        self.button = tk.Button(root, text="Set Target", command=self.on_botton_hq)
        self.button.pack()

        self.button = tk.Button(
            root, text="Incorrect Translation", command=self.on_botton_lq
        )
        self.button.pack()

        root.mainloop()

    def on_botton_hq(self, event=None):
        self.on_botton(tag_quality="HighQuality")

    def on_botton_lq(self, event=None):
        self.on_botton(tag_quality="LowQuality")

    def on_botton(self, tag_quality: str):
        try:
            index_ranges, selected_text = (
                self.target_text.tag_ranges(tk.SEL),
                self.target_text.get(tk.SEL_FIRST, tk.SEL_LAST),
            )

            # print(
            #    f"Selected text [{index_ranges}]: {selected_text}. "
            # )

        except TclError:
            msg_box = messagebox.askquestion(
                title="No text selected",
                message="Are you sure that target in the source sentence is missing in the target sentence?",
                icon="warning",
            )
            if msg_box == "no":
                return

            index_ranges = (".-1", ".-1")

        (
            source_sentence_txt,
            en_sentence_txt,
            target_sentence_txt,
            tag_start,
            tag_end,
            en_tag_start,
            en_tag_end,
        ) = self.sentence_reader.step(
            start_index=int(str(index_ranges[0]).split(".")[-1]),
            end_index=int(str(index_ranges[1]).split(".")[-1]),
            en_start_index=int(str(index_ranges[0]).split(".")[-1]),
            en_end_index=int(str(index_ranges[1]).split(".")[-1]),
            tag_quality=tag_quality
        )

        if not source_sentence_txt and not target_sentence_txt:
            messagebox.showinfo(title="End of dataset", message="End of dataset")
            sys.exit(0)

        self.source_text.delete(1.0, "end")
        self.source_text.insert("insert", source_sentence_txt)
        self.source_text.tag_add("TARGET", f"1.{tag_start}", f"1.{tag_end}")

        self.en_text.delete(1.0, "end")
        self.en_text.insert("insert", en_sentence_txt)
        self.en_text.tag_add("TARGET", f"1.{en_tag_start}", f"1.{en_tag_end}")

        self.target_text.delete(1.0, "end")
        self.target_text.insert("insert", target_sentence_txt)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--source_dataset",
        type=str,
        required=True,
        help="Source dataset IOB2 format",
    )
    parser.add_argument(
        "--en_dataset",
        type=str,
        required=True,
        help="Englsih dataset IOB2 format",
    )

    parser.add_argument(
        "--target_sentences",
        type=str,
        required=True,
        help="Target sentences txt format",
    )

    parser.add_argument(
        "--output_dataset",
        type=str,
        required=True,
        help="Output path",
    )

    parser.add_argument(
        "--font_size",
        type=int,
        default=14,
        help="App font size",
    )

    args = parser.parse_args()

    app = App(
        source_dataset=args.source_dataset,
        en_dataset=args.en_dataset,
        target_sentences=args.target_sentences,
        output_dataset=args.output_dataset,
        font_size=args.font_size,
    )
