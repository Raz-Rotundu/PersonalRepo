import itertools
import random
import copy

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
        # If the number of cells matches the number of bombs, they are all mines
        if len(self.cells) == self.count and self.count != 0:
            return self.cells
        else:
            # Otherwise we return empty set
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # If the count is 0 and number of cells is not 0, they are all safe
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            # Remove it from the sentence
            self.cells.remove(cell)
            # Remove one mine from the count
            self.count -= 1
        # Otherwise do nothing
        return

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            # Remove it
            self.cells.remove(cell)
            # Do not update mine count
        # Otherwise do nothing
        return


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
        # 1)
        self.moves_made.add(cell)
        # 2)
        self.mark_safe(cell)
        # 3) Get all of the cell's neighbors
        neighbors_tuple = self.get_undetermined_neighbors(cell)
        # Make sentence object and add to knowledge base
        s = Sentence(neighbors_tuple[0], count - neighbors_tuple[1])

        self.knowledge.append(s)

        # 4) Mark new safes and mines based on the sentences in knowledge
        self.update_safes_mines()

        # 5) Infer new sentences based on addition
        self.infer_new_sentences()


    def infer_new_sentences(self):
        """ Infers new sentences from existing knowledge base"""
        # A variable which prevents updating if no n is found
        n_found = False

        knowledge_copy = copy.deepcopy(self.knowledge)

        # For every combination of sentences
        for s in knowledge_copy:
            for k in knowledge_copy:
                # If s is a strict subset of k, subtract cells and counts
                s_cells = s.cells
                k_cells = k.cells
                # Must be a strict subset, exclude empty sets
                if (s_cells.issubset(k_cells)) and len(s.cells) != 0:
                    # create a new set from the subtraction of the two
                    n = k_cells.difference(s_cells)
                    c = k.count - s.count

                    new_sentence = Sentence(n,c)

                    # Add it to self.knowledge
                    self.knowledge.append(new_sentence)

                    # Remove s and k from knowledge( Eliminated by inference)
                    if k in self.knowledge:
                        self.knowledge.remove(k)
                    if s in self.knowledge:
                        self.knowledge.remove(s)

                    # Mark that an n is found
                    n_found = True

                    # Update safes and mines
                    self.update_safes_mines()

                    # Call the function again on the updated Knowledge base
                    self.infer_new_sentences()

    def update_safes_mines(self):
        """ Calculates new safes and mines based on the existing set of knowledge"""

        # Go through each sentence and evaluate their counts for safety and mins
        for s in self.knowledge:
            safes = s.known_safes()
            mines = s.known_mines()
            # If sentence indicates no mines, mark all as safe
            if len(safes) != 0:
                # copy out cells to avoid iteration issues
                scopy = copy.deepcopy(safes)
                for c in scopy:
                    self.mark_safe(c)
            # If sentence indicates all mines, mark all as mines
            elif len(mines) != 0:
                mcopy = copy.deepcopy(mines)
                for j in mcopy:
                    self.mark_mine(j)
                    #print("{} added to mines".format(str(j)))

    def get_undetermined_neighbors(self, cell):
        """ Returns set of all undetermined neighbors of a cell"""

        #coordinates
        ycord = cell[0]
        xcord = cell[1]

        # set of neighbors
        neighbors = set()

        #for each row
        for i in range((ycord - 1), (ycord + 2)):
            # If it is not in bounds
            if (i < 0) or (i > 7):
                continue
            # for each column
            for j in range((xcord - 1), (xcord + 2)):
                # If it is not in bounds
                if (j < 0) or (j > 7):
                    continue
                # Make sure we're not reading the current cell
                if (i,j) != cell:
                    neighbors.add((i,j))

         # Only let in the undetermined cells
         # Use copy to avoid iteration errors
        n_copy = copy.deepcopy(neighbors)

        mines_removed = 0

        for neighbor in n_copy:
            if neighbor in self.safes:
                neighbors.remove(neighbor)
            if neighbor in self.mines:
                neighbors.remove(neighbor)
                mines_removed += 1

        # Return tuple of neighbors, and number of mines removed to update count
        return (neighbors, mines_removed)



    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Get a safe cell, make sure it's not a move that's been made
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        # Otherwise return an empty set
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # A set storing all the valid moves
        moves = []

        # For every cell in the grid
        for i in range(self.height):
            for j in range(self.width):

                # Make sure it's not a mine or a move made
                if (i,j) not in self.moves_made:
                    if(i,j) not in self.mines:
                       moves.append((i,j))
        if len(moves) != 0:
            move = random.choice(moves)

            # TEST
            #print("Moving to {}".format(str(move)))

            return move
        else:
            return None
