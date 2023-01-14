class Player():
    def __init__(self, number: int):
        self.__number = number
        self.__color = self.setColorFromNumber()

    def getNumber(self) -> int:
        return self.__number

    def getColor(self) -> str:
        return self.__color

    def setNumber(self, value: int) -> None:
        self.__number = value

    def setColor(self, value: str) -> None:
        self.__color = value

    def __repr__(self) -> str:
        return self.getColor()

    def setColorFromNumber(self) -> None:
        BLACK = "#FFFFFF"
        RED = "#c3463d"
        ORANGE = "#d26f34"
        YELLOW = "#efe743"
        GREEN = "#639d39"
        BLUE = "#1a6baa"
        PURPLE = "#6d3757"
        PINK = "#cc4a8a"
        TEAL = "#659bfc"
        colorList = [BLACK, RED, ORANGE,
                     YELLOW, GREEN,
                     BLUE, PURPLE,
                     PINK, TEAL]

        return colorList[self.getNumber()]
