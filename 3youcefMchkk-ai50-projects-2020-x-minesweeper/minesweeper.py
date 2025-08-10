import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # if the length of the sentence equals the count number then all the cells are mines
        if len(self.cells) == self.count :
            return self.cells

        return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        
        #if the count = 0 then all the cells are safe
        if self.count == 0:
            return self.cells
        
        return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells :
            self.cells.remove (cell)
            self.count = self.count - 1
        

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells :
            self.cells.remove (cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)



    


    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        
        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2) mark the cell as safe
        self.mark_safe(cell)

        # 3) add a new sentence to the AI's knowledge base bases on the value of 'cell' and 'count'

        neighbors = [(cell[0]-1 , cell[1]-1 ), 
                     (cell[0]-1 , cell[1] ) ,
                     (cell[0]-1 , cell[1]+1 ),
                     (cell[0] , cell[1]-1 ),
                     (cell[0] , cell[1] ),
                     (cell[0] , cell[1]+1 ) ,
                     (cell[0]+1 , cell[1]-1 ), 
                     (cell[0]+1 , cell[1] ) ,
                     (cell[0]+1 , cell[1]+1 ),
        
        ]
        undetermined_N = list ()
        tmp_count = count

        # check if the neighbors are in the frame
        # check if the cells aren't safe or mines
        for neighbor in neighbors :
            if neighbor[0] < self.height and neighbor[0] >= 0 and neighbor[1] < self.height and neighbor[1] >= 0:
                if neighbor in self.mines :
                    tmp_count = tmp_count - 1
                elif neighbor not in self.safes :
                    undetermined_N.append (neighbor)


        # create a sentence
        x = Sentence (undetermined_N , tmp_count)


        # add it to the knowledge
        self.knowledge.append (x)


        # 4) mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base

        self.mark_cells()


        # 5) add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge

        self.add_new_S()


        


    #part 04
    def mark_cells (self) :
        
        check = False

        for sentence in self.knowledge :

            
            if len(sentence.cells) != 0:
                if sentence.known_mines() != None :
                    tmp_mines = sentence.known_mines()
                    tmp_mines = tmp_mines.copy()

                    for cell in tmp_mines :
                        if cell not in self.mines :
                            check = True
                            self.mark_mine(cell) 

            
            if len(sentence.cells) != 0 :
                if sentence.known_safes () != None :
                    tmp_safes = sentence.known_safes ()
                    tmp_safes = tmp_safes.copy()

                    for cell in tmp_safes :
                        if cell not in self.safes :
                            check = True
                            self.mark_safe (cell)
        
        if check == True :
            self.mark_cells ()

        return check



    # part 05 : 
    def add_new_S (self) :
        i = 0

        for i in range(len(self.knowledge)) :
            for j in range(i+1,len(self.knowledge)) :

                if self.knowledge[i].cells.issubset(self.knowledge[j].cells) :
                    y = Sentence (self.knowledge[j].cells.difference(self.knowledge[i].cells) , self.knowledge[j].count - self.knowledge[i].count)
                    if y not in self.knowledge :
                        self.knowledge.append (y)
                        self.mark_cells()
                elif self.knowledge[j].cells.issubset(self.knowledge[i].cells) :
                    y = Sentence (self.knowledge[i].cells.difference(self.knowledge[j].cells) , self.knowledge[i].count - self.knowledge[j].count)
                    if y not in self.knowledge :
                        self.knowledge.append (y)
                        self.mark_cells()


        # remove useless cells
        x = Sentence (set() , 0)

        while x in self.knowledge :
            self.knowledge.remove(x)

        


    
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes :
            if cell not in self.moves_made:
                return cell

        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # make a list of all the possible moves
        possible_moves = list ()
        optimal_moves = list ()

        for i in range(self.height):
            for j in range(self.width) :
                possible_moves.append ((i ,j))

        # remove the made moves and the mine cells from the list


        for cell in possible_moves :
            if cell not in self.moves_made and cell not in self.mines :
                optimal_moves.append (cell)


        if len (optimal_moves) == 0 :
            return None

        return random.choice(optimal_moves)

