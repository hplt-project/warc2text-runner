import io

from langid_scripts.proto_langid import FastTextLangId


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
        self._run_test(monkeypatch, '{"t":null}', '{"lang":["_null"]}\n')

    def test_json_decode_error(self, monkeypatch) -> None:
        """
        Test the predict_language_from_stdin_jsonlines method. Test json decode error case.
        """
        self._run_test(monkeypatch, '{"t":', '{"lang":["_json_decode_error"]}\n')
