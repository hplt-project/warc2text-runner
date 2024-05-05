"""The prototype script for language identification for warc2text-runner."""

from __future__ import annotations

import argparse
import fileinput
import ujson as json
import sys

import fasttext
import os


class FastTextLangId:
    """The FastText language identification model."""

    def __init__(self, model_path: str) -> None:
        """
        Init the FastText model.

        To download the model, run the following commands:
        wget https://data.statmt.org/lid/lid201-model.bin.gz
        pigz -d lid201-model.bin.gz

        Expected usage (stdin jsonlines):
        python proto_langid.py --model_path $MODEL_PATH < $YOUR_FILE

        """
        self.model = fasttext.load_model(model_path)

    def _preproccess_text(self, text: str) -> str:
        """Preprocesses the text. Naive cleaning."""
        return text.replace("\n", " ").strip()

    def _postprocess_prediction(self, prediction: tuple) -> str:
        """Postprocesses the prediction."""
        return prediction[0][0].split("__label__")[1]

    def predict_language_from_stdin_jsonlines(self) -> None:
        """
        Read from stdin jsonlines.

        Expected input: {"t":"text"}
        Expected output: {"lang":"en", "prob":0.9}

        Expected output(if None/null it "t" field): {"lang":null}
        Expected output(if empty string in "t" field): {"lang":"unk"}

        """
        with fileinput.input(files=("-",), encoding="utf-8") as f:
            for fileinput_line in f:
                json_line = json.loads(fileinput_line)

                if json_line["t"] is None:
                    print(json.dumps({'lang': None}))
                    sys.stdout.write('{"lang": null}\n')

                elif json_line["t"] == "":
                    print(json.dumps({'lang': '_unk'}))
                else:
                    prediction = self.model.predict(
                        text=self._preproccess_text(json_line["t"]),
                        k=1,
                        threshold=0.0,
                        on_unicode_error="strict",
                    )

                    print(json.dumps({'lang': self._postprocess_prediction(prediction), 'prob': round(prediction[1][0], 4)}))

        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict language using FastText model.")
    parser.add_argument(
        "--model_path",
        default=os.path.join(os.path.expanduser("~"), ".cache/hplt/lid201-model.bin"),
        help="Path to the FastText model file",
    )

    args = parser.parse_args()

    loaded_model = FastTextLangId(args.model_path)
    loaded_model.predict_language_from_stdin_jsonlines()
