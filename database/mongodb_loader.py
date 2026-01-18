class Loader:
    """
    The Loader class is responsible for retrieving and loading game data from the database.
    """
    def __init__(self, database=None):
        self.database = database
