# Program for building and solving a maze.
from maze import Maze


def main():
    '''The main routine.'''
    maze = buildMaze("mazefile.txt")
    if maze.findPath():
        print("Path found....")
        maze.draw()
        # print("After reset....")
        # maze.reset()
        # maze.draw()
    else:
        print("Path not found....")
        maze.draw()


def buildMaze(filename):
    '''
    Builds a maze based on a text format in the given file.
    :param filename: str
    '''
    infile = open(filename, "r")

    # Read the size of the maze.
    nrows, ncols = readValuePair(infile)
    maze = Maze(nrows, ncols)

    # Read the starting and exit positions.
    row, col = readValuePair(infile)
    maze.setStart(row, col)
    row, col = readValuePair(infile)
    maze.setExit(row, col)

    # Read the maze itself.
    for row in range(nrows):
        line = infile.readline()
        for col in range(len(line)):
            if line[col] == "*":
                maze.setWall(row, col)

    # Close the maze file and return the newly constructed maze.
    infile.close()

    return maze


def readValuePair(infile):
    '''
    Extracts an integer value pair from the given input file.
    :param infile: str
    :return: tuple of ints
    '''
    line = infile.readline()
    valA, valB = line.split()
    return int(valA), int(valB)


# Call the main routine to execute the program.
main()
