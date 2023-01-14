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

    def validWidth(self, width: int, min=3, max=12) -> None:
        if width < min:
            print(
                f"The minimal number of columns is {min}, the width has been increased")
            width = min
        if width > max:
            print(
                f"The maximal number of columns is {max}, the width has been decreased")
            width = max
        return width

    def validHeight(self, height: int, min=3, max=10) -> None:
        if height < min:
            print(
                f"The minimal number of rows is {min}, the height has been increased")
            height = min
        if height > max:
            print(
                f"The maximal number of rows is {max}, the height has been decreased")
            height = max
        return height

    def validNumberOfBots(self, NumberOfBots, min=2, max=8) -> None:
        if NumberOfBots + self.getNumberOfPlayers() > max:
            print(
                f"The maximal amount of player is {max} including bots, the amount of bots has been decreased to {max - self.getNumberOfPlayers()}")
            NumberOfBots = max - self.getNumberOfPlayers()
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
        self.__NumberOfPlayers = value

    def setNumberOfBots(self, value: int) -> None:
        self.__NumberOfBots = value

    def setPlayerList(self, value: list) -> None:
        self.__PlayerList = value

    def createGrid(self) -> list:
        return [[Case(0, (x, y), Player(0)) for x in range(self.getWidth())]
                for y in range(self.getHeight())]

    def addbots(self, value: int) -> None:
        self.setNumberOfBots(self.validNumberOfBots(value))

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
                    coord[0] >= self.getHeight() or
                    coord[1] >= self.getWidth())

    def getNeighbours(self, coord: tuple) -> list:
        neighbours = []

        if coord[0]-1 >= 0:
            neighbours.append(self.getCell((coord[0]-1, coord[1])))

        if coord[1]-1 >= 0:
            neighbours.append(self.getCell((coord[0], coord[1]-1)))

        if coord[0]+1 < self.getHeight():
            neighbours.append(self.getCell((coord[0]+1, coord[1])))

        if coord[1]+1 < self.getWidth():
            neighbours.append(self.getCell((coord[0], coord[1]+1)))

        return neighbours

    def numberOfNeighbours(self, coord: tuple) -> int:
        return len(self.getNeighbours(coord))

    def getCell(self, coord: tuple) -> Case:
        # print(coord, self.getGrid())
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
            return

        cell.setPawnNumber(0)
        cell.setPlayer(Player(0))

        for neighbour in self.getNeighbours(coord):
            neighbour.setPlayer(player)
            neighbour.setPawnNumber(neighbour.getPawnNumber()+1)

        # prevent infinite recursion when game is over
        self.updatePlayers()
        if self.checkWin():
            return

        for neighbour in self.getNeighbours(coord):
            if self.inGrid(neighbour.getCoordinates()):
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


def yesNoInput(message: str) -> bool:
    while True:
        inp = input("\n" + message + " : (y/n)  ").lower()
        if inp == "y":
            return True
        if inp == "n":
            return False


def validNumberOfPlayers(NumberOfPlayers, min=2, max=8) -> None:
    if NumberOfPlayers < min:
        print(
            f"The minimal amount of player is {min}, the amount of player has been increased")
        NumberOfPlayers = min
    if NumberOfPlayers > max:
        print(
            f"The maximal amount of player is {max}, the amount of player has been decreased")
        NumberOfPlayers = max
    return NumberOfPlayers


def createGame(width: int, height: int, nbPlayer: int, bots: bool, nbBots: int = 0):
    Game = Jeu(width, height)

    Game.setNumberOfPlayers(nbPlayer)

    if bots:
        Game.addbots(nbBots)

    Game.createPlayerList()
    Game.display()
    return Game


def initializeGame():
    width = intInput("How many columns ? between 3 and 12")
    height = intInput("How many rows ? between 3 and 10")
    bots = yesNoInput("Do you want to play against bots ?")

    if bots:
        nbPlayer = validNumberOfPlayers(
            intInput("How many players ? minimum 1, maximum 7"),
            min=1, max=7)

        nbBots = intInput(
            f"you can add {8 - nbPlayer} Bots maximum, how many do you want to play against")
    else:
        nbPlayer = validNumberOfPlayers(
            intInput("How many players ? minimum 2"),
            min=2)
        nbBots = 0

    return createGame(width, height, nbPlayer, bots, nbBots)


def play():
    Game = initializeGame()

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
