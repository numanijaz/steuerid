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
