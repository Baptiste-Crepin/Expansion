from Player import Player
from Case import Case


class Jeu():
    def __init__(self, width: int, height: int, NumberOfPlayers: int) -> None:
        self.__width = self.validWidth(width)
        self.__height = self.validHeight(height)
        self.__NumberOfPlayers = self.validNumberOfPlayers(NumberOfPlayers)
        self.__PlayerList = self.createPlayerList()
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

    def getGrid(self) -> list:
        return self.__grid

    def getNumberOfPlayers(self) -> int:
        return self.__NumberOfPlayers

    def getPlayerList(self) -> int:
        return self.__PlayerList

    def setWidth(self, value: int) -> None:
        self.__width = value

    def setHeight(self, value: int) -> None:
        self.__height = value

    def setGrid(self, value: list) -> None:
        self.__grid = value

    def setNumberOfPlayers(self, value: int) -> None:
        self.__NumberOfPlayers = value

    def setPlayerList(self, value: list) -> None:
        self.__PlayerList = value

    def createGrid(self) -> list:
        return [[Case(0, (x, y), Player(0)) for x in range(self.getWidth())]
                for y in range(self.getHeight())]

    def createPlayerList(self) -> list:
        print("11", [Player(x+1) for x in range(self.getNumberOfPlayers())])
        return [Player(x+1) for x in range(self.getNumberOfPlayers())]

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
        return not (coord[0] < 0 or
                    coord[1] < 0 or
                    coord[0] >= self.getWidth() or
                    coord[1] >= self.getHeight())

    def getNeighbours(self, coord: tuple) -> list:
        neighbours = []

        if coord[0]-1 >= 0:
            neighbours.append(self.getCell((coord[0]-1, coord[1])))

        if coord[1]-1 >= 0:
            neighbours.append(self.getCell((coord[0], coord[1]-1)))

        if coord[0]+1 < self.getWidth():
            neighbours.append(self.getCell((coord[0]+1, coord[1])))

        if coord[1]+1 < self.getHeight():
            neighbours.append(self.getCell((coord[0], coord[1]+1)))

        return neighbours

    def numberOfNeighbours(self, coord: tuple) -> int:
        return len(self.getNeighbours(coord))

    def getCell(self, coord: tuple) -> object:
        return self.getGrid()[coord[0]][coord[1]]

    def placePawn(self, coord: tuple, player: Player) -> None:
        if not self.inGrid(coord):
            return False

        cell = self.getCell(coord)

        if cell.getPlayer().getNumber() != 0 and cell.getPlayer() != player:
            return False

        cell.setPawnNumber(cell.getPawnNumber() + 1)
        cell.setPlayer(player)

    def expandPawn(self, coord: tuple, player: Player) -> None:
        cell = self.getCell(coord)
        if self.numberOfNeighbours(coord) > cell.getPawnNumber():
            return False

        cell.setPawnNumber(0)
        cell.setPlayer(Player(0))

        for neighbour in self.getNeighbours(coord):
            neighbour.setPlayer(player)
            neighbour.setPawnNumber(neighbour.getPawnNumber()+1)
            self.expandPawn(neighbour.getCoordinates(), player)

    def playerInGrid(self, player):
        for row in self.getGrid():
            for cell in row:
                #print(cell.getPlayer(), player)
                if cell.getPlayer().getNumber() == player.getNumber():
                    return True

        return False

    def updatePlayers(self) -> None:
        for player in self.getPlayerList():
            if not self.playerInGrid(player):
                print("LOST", player)
                self.getPlayerList().remove(player)

    def checkWin(self):
        if len(self.getPlayerList()) == 1:
            #print(len(self.getPlayerList()), self.getPlayerList())
            return True
        return False


def play():
    G1 = Jeu(int(input("width")), int(input("height")),
             int(input("player Number")))
    P1 = G1.getPlayerList()[0]
    P2 = G1.getPlayerList()[1]
    print()
    print("First Display")
    G1.display()
    print()

    for player in G1.getPlayerList():
        coordo = (int(input("col"))-1, int(input("row"))-1)
        G1.placePawn(coordo, player)
        G1.expandPawn(coordo, player)
        G1.display()
        print()

    while not G1.checkWin():
        for player in G1.getPlayerList():
            print(player.getNumber())
            coordo = (int(input("col"))-1, int(input("row"))-1)
            G1.placePawn(coordo, player)
            G1.expandPawn(coordo, player)
            G1.display()
            G1.updatePlayers()
            print()


if __name__ == "__main__":
    play()
