from __future__ import annotations
import sys
import fasttext
import fileinput
import argparse
import json


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


class FastTextLangId:
    def __init__(self, model_path: str | Path):
        """Initializes the FastText model.

        To download the model, run the following commands:
        wget https://data.statmt.org/lid/lid201-model.bin.gz
        pigz -d lid201-model.bin.gz

        Expected usage (stdin):
        python proto_langid.py --model_path $MODEL_PATH --mode stdin < $YOUR_FILE

        Expected usage (stdin jsonlines):
        python proto_langid.py --model_path $MODEL_PATH --mode stdin_jsonlines < $YOUR_FILE

        """

        print(f"Loading model from: {model_path}")
        self.model = fasttext.load_model(model_path)

    def _preproccess_text(self, text: str) -> str:
        """Preprocesses the text"""
        # TODO: Ask Laurie about prepeprocessing
        return text.replace("\n", " ").strip()

    def _postprocess_prediction(self, prediction: tuple) -> str:
        """Postprocesses the prediction."""
        return prediction[0][0].split("__label__")[1] + "\n"

    def predict_language_from_stdin(self) -> None:
        """Reads line by line from standard input and writes the predicted language to standard output."""

        with fileinput.input(files=("-",), encoding="utf-8") as f:
            for fileinput_line in f:
                prediction = self.model.predict(
                    self._preproccess_text(fileinput_line), k=1
                )
                sys.stdout.write(self._postprocess_prediction(prediction))

        return None

    def predict_language_from_stdin_jsonlines(self) -> None:
        """Reads line by line from standard input (expected jsonlines format {"t":"Your text"})
        and writes the predicted language to standard output.

        """

        with fileinput.input(files=("-",), encoding="utf-8") as f:
            for fileinput_line in f:
                json_line = json.loads(fileinput_line)

                if json_line["t"] is None:
                    sys.stdout.write("None\n")

                else:
                    prediction = self.model.predict(
                        self._preproccess_text(json_line["t"]), k=1
                    )
                    sys.stdout.write(self._postprocess_prediction(prediction))

        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Predict language using FastText model."
    )
    parser.add_argument(
        "--model_path",
        default="models/lid201-model.bin",
        help="Path to the FastText model file",
    )

    parser.add_argument(
        "--mode",
        default="stdin_jsonlines",
        choices=["stdin", "stdin_jsonlines"],
        help="Mode of input",
    )

    args = parser.parse_args()

    print("Started processing")

    loaded_model = FastTextLangId(args.model_path)

    if args.mode == "stdin":
        print(f"Reading from standard input! --mode is {args.mode}")
        loaded_model.predict_language_from_stdin()

    elif args.mode == "stdin_jsonlines":
        print(f"Reading from standard input (jsonlines)! --mode is {args.mode}")
        loaded_model.predict_language_from_stdin_jsonlines()

    else:
        raise NotImplementedError("Other input methods not implemented yet!")

    print("Finished processing")
