class Location:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __hash__(self):
        return hash(str(self.row) + str(self.col))

    def operation(self, other):
        return (self.row - other.row) + (self.col - other.col)

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __lt__(self, other):
        return self.operation(other) < 0

    def __gt__(self, other):
        return self.operation(other) > 0

    def __repr__(self) -> str:
        return f"({self.row}, {self.col})"
