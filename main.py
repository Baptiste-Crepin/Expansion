from Player import Player
from Case import Case
from Bot import Bot


class Jeu():
    def __init__(self, width: int, height: int) -> None:
        self.__width = self.validWidth(width)
        self.__height = self.validHeight(height)
        self.__grid = self.createGrid()
        self.__NumberOfPlayers = 0
        self.__NumberOfBots = 0
        self.__PlayerList = []

        while not self.engoughSpaceForPlayer():
            self.expandBoard(self.getWidth()+1, self.getHeight()+1)

    def validWidth(self, width) -> None:
        if width < 3:
            print("The minimal width is 3, the width has been increased")
            width = 3
        if width > 12:
            print("The maximal width is 12, the width has been decreased")
            width = 12
        return width

    def validHeight(self, height) -> None:
        if height < 3:
            print("The minimal height is 3, the height has been increased")
            height = 3
        if height > 10:
            print("The maximal height is 10, the height has been decreased")
            height = 10
        return height

    def validNumberOfPlayers(self, NumberOfPlayers) -> None:
        if NumberOfPlayers < 2:
            print(
                "The minimal amount of player is 2, the amount of player has been increased")
            NumberOfPlayers = 2
        if NumberOfPlayers > 8:
            print(
                "The maximal amount of player is 8, the amount of player has been decreased")
            NumberOfPlayers = 8
        return NumberOfPlayers

    def validNumberOfBots(self, NumberOfBots) -> None:
        if NumberOfBots + self.getNumberOfPlayers() > 8:
            print(
                "The maximal amount of player is 8 including bots, the amount of bots has been decreased")
            NumberOfBots = 8 - self.getNumberOfPlayers()
        return NumberOfBots

    def getWidth(self) -> int:
        return self.__width

    def getHeight(self) -> int:
        return self.__height

    def getGrid(self) -> list:
        return self.__grid

    def getNumberOfPlayers(self) -> int:
        return self.__NumberOfPlayers

    def getNumberOfBots(self) -> int:
        return self.__NumberOfBots

    def getPlayerList(self) -> int:
        return self.__PlayerList

    def setWidth(self, value: int) -> None:
        self.__width = value

    def setHeight(self, value: int) -> None:
        self.__height = value

    def setGrid(self, value: list) -> None:
        self.__grid = value

    def setNumberOfPlayers(self, value: int) -> None:
        self.__NumberOfPlayers = self.validNumberOfPlayers(value)

    def setNumberOfBots(self, value: int) -> None:
        self.__NumberOfBots = self.validNumberOfBots(value)

    def setPlayerList(self, value: list) -> None:
        self.__PlayerList = value

    def createGrid(self) -> list:
        return [[Case(0, (x, y), Player(0)) for x in range(self.getWidth())]
                for y in range(self.getHeight())]

    def addbots(self, value: int) -> None:
        print("The bots will be added the the players you already have")
        self.setNumberOfBots(value)

    def createPlayerList(self) -> list:
        playerList = [Player(x+1) for x in range(self.getNumberOfPlayers())]
        if self.getNumberOfBots() != 0:
            bots = [Bot(len(playerList)+x+1)
                    for x in range(self.getNumberOfBots())]
            playerList += bots
        self.__PlayerList = playerList

    def display(self) -> None:
        for row in self.getGrid():
            print(" | ".join(map(str, row)))
        print()

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

    def getCell(self, coord: tuple) -> Case:
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
                if cell.getPlayer().getNumber() == player.getNumber():
                    return True

        return False

    def updatePlayers(self) -> None:
        for player in self.getPlayerList():
            if not self.playerInGrid(player):
                print("LOST", player.getNumber())
                self.getPlayerList().remove(player)

    def checkWin(self):
        if len(self.getPlayerList()) == 1:
            return True
        return False


def intInput(message: str) -> int:
    try:
        return int(input("\n" + message + ":  "))
    except ValueError:
        return intInput("\nIncorect Value, please enter a number")


def yesNoInput(message: str) -> int:
    while True:
        inp = input("\n" + message + " : (y/n)  ").lower()
        if inp == "y":
            return True
        if inp == "n":
            return False


def createGame():
    Game = Jeu(intInput("width"), intInput("height"))
    Game.setNumberOfPlayers(intInput("player Number"))

    if yesNoInput("Do you want to play against bots ?"):
        Game.addbots(intInput("How many bots do you want ?"))

    Game.createPlayerList()
    Game.display()
    return Game


def play():
    Game = createGame()

    # play one time for all the players before checking and eliminating them
    for player in Game.getPlayerList():
        print(player.getNumber())
        if isinstance(player, Bot):
            coordo = player.pickCoordo(Game)
            while Game.placePawn(coordo, player) == False:
                coordo = player.pickCoordo(Game)
        else:
            coordo = (intInput("row")-1, intInput("Col")-1)
            while Game.placePawn(coordo, player) == False:
                coordo = (intInput("row")-1, intInput("Col")-1)

        Game.expandPawn(coordo, player)
        Game.display()

    # game loop until game is over
    while not Game.checkWin():
        for player in Game.getPlayerList():
            print(player.getNumber())
            if isinstance(player, Bot):
                coordo = player.pickCoordo(Game)
                while Game.placePawn(coordo, player) == False:
                    coordo = player.pickCoordo(Game)
            else:
                coordo = (intInput("row")-1, intInput("Col")-1)
                while Game.placePawn(coordo, player) == False:
                    coordo = (intInput("row")-1, intInput("Col")-1)

            Game.expandPawn(coordo, player)
            Game.display()
            Game.updatePlayers()

    print(
        f'The game has ended and Player {Game.getPlayerList()[0].getNumber()} Won')


if __name__ == "__main__":
    play()
