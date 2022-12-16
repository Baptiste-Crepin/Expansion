class Case():

    def __init__(self, pawnNumber: int, player: int) -> None:
        self.__pawnNumber = pawnNumber
        self.__player = player

    def getPawnNumber(self) -> int:
        return self.__pawnNumber

    def getPlayer(self) -> int:
        return self.__player

    def setPawnNumber(self, value: int) -> None:
        self.__pawnNumber = value

    def setPlayer(self, value: int) -> None:
        self.__player = value

    def __repr__(self) -> str:
        return str((self.getPawnNumber(), self.getPlayer()))


class Jeu():
    def __init__(self, width: int, height: int, NumberOfPlayers) -> None:
        self.__width = self.validWidth(width)
        self.__height = self.validHeight(height)
        self.__NumberOfPlayers = self.validNumberOfPlayers(NumberOfPlayers)
        print(self.__height)
        self.__grid = self.createGrid()

        while not self.engoughSpaceForPlayer():
            self.expandBoard(self.getWidth()+1, self.getHeight()+1)

    def getWidth(self) -> int:
        return self.__width

    def getHeight(self) -> int:
        return self.__height

    def getNumberOfPlayers(self) -> int:
        return self.__NumberOfPlayers

    def getGrid(self) -> list:
        return self.__grid

    def setWidth(self, value: int) -> None:
        self.__width = value

    def setHeight(self, value: int) -> None:
        self.__height = value

    def setNumberOfPlayers(self, value: int) -> None:
        self.__NumberOfPlayers = value

    def setGrid(self, value: list) -> None:
        self.__grid = value

    def createGrid(self) -> list:
        return [[Case(0, 0) for x in range(self.getWidth())]
                for y in range(self.getHeight())]

    def validWidth(self, width) -> None:
        if width < 3:
            self.setWidth(3)
            return self.getWidth()
        if width > 12:
            self.setWidth(12)
            return self.getWidth()

    def validHeight(self, height) -> None:
        if height < 3:
            self.setHeight(3)
            return self.getHeight()
        if height > 10:
            self.setHeight(10)
            return self.getHeight()

    def validNumberOfPlayers(self, NumberOfPlayer) -> None:
        if NumberOfPlayer < 2:
            self.setNumberOfPlayers(2)
            return self.getNumberOfPlayers()
        if NumberOfPlayer > 8:
            self.setNumberOfPlayers(8)
            return self.getNumberOfPlayers()

    def display(self) -> None:
        for row in self.getGrid():
            print(" | ".join(map(str, row)))

    def expandBoard(self, width: int, height: int):
        self.setWidth(width)
        self.setHeight(height)
        self.setGrid(self.createGrid())

    def engoughSpaceForPlayer(self) -> bool:
        if self.getWidth() * self.getHeight() >= self.getNumberOfPlayers():
            return True
        return False


if __name__ == "__main__":
    # import doctest
    # doctest.testmod(verbose=True)
    J1 = Jeu(1, 1, 9999)
    J1.display()
    print(J1.engoughSpaceForPlayer())
    J1.display()
    print(J1.getNumberOfPlayers())
