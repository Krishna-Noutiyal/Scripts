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


def create_matrix(key: str, lst: list) -> list[list]:
    """This fucntion creates a 5x5 matrix for a given key & a list of alphabets

    Args:
        key (string): A secret key of user
        lst (list[char]): list of alphabets to complete the matrix

    Returns:
        matrix (list[list[char]]): A 5x5 matrix
    """
    matrix = []

    # A temporary list to store the alphabets before creating the matrix
    temp = []

    # lower the key
    key = key.lower()

    # Adding the key to the temp list
    for i in key:
        if i not in temp:
            temp.append(i)

    # Adding the alphabets to the temp list to complete the matrix
    for i in lst:
        if i not in temp:
            temp.append(i)

    # Creating the matrix
    matrix = [temp[i : i + 5] for i in range(0, 25, 5)]

    return matrix


def search_matrix(pair: str, matrix: list[list]) -> list[list[int]]:
    """Searches the matrix for the given pair of characters
    and returns their respective row & column number

    Args:
        pair (str): It includes a pair of character eg. "ab","sa","gf" etc.
        matrix (list[list]): A matrix created by the create_matrix function

    Returns:
        list[list[int]]: This contains the row and column number of the pair eg. [[3,5],[4,2]].
    """
    pair = pair.lower()
    al1 = pair[0]
    al2 = pair[1]

    for i in matrix:
        if al1 == "j":
            row1 = -1
            col1 = -1
        elif al2 == "j":
            row2 = -1
            col2 = -1
        if al1 in i:
            row1 = matrix.index(i)
            col1 = i.index(al1)
        if al2 in i:
            row2 = matrix.index(i)
            col2 = i.index(al2)

    return [[row1, col1], [row2, col2]]


def encrypt_pair(pair: str, matrix: list[list]) -> str:
    """This function encrypts a pair of characters using the Playfair Cipher
    algorithm. It takes a pair of characters and a 5x5 matrix as input.

    Args:
        pair (str): This is a pair of charcters eg. "ab","sa","gf" etc.
        matrix (list[list]): A 5x5 matrix created by the create_matrix function

    Returns:
        str: A pair of encrypted characters eg. "ab"->"bd","sa"->"ar" etc.
    """
    al1, al2 = search_matrix(pair, matrix)
    char1_row, char1_col = al1[0], al1[1]
    char2_row, char2_col = al2[0], al2[1]
    
    if al1[0] == [-1,-1] :
        pass
    elif al2[0] == [-1,-1]:
        pass
    elif al1[0] == al2[0]:
        enc_char1 = matrix[char1_row][(char1_col + 1) % 5]
        enc_char2 = matrix[char2_row][(char2_col + 1) % 5]
    elif al1[1] == al2[1]:
        enc_char1 = matrix[(char1_row + 1) % 5][char1_col]
        enc_char2 = matrix[(char2_row + 1) % 5][char2_col]
    else:
        enc_char1 = matrix[char2_row][char1_col]
        enc_char2 = matrix[char1_row][char2_col]

    return enc_char1 + enc_char2


def print_matrix(matrix) -> None:
    """This function prints the matrix in a readable format

    Args:
        matrix (list[list[char]]): A 5x5 matrix
    """
    for i in matrix:
        print(" ".join(i))

    return None


def get_cipher(text: str,matrix:list[list[int]]) -> str:
    """Converts plain text into cypher text

    Args:
        text (str): The string to be encrypted
        matrix (list[list[int]]) : A matrix created by create_matrix function
    Returns:
        str: The encrypted string
    """

    pair_list = list(
        map(
            lambda x: x if len(x) == 2 else x[0] + 'j' + x[1] if len(x) == 1 else x + 'j',
            [text[i] + (text[i + 1]) for i in range(0, len(text) - 1, 2)],
        )
    )

    encrypted_pair_list = [encrypt_pair(i,matrix) for i in pair_list]
    return "".join(encrypted_pair_list)


key = "krishna"

matrix = create_matrix(key, alphabets)

print_matrix(matrix)

print(get_cipher("hello",matrix))
# print("ab : ",search_matrix("ab", matrix))
# print("ab : ",encrypt_pair("ab", matrix))
# print("mr : ",encrypt_pair("mr", matrix))
# print("mv : ",encrypt_pair("mv", matrix))
