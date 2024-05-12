import io

import pytest
import ujson

from src.warc2text_runner.two.fastertext_lid.proto_langid import FastTextLangId


class TestFastTextLangId:
    def setup_method(self):
        model_path = "tests/test_langid_scripts/test_model/lid193_merged_arabics.bin"
        self.loaded_model = FastTextLangId(model_path=model_path)

    def _run_test(self, monkeypatch, stdin, expected_output) -> None:
        result = io.StringIO()
        monkeypatch.setattr("sys.stdin", io.StringIO(stdin))
        monkeypatch.setattr("sys.stdout", result)
        self.loaded_model.predict_language_from_stdin_jsonlines()
        assert result.getvalue() == expected_output

    def test_empty_text(self, monkeypatch) -> None:
        """
        Test the predict_language_from_stdin_jsonlines method. Test empty string case.
        """
        self._run_test(monkeypatch, '{"t":""}', '{"lang":["_unk"]}\n')

    def test_null_input(self, monkeypatch) -> None:
        """
        Test the predict_language_from_stdin_jsonlines method. Test null input case.
        """
        self._run_test(monkeypatch, '{"t":null}', '{"lang":null}\n')

    def test_sequence_of_texts(self, monkeypatch) -> None:
        """
        Test the predict_language_from_stdin_jsonlines method. Test sequence of texts case.
        """
        input_sequence = '{"t":"Привет! Меня зовут Юлия. Я изучаю эсперанто и хочу познакомиться с другими людьми, которые тоже изучают этот"}\n{"t":"язык."}\n{"t":"Hello! My name is Julia. I am studying Esperanto and want to meet other people who are also studying this language."}\n{"t":""}\n{"t": "汉语"}\n{"t": null}\n{"t":"Hello World. We can drink some tea. He likes ice-cream and potatoes."}\n{"t":"See\xa0what\'s hidden in your string…\tor be\u200bhind\ufeff"}\n'  # noqa: RUF001
        output_sequence = '{"lang":["rus_Cyrl","tat_Cyrl","tgk_Cyrl"],"prob":[0.9998,0.0001,0.0001]}\n{"lang":["rus_Cyrl","tat_Cyrl","bel_Cyrl"],"prob":[0.9995,0.0005,0.0]}\n{"lang":["eng_Latn","ibo_Latn","yor_Latn"],"prob":[0.9975,0.0004,0.0004]}\n{"lang":["_unk"]}\n{"lang":["zho_Hans","khm_Khmr","amh_Ethi"],"prob":[0.8893,0.107,0.0038]}\n{"lang":null}\n{"lang":["eng_Latn","swh_Latn","hau_Latn"],"prob":[0.9995,0.0001,0.0001]}\n{"lang":["eng_Latn","gaz_Latn","swh_Latn"],"prob":[0.9327,0.0447,0.0039]}\n'

        self._run_test(
            monkeypatch,
            input_sequence,
            output_sequence,
        )

    def _run_test_invalid_json(self, monkeypatch, invalid_jsonline) -> None:
        result = io.StringIO()
        monkeypatch.setattr("sys.stdin", io.StringIO(invalid_jsonline))
        monkeypatch.setattr("sys.stdout", result)

        with pytest.raises(ujson.JSONDecodeError):
            self.loaded_model.predict_language_from_stdin_jsonlines()

    def test_invalid_json(self, monkeypatch) -> None:
        """
        Test the predict_language_from_stdin_jsonlines method. Test invalid json case.
        """
        self._run_test_invalid_json(monkeypatch, '{"t":')
