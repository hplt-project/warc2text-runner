"""Naive test for `proto_langid.py`."""

import pathlib
import subprocess

from langid_scripts.proto_langid import FastTextLangId


class TestFastTextLangId:
    def download_model(self) -> None:
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

        return None

    def setup_method(self):
        model_path = "tests/test_langid_scripts/test_model/lid193_merged_arabics.bin"
        self.loaded_model = FastTextLangId(model_path=model_path)

    def test_preprocess_text(self):
        """
        Test the _preproccess_text method.
        """
        text = """\nHello World\nЯ стану%,1твоим9героем лирическим\n!@£$%^&*()_+"""
        expected = "Hello World Я станутвоимгероем лирическим _"
        result = self.loaded_model._preproccess_text(text)
        assert result == expected

    def test_postprocess_predicted_labels(self):
        """
        Test the _postprocess_predicted_labels method.
        """
        prediction = (("__label__eng_Latn", "__label__mylang", "123456789magiclang"),)
        expected = ["eng_Latn", "mylang", "magiclang"]
        result = self.loaded_model._postprocess_predicted_labels(prediction)
        assert result == expected

    def test_postprocess_predicted_probabilities(self):
        """
        Test the _postprocess_predicted_probabilities method.
        """
        prediction = (("__label__eng_Latn",), [0.92134414, 0.07865586])
        expected = [0.9213, 0.0787]
        result = self.loaded_model._postprocess_predicted_probabilities(prediction)
        assert result == expected
