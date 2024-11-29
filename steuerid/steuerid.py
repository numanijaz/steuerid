#!/usr/bin/env python

"""
This module contains the SteuerId class that contains
the logic to validate a given Steuer-ID. It solely checks the
structural validations but does not checks if the provided Steuer-ID
is actually assigned to a person or not.
"""

from os import environ
from collections import Counter

from exceptions import *

STEUER_ID_LENGTH = 11
PRODUCTION = environ.get("STEUERID_PRODUCTION", False)


class SteuerIdValidator:
    def _validate_structure(self, steuer_id: str) -> None:
        """
        Performs following checks on steuer_id:
        1. steuer_id is not empty.
        2. Length of steuer_id is valid.
        3. steuer_id does not contain characters other than digits.

        Args:
            steuer_id (str): The Steuer-ID to check the structure for.

        Raises:
            EmptyInput: raised if the Steuer-ID is empty.
            InvalidLength: raised if the length of Steuer-ID is invalid.
            OnlyDigitsAllowed: raised if the Steuer-ID contains character(s)
                that are not digits.

        Returns:
            bool
        """
        if not steuer_id:
            raise EmptyInputException

        if not len(steuer_id) == STEUER_ID_LENGTH:
            raise InvalidLengthException

        if not steuer_id.isdigit():
            raise OnlyDigitsAllowedException

    def _validate_test_id(self, steuer_id: str) -> None:
        """Checks if PRODUCTION mode is on, then no test steuer_id is provided.

        Args:
            steuer_id (str)

        Raises:
            TestSteuerIDNotAllowed: raised if its PRODUCTION environment and
            test steuer_id (starting with '0') is provided.
        """
        if PRODUCTION and steuer_id[0] == '0':
            raise TestSteuerIDNotAllowedException

    def _validate_digit_repetitions(self, steuer_id: str) -> None:
        """
        Performs the following checks on steuer_id:
        1. One and only one digit is repeating in first 10 digits of steuer_id.
        2. The repeating digit occurs maximum of 3 times.
        3. If the repeating digit occurs 3 times then this repetition should not
        be consecutive.

        Args:
            steuer_id (str)

        Raises:
            OnlyOneRepeatedDigit
            InvalidDigitRepetition
            InvalidRepeatedDigitChain
        """
        first_ten_digits = steuer_id[:10]
        digit_counts = Counter(first_ten_digits)
        repeated_digit_counts = {
            k: v for k, v in digit_counts.items()
            if v > 1
        }

        if len(repeated_digit_counts) != 1:
            raise OnlyOneRepeatedDigitException

        repeated_digit = next(iter(repeated_digit_counts))
        digit_repetitions = repeated_digit_counts[repeated_digit]
        if digit_repetitions not in [2, 3]:
            raise InvalidDigitRepetitionException

        if digit_repetitions == 3 and repeated_digit * digit_repetitions in steuer_id:
            raise InvalidRepeatedDigitChainException

    def _get_checksum_digit(self, steuer_id: str) -> int:
        """Computes the checksum digit based on ELSTER algorithm.

        Args:
            steuer_id (str)

        Returns:
            int: the checksum digit.
        """
        product = STEUER_ID_LENGTH - 1
        modulo = STEUER_ID_LENGTH - 1

        for c in steuer_id[:10]:
            digit = int(c)
            summ = (digit + product) % modulo
            if summ == 0:
                summ = modulo
            product = (2 * summ) % STEUER_ID_LENGTH

        checksum_digit = STEUER_ID_LENGTH - product
        return 0 if checksum_digit == modulo else checksum_digit

    def _validate_checksum_digit(self, steuer_id: str) -> None:
        """
        Validates if the last digit in steuer_id is valid using
        the validation algorithm provided by ELSTER.

        Args:
            steuer_id (str)

        Raises:
            InvalidCheksumDigit
        """
        if steuer_id[-1] != str(self._get_checksum_digit(steuer_id)):
            raise InvalidCheksumDigitException

    def validate(self, steuer_id: str) -> tuple[bool, Exception]:
        """
        Validates the steuer_id based on criterion provided by ELSTER
        handbook (Pruefung_der_Steuer_und_Steueridentifikatsnummer.pdf).

        Args:
            steuer_id (str)

        Returns:
            tuple[bool, Exception]: A tuple where first element is a
            boolean indicating the status of validation. If the validtion
            encountered errors, the second element in the tuple contains
            the Exception object.
        """
        try:
            self._validate_structure(steuer_id)
            self._validate_test_id(steuer_id)
            self._validate_digit_repetitions(steuer_id)
            self._validate_checksum_digit(steuer_id)

            # validation went through
            return True, None
        except SteuerIDValidationException as ex:
            return False, ex
        except:
            raise
