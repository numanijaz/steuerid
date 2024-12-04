import pytest

from steuerid import SteuerIdValidator

class TestValidSteuerId:
    @pytest.mark.parametrize("steuer_id", [
        '02476291358',
        '86095742719',
        '47036892816',
        '65929970489',
        '57549285017',
        '25768131411',
        '26954371827',
        '37396038422',
        '36594612769',
        '70761537429',
        '31580565947',
        '49735528659',
        '37358134207',
        '10456228370',
        '82240169524',
        '85826408911',
        '26083345737',
        '12345678920',
    ])
    def test_valid_general(self, steuer_id):
        is_valid, _ = SteuerIdValidator.validate(steuer_id)
        assert is_valid
