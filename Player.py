class Player():
    def __init__(self, number: int, color: str):
        self.__number = number
        self.__color = color

    def getNumber(self) -> int:
        return self.__number

    def getColor(self) -> str:
        return self.__color

    def setNumber(self, value: int) -> None:
        self.__number = value

    def setNumber(self, value: str) -> None:
        self.__color = value

    def __repr__(self) -> str:
        return self.getColor()
