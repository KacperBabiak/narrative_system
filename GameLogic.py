class GameLogic:
    def __init__(self) -> None:
        self.characters = {}
        self.candles = 0
        self.first_candle_char = None

    def __init__(self,characters,candles = 0, character = None) -> None:
        self.characters = characters
        self.candles = candles
        self.first_candle_char = character