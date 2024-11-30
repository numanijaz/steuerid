# SteuerID

This package validates the German Tax-ID (Steueridentifikationsnummer / Steuer-ID).

Here is an example of how it can be used:

```python
from steuerid import SteuerIdValidator

validator = SteuerIdValidator()
validation_result = validator.validate("02476291358")

print(validation_result) # (True, None) -> the provided steuer id is valid

validation_result = validator.validate("x1234567890")
print(validation_result) # (False, OnlyDigitsAllowedException) -> invalid, only digits are allowed
```

By default, the test Steuer-IDs (starting with `0`) are allowed.
If you are using this in production, please set the `STEUERID_PRODUCTION`
environment variable to `True`.

## Development
For development first clone the repo. It would be better to create a virtual env
and activate that virtual env. Inside the venv install the dependencies using
`poetry install` command (poetry needs to be installed).

### Testing
Run `pytest` command to run the unit tests.
