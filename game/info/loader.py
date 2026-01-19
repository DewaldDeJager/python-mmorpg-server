import math
from game.info.formulas import Formulas
from network.modules import Constants

class Loader:
    """
    Responsible for loading hard-coded values into the global classes.
    """

    def __init__(self):
        self.load_levels()

    def load_levels(self) -> None:
        """
        Loads the levels into the Formulas global class. The formula has been taken from RuneScape
        experience formula. https://runescape.fandom.com/wiki/Experience
        """
        Formulas.LEVEL_EXP = [0] * Constants.MAX_LEVEL
        Formulas.LEVEL_EXP[0] = 0

        current_exp = 0
        for i in range(1, Constants.MAX_LEVEL):
            points = math.floor(0.25 * math.floor(i + 300 * math.pow(2, i / 7)))
            current_exp += points
            Formulas.LEVEL_EXP[i] = current_exp
