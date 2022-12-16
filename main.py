from Player import Player
from Case import Case


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
        return [[Case(0, (x, y), Player(0, "#FFFFFF")) for x in range(self.getWidth())]
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

    def placePawn(self, coord: tuple, player: Player) -> None:
        if not self.inGrid(coord):
            return False

        cell = self.getGrid()[coord[0]][coord[1]]
        cell.setPawnNumber(cell.getPawnNumber() + 1)
        cell.setPlayer(player)


if __name__ == "__main__":
    G1 = Jeu(1, 1, 9999)
    P1 = Player(1, "#FF0000")
    G1.display()
    print()
    # print(G1.inGrid((2, 2)))
    # print(G1.NumberOfNeighbours((0, 0)))
    # print(G1.NumberOfNeighbours((1, 1)))
    G1.placePawn((1, 1), P1)
    G1.display()
    print()
    G1.placePawn((1, 1), P1)
    G1.display()
