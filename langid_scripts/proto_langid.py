"""The prototype script for language identification for warc2text-runner."""

from __future__ import annotations

import argparse
import fileinput

import fasttext
import numpy
import regex
import ujson

from langid_scripts.patterns import NONWORD_REPLACE_PATTERN


class FastTextLangId:
    """The FastText language identification model."""

    def __init__(self, model_path: str) -> None:
        """
        Init the FastText model.

        To download the model, run the following commands:
        wget https://data.statmt.org/lid/lid193_merged_arabics.bin

        Expected usage (stdin jsonlines):
        python -m langid_scripts.proto_langid --model_path $MODEL_PATH < $YOUR_FILE

        """
        self.model = fasttext.load_model(model_path)

    def _preproccess_text(self, text: str) -> str:
        """Preprocesses a single line of text for lang ID."""
        text = text.replace("\n", " ").strip()
        return regex.sub(NONWORD_REPLACE_PATTERN, "", text)

    def _postprocess_predicted_labels(self, prediction: tuple) -> list[str]:
        """
        Postprocess the predicted labels.

        Example: "__label__eng_Latn" -> "eng_Latn"
        """
        return [label[9:] for label in prediction[0]]

    def _postprocess_predicted_probabilities(self, prediction: tuple) -> list[float]:
        """
        Postprocess the predicted probabilities.

        Example: [0.92134414] -> [0.9213]
        """
        rounded_probs = numpy.round(prediction[1], decimals=4)

        return rounded_probs.tolist()

    def predict_language_from_stdin_jsonlines(self) -> None:
        """
        Read from stdin jsonlines.

        Example input:

        {"t": "Hello, world!"}

        Example output:

        {"lang": ["eng_Latn"], "prob": [0.9213]}

        """
        with fileinput.input(files=("-",), encoding="utf-8") as f:
            for fileinput_line in f:
                # load json line

                json_line = ujson.loads(fileinput_line)

                if json_line["t"] is None:
                    print(ujson.dumps({"lang": ["_null"]}))
                    continue

                if len(json_line["t"]) == 0:
                    print(ujson.dumps({"lang": ["_unk"]}))
                    continue

                prediction = self.model.predict(
                    text=self._preproccess_text(json_line["t"]),
                    k=3,
                    threshold=0.0,
                    on_unicode_error="strict",
                )

                print(
                    ujson.dumps(
                        {
                            "lang": self._postprocess_predicted_labels(prediction),
                            "prob": self._postprocess_predicted_probabilities(prediction),
                        }
                    )
                )

        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict language using FastText model.")
    parser.add_argument(
        "--model_path",
        default="models/lid193_merged_arabics.bin",
        help="Path to the FastText model file",
    )

    args = parser.parse_args()

    loaded_model = FastTextLangId(args.model_path)
    loaded_model.predict_language_from_stdin_jsonlines()
