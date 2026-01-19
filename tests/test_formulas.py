import pytest
from common.utils import Utils
from game.info.formulas import Formulas
from game.info.loader import Loader
from network.modules import Constants

class TestFormulas:
    @pytest.fixture(autouse=True)
    def setup_loader(self):
        Loader()

    def test_level_exp_loading(self):
        assert len(Formulas.LEVEL_EXP) == Constants.MAX_LEVEL
        assert Formulas.LEVEL_EXP[0] == 0
        # Check some known values or just that it's increasing
        for i in range(1, len(Formulas.LEVEL_EXP)):
            assert Formulas.LEVEL_EXP[i] > Formulas.LEVEL_EXP[i-1]

    def test_exp_to_level(self):
        assert Formulas.exp_to_level(0) == 1
        assert Formulas.exp_to_level(10) == 1
        # Lvl 1: points = floor(0.25 * floor(1 + 300 * 2^(1/7))) 
        # 2^(1/7) approx 1.104
        # 300 * 1.104 = 331.2
        # floor(1 + 331) = 332
        # 0.25 * 332 = 83
        # LevelExp[1] = 83
        assert Formulas.exp_to_level(82) == 1
        assert Formulas.exp_to_level(83) == 2

    def test_next_exp(self):
        assert Formulas.next_exp(0) == Formulas.LEVEL_EXP[1]
        assert Formulas.next_exp(83) == Formulas.LEVEL_EXP[2]

    def test_prev_exp(self):
        assert Formulas.prev_exp(0) == 0
        assert Formulas.prev_exp(83) == 83
        assert Formulas.prev_exp(82) == 0

    def test_get_max_hit_points(self):
        assert Formulas.get_max_hit_points(1) == 39 + 30
        assert Formulas.get_max_hit_points(10) == 39 + 300

