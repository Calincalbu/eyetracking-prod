if __name__ == "__main__":
    alphabet = 'A B C D'
    result = '  '
    result += alphabet
    result += '\n'

    for row in alphabet.split(' '):
        result += row + ' '
        for col in alphabet.split(' '):
            additive = '0'

            # Rules
            if (row == col):
                additive = '1'
            else:
                additive = '0'
            

            result += additive
            result += ' '
        result += '\n'
    
    print(result)