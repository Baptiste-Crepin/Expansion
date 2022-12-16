class Case():

    def __init__(self, pawnNumber: int, player: int):
        self.pawnNumber = pawnNumber
        self.player = player

    def getPawnNumber(self):
        return self.pawnNumber

    def getPlayer(self):
        return self.player

    def setPawnNumber(self, value: int):
        self.pawnNumber = value

    def setPlayer(self, value: int):
        self.player = value

    def __repr__(self):
        return str((self.getPawnNumber(), self.getPlayer()))


class Jeu():
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[Case(0, 0) for x in range(self.width)]
                     for y in range(self.height)]

    def display(self):
        for row in self.grid:
            print(" | ".join(map(str, row)))


if __name__ == "__main__":
    # import doctest
    # doctest.testmod(verbose=True)
    J1 = Jeu(3, 4)
    J1.display()
