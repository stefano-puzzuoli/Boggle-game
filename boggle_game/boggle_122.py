import sys

rows = 4
cols = 4
points_table = {0 : 0,
               1 : 0,
               2 : 0,
               3 : 1,
               4 : 1,
               5 : 2,
               6 : 3,
               7 : 5,
}

def make_grid(board):
    d = {}
    board = board.upper()
    board_groups = board[:4] + " " + board[4:8] + " " + board[8:12] + " " + board[12:16]
    board = board_groups.split()
    i = 0
    while i < rows:
       j = 0
       while j < cols:
          d[i,j] = board[i][j]
          j += 1
       i += 1
    return(d)
        
    


def neighbours_of_a_position(row, col):
    return [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
            (row, col - 1),                     (row, col + 1), 
            (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]


def all_grid_neighbours(grid):
    neighbours = {}
    for position in grid:
        row, col = position
        position_neighbours = neighbours_of_a_position(row, col)
        neighbours[position] = [p for p in position_neighbours if p in grid]
    return neighbours


def path_to_word(grid, path):
    return ''.join([grid[p] for p in path])


def is_a_real_word(word, dictionary):
    return word in dictionary


def search(grid, dictionary):
    neighbours = all_grid_neighbours(grid)
    paths = []
    full_words, stems = dictionary

    def do_search(path):
        word = path_to_word(grid, path)
        if is_a_real_word(word, full_words):
            paths.append(path)
        if word not in stems:
            return
        for next_pos in neighbours[path[-1]]:
            if next_pos not in path:
                do_search(path + [next_pos])
    for position in grid:
        do_search([position])
    words = []
    for path in paths:
        newword = path_to_word(grid, path)
        if len(newword) > 2:
            words.append(newword)
    return set(words)


def get_dictionary(dictionary_file):
   
    full_words, stems = set(), set()

    with open(dictionary_file) as f:
        for word in f:
            word = word.strip().upper()
            full_words.add(word)

            for i in range(1, len(word)):
                stems.add(word[:i])
    return full_words, stems


def display_points(words):

    max_points = 0
    for word in words:
       lenght = len(word)
       if lenght in points_table:
          max_points += points_table[lenght]
       else:
          max_points += 11
    print ("Possible points: {}".format(max_points))


def main():

    boards_file = sys.argv[1]
    dic_file = sys.argv[2]
    dictionary = get_dictionary(dic_file)
    with open(boards_file) as fin:
       for line in fin:
          line = line.strip()
          grid = make_grid(line)
          words = search(grid, dictionary)
          display_points(words)

if __name__ == '__main__':
   main()
