"""Naive test for `proto_langid.py`."""

import io
import pathlib
import subprocess

from langid_scripts.proto_langid import FastTextLangId


class TestFastTextLangId:
    def download_and_load_model(self) -> FastTextLangId:
        # Create a directory for the model for testing
        test_model_dir = "tests/test_langid_scripts/test_model"
        model_dir = pathlib.Path(test_model_dir)
        model_dir.mkdir(parents=True, exist_ok=True)

        # Model URL
        model_url = "https://data.statmt.org/lid/lid193_merged_arabics.bin"
        model_bin = pathlib.Path(model_url).name  # MODEL_NAME.bin

        if not model_dir.joinpath(model_bin).is_file():
            # Download the model file
            subprocess.run(
                ["wget", "-P", str(model_dir), model_url],
                check=True,
            )

        return FastTextLangId(model_path=str(model_dir.joinpath(model_bin)))

    def setup_method(self):
        self.loaded_model = self.download_and_load_model()

    def test_preprocess_text(self):
        """
        Test the _preproccess_text method.
        """
        text = "\nHello World\n"
        expected = "Hello World"
        result = self.loaded_model._preproccess_text(text)
        assert result == expected

    def test_postprocess_prediction(self):
        """
        Test the _postprocess_prediction method.
        """
        prediction = (("__label__eng_Latn",),)
        expected = "eng_Latn"
        result = self.loaded_model._postprocess_prediction(prediction)
        assert result == expected

    def test_predict_language_from_stdin_jsonlines_none(self, monkeypatch) -> None:
        """
        Test the predict_language_from_stdin_jsonlines method. Test None/null case.
        """
        stdin = '{"t":null}\n'
        expected = '{"lang":null}\n'
        result = io.StringIO()

        monkeypatch.setattr("sys.stdin", io.StringIO(stdin))
        monkeypatch.setattr("sys.stdout", result)
        self.loaded_model.predict_language_from_stdin_jsonlines()
        assert result.getvalue() == expected

    def test_predict_language_from_stdin_jsonlines_empty(self, monkeypatch) -> None:
        """
        Test the predict_language_from_stdin_jsonlines method. Test empty string case.
        """
        stdin = '{"t":""}\n'
        expected = '{"lang":"unk"}\n'
        result = io.StringIO()

        monkeypatch.setattr("sys.stdin", io.StringIO(stdin))
        monkeypatch.setattr("sys.stdout", result)
        self.loaded_model.predict_language_from_stdin_jsonlines()
        assert result.getvalue() == expected

    def test_predict_language_from_stdin_jsonlines(self, monkeypatch) -> None:
        """
        Test the predict_language_from_stdin_jsonlines method.
        """
        stdin = '{"t":"Hello World. We can drink some tea. He likes ice-cream and potatoes."}\n'
        expected = '{"lang":"eng_Latn", "prob":0.9993}\n'
        result = io.StringIO()

        monkeypatch.setattr("sys.stdin", io.StringIO(stdin))
        monkeypatch.setattr("sys.stdout", result)
        self.loaded_model.predict_language_from_stdin_jsonlines()
        assert result.getvalue() == expected
