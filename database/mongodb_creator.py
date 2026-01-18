class Creator:
    """
    The Creator class is responsible for creating and saving new data to the database,
    such as new players or world state changes.
    """
    def __init__(self, database=None):
        self.database = database
