alphabets = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]


def create_matrix(key, list)-> list[list]:
    """This fucntion creates a 5x5 matrix for a given key & a list of alphabets

    Args:
        key (string): A secret key of user
        list (list[char]): list of alphabets to complete the matrix
    
    Returns:
        matrix (list[list[char]]): A 5x5 matrix
    """
    matrix = []

    # A temporary list to store the alphabets before creating the matrix
    temp = []
    
    # Adding the key to the temp list
    for i in key:
        if i not in temp:
            temp.append(i)
            
    # Adding the alphabets to the temp list to complete the matrix
    for i in list:
        if i not in temp:
            temp.append(i)
            
    # Creating the matrix
    matrix = [temp[i : i + 5] for i in range(0, 25, 5)]
    
    return matrix


def print_matrix(matrix) -> None:
    """This function prints the matrix in a readable format

    Args:
        matrix (list[list[char]]): A 5x5 matrix
    """
    for i in matrix:
        print(" ".join(i))
        
    return None


key = "monarchy"

matrix = create_matrix(key, alphabets)

print_matrix(matrix)