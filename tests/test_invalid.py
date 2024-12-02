import pytest

from steuerid import SteuerIdValidator
from steuerid import STEUERID_PRODUCTION_ENV
from steuerid.exceptions import *


class TestInvalidSteuerId:
    validator = SteuerIdValidator()

    @pytest.mark.parametrize(
        ["steuer_id", "expected_exception"],
        [
            [None, EmptyInputException],
            ["", EmptyInputException],
            ["12.34.67.91", OnlyDigitsAllowedException],
            ["12/45/68/11", OnlyDigitsAllowedException],
            ["0", InvalidLengthException],
            ["1234", InvalidLengthException],
            ["11223456789", OnlyOneRepeatedDigitException],
            ["11113456789", InvalidDigitRepetitionException],
            ["21113456789", InvalidRepeatedDigitChainException],
            ["01234567800", InvalidChecksumDigitException],
        ]
    )
    def test_invalid_with_exception(self, steuer_id, expected_exception):
        is_valid, ex = self.validator.validate(steuer_id)
        assert not is_valid
        assert isinstance(ex, expected_exception)

    def test_no_test_id_allowed(self, monkeypatch):
        monkeypatch.setenv(STEUERID_PRODUCTION_ENV, "True")

        is_valid, ex = self.validator.validate("01234567899")
        assert not is_valid
        assert isinstance(ex, SteuerTestIdNotAllowedException)

        monkeypatch.setenv(STEUERID_PRODUCTION_ENV, "False")
    
    @pytest.mark.parametrize("steuer_id", [
        '12345678912',
        '98765432199',
        '01234567800',
        '65299970480',
        '26954371820',
        '37505648067',
        '11112345678',
        '11111345677',
        '11111145670',
        '11111115672',
        '11111111670',
        '11111111178',
        '11111111119',
        '12.345.678.911',
        '12-345-678-911',
        '123/456/78911',
    ])
    def test_invalid_general(self, steuer_id):
        is_valid, _ = self.validator.validate(steuer_id)
        assert not is_valid
