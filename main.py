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


class Case():

    def __init__(self, pawnNumber: int, player: object) -> None:
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
        return str((self.getPawnNumber(), (self.getPlayer().getNumber(), self.getPlayer().getColor())))


class Jeu():
    def __init__(self, width: int, height: int, NumberOfPlayers: int) -> None:
        self.__width = self.validWidth(width)
        self.__height = self.validHeight(height)
        self.__NumberOfPlayers = self.validNumberOfPlayers(NumberOfPlayers)
        self.__grid = self.createGrid()

        while not self.engoughSpaceForPlayer():
            self.expandBoard(self.getWidth()+1, self.getHeight()+1)

    def validWidth(self, width) -> None:
        width = 3 if width < 3 else width
        width = 12 if width > 12 else width
        return width

    def validHeight(self, height) -> None:
        height = 3 if height < 3 else height
        height = 10 if height > 10 else height
        return height

    def validNumberOfPlayers(self, NumberOfPlayers) -> None:
        NumberOfPlayers = 2 if NumberOfPlayers < 2 else NumberOfPlayers
        NumberOfPlayers = 8 if NumberOfPlayers > 8 else NumberOfPlayers
        return NumberOfPlayers

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
        return [[Case(0, Player(0, "#FFFFFF")) for x in range(self.getWidth())]
                for y in range(self.getHeight())]

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

    def inGrid(self, coord: tuple) -> bool:
        return not (coord[0] <= 0 or
                    coord[1] <= 0 or
                    coord[0] >= self.getWidth() or
                    coord[1] >= self.getHeight())

    def NumberOfNeighbours(self, coord: tuple) -> int:
        neighbours = 4

        if coord[0]-1 < 0:
            neighbours -= 1
        if coord[1]-1 < 0:
            neighbours -= 1
        if coord[0]+1 >= self.getWidth():
            neighbours -= 1
        if coord[1]+1 >= self.getHeight():
            neighbours -= 1
        return neighbours


if __name__ == "__main__":
    J1 = Jeu(1, 1, 9999)
    J1.display()
    #print(J1.inGrid((2, 2)))
    #print(J1.NumberOfNeighbours((0, 0)))
    print(J1.NumberOfNeighbours((1, 1)))
    print(J1.NumberOfNeighbours((2, 1)))
    print(J1.NumberOfNeighbours((2, 2)))
