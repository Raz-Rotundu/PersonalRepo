import sys
import copy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # For each variable
        for variable in self.domains:
            # For every value in that word's domain
            domain_copy = copy.deepcopy(self.domains[variable])
            for word in domain_copy:
                # If item length does not match word length: remove rom domain
                if len(word) != variable.length:
                    self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # O is either a set (i, j) or None
        o = self.crossword.overlaps[x, y]
        if None in o:
            # No modification needed
            return False
        else:
            # Number of modifications made to x
            mods = 0
            # A copy of x's domain, since we'll be removing things from it on the fly
            xdomain = copy.deepcopy(self.domains[x])
            # For each word in x's domain
            for xval in xdomain:
                # Get its specified ith char
                i = xval[o[0]]
                # Number of matched in y for this variable
                count = 0
                for yval in self.domains[y]:
                    j = yval[o[1]]
                    # If the letters at the posistions match
                    if i == j:
                        count += 1
                # If this word for x has no matches in y at (i, j), remove it from x
                if count == 0:
                    self.domains[x].remove(xval)
                    mods += 1
            # If modification was made return true otherwise return false
            if mods != 0:
                return True
            else:
                return False

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # If no arcs were given, we take a queue of all possible variable combinations POTENTIAL PROBLEM
        if not arcs:
            q = self.buildqueue()
            # Then we arc evaluate the queue
            return self.arc_eval(q)
        else:
            return self.arc_eval(arcs)

    def buildqueue(self):
        """Creates a queue of every possible edge between self's variables by identifying neighbors. Reciprocals eliminated
        """
        # Will have 2 entries for each edge to represent direction
        Q = []
        for v in self.domains:
            neighbors = self.crossword.neighbors(v)
            if len(neighbors) != 0:
                for n in neighbors:
                    Q.append((v,n))
        return Q

    def arc_eval(self, queue):
        """A helper for the ac3 function.
        Takes a queue as argument
        carries out the operations, modifying self.domain variables as necessary
        return false if problem is unsilvable
        return true if successful
        """
        while len(queue) != 0:
            val = queue.pop(0)
            # The two variables we're checking
            x = val[0]
            y = val[1]
            # Making it arc consistent
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in (self.crossword.neighbors(x) - {y}):
                    queue.append((z, x))
        return True




    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Check each variable in assignment to make sure it has been assigned a word
        if len(assignment) != len(self.domains):
            return False
        for var in assignment:
            if assignment[var] is None:
                return False
        else:
            return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        return (self.check_unique(assignment) and self.check_length(assignment) and self.check_neighbors(assignment))

    def check_unique(self, assignment):
        """ Helper which checks that all values in list are unique
        return T if all are unique, F otherwise
        """
        vals = list(assignment.values())
        l = []
        for i in vals:
            if i not in l:
                l.append(i)
        return len(vals) == len(l)

    def check_length(self, assignment):
        """ Helper that checks that the word assigned to the variable is of correct length for variable
        returns T if all are proper length, F otherwise
        """
        for var in assignment:
            if len(assignment[var]) != var.length:
                return False
        return True

    def check_neighbors(self, assignment):
        """Runs check_conflict on the neighbors of each variable in assignment
        returns false on the first instance of a conflict picked up by check_conflict
        """
        for variable in assignment:
            n = self.crossword.neighbors(variable)
            for y in n:
                if self.check_conflict(variable, y):
                    return False
            return True

    def check_conflict(self, x, y):
        """Checks if there is a conflict between x and y
        returns true if conflict found
        returns flase if OK
        """
        o = self.crossword.overlaps[x,y]
        # If no overlap, there can't be conflict so auto false(no conflict)
        i = list(self.domains[x])
        j = list(self.domains[y])
        i = i[0]
        j = j[0]
        if not o:
            return False
        elif i[o[0]] != j[o[1]]:
            return True
        else:
            return False

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        elims = dict()
        words = self.domains[var]
        neighbors = self.crossword.neighbors(var)

        for neighbor in neighbors:
            # Only want blank neighbors
            if neighbor not in assignment:
                o = self.crossword.overlap[var, neighbor]
                for word in words:
                    if word not in elims:
                        elims[word] = self.count_elims(word, neighbor, o)
                    else:
                        elims += self.count_elims(word, neighbor, o)
        # sort it out, return the list of keys
        return sorted(elims)

    def count_elims(self, string, variable, overlap):
        """Takes a string, variable object, and an overlap value
        returns how many of variable's domain are ruled out given string and overlap
        """
        count = 0
        for word in self.domains[variable]:
            if string[overlap[0]] != word[overlap[1]]:
                count += 1
        return count

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        options = dict()
        # Filter out variable already assigned
        options = self.assign_elim(assignment)
        options = self.dict_sort(options)
        # Options now represents number of values for each var
        options = self.get_mins(options)
        # Options is now restored to its original format
        options = self.degree_sort(options)
        # Return the first one from the list of variables
        #Test
        k = list(options.keys())
        return k[0]

    def assign_elim(self, assignment):
        """ Returns a dictionary of all of self's variables which are not in assignment"""
        out = dict()
        for variable in self.domains:
            if variable not in assignment:
                out[variable] = self.domains[variable]
        return out

    def dict_sort(self, dictionary):
        """ Takes a dictionary with numerical values, returns it in ascending order"""
        # A dict where the value is the number of options a variable has
        temp = dict()
        for variable in dictionary:
            temp[variable] = len(dictionary[variable])

        out = dict(sorted(temp.items(), key = lambda x:x[1]))

        # Return the num value dict
        return out

    def get_mins(self, dictionary):
        """ Returns finds the minimal value and returns a dictionary of only those keys that have the minimal value """
        out = copy.deepcopy(dictionary)
        minimum = min(list(dictionary.values()))
        for variable in dictionary:
            if dictionary[variable] != minimum:
                out.pop(variable)
        return out

    def degree_sort(self, dictionary):
        """Sorts a dictionary's keys by the number of neighbors, leaves only the minimum"""
        degs = dict()

        # Make a dict mapping variables to number of neighbors they have
        for var in dictionary:
            degs[var] = len(self.crossword.neighbors(var))

        # Get the min
        minimum = min(list(degs.values()))
        # Copy out degs
        dcopy = copy.deepcopy(degs)

        # Clear out ones that don't satisfy min
        for var in dcopy:
            if dcopy[var] != minimum:
                degs.pop(var)

        # Return to variable - potential values format
        for var in degs:
            degs[var] = self.domains[var]

        return degs

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        # Get a A variable which is still blank
        var = self.select_unassigned_variable(assignment)

        # Possible answers for variable
        #Test
        t = self.domains
        p = self.domains[var]
        for val in p:
            assignment[var] = val
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result != None:
                    return result
                assignment.pop(var)
        return None








def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
