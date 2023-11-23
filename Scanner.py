import subprocess

code = """
x := 12;
y := 20 / 2;
if x < 100 then
    repeat$
        x := x + 1;
        read x;
        write x;
    until x = 200 * 5;
end#
"""

tokens_types = {";": "SEMICOLON", "if": "IF", "then": "THEN", "end": "END", "repeat": "REPEAT",
                "until": "UNTIL", ":=": "ASSIGN", "read": "READ", "write": "WRITE", "<": "LESSTHAN", "=": "EQUAL",
                "+": "PLUS", "-": "MINUS", "*": "MULT", "/": "DIV", "(": "OPENBRACKET", ")": "CLOSEDBRACKET"}

reserved_words = ["if", "then", "end", "repeat", "until", "read", "write"]

single_special_chars = [";", "<", "+", "-", "*", "/", "(", ")"]

tokens_collected = []

skipper = 0

# scanning
for i in range(len(code)):

    if skipper > 1:
        skipper -= 1
        continue

    # counter for skipping several loops
    skipper = 0

    # assign operator
    if code[i] == ":":
        if code[i+1] == "=":
            tokens_collected.append([code[i]+code[i+1], "ASSIGN"])
        else:
            tokens_collected.append([code[i], "INVALID_TOKEN"])

    # equal
    elif code[i] == "=":
        if code[i-1] == ":":
            continue
        else:
            tokens_collected.append([code[i], "EQUAL"])

    # the rest of the special chars
    elif code[i] in single_special_chars:
        tokens_collected.append([code[i], tokens_types[code[i]]])

    # numbers
    elif code[i].isnumeric():
        num = ""
        num_counter = 0
        while code[i+num_counter].isnumeric():
            num += code[i+num_counter]
            num_counter += 1
            skipper += 1
        tokens_collected.append([num, "NUMBER"])

    # letters => identifiers and reserved words
    elif code[i].isalpha():
        word = ""
        word_counter = 0
        while code[i+word_counter].isalpha():
            word += code[i+word_counter]
            word_counter += 1
            skipper += 1

        # check wether identifier or reserved word
        if word not in reserved_words:
            tokens_collected.append([word, "IDENTIFIER"])
        else:
            tokens_collected.append([word, tokens_types[word]])
            
    elif  not (code[i].isalpha() or code[i].isdigit()) and (code[i] not in single_special_chars) and code[i] != " " and code[i] != "\n":
        tokens_collected.append([code[i], "INVALID_TOKEN"])
        

scanned_code = ""

for i in tokens_collected:
    temp = " , ".join(i)
    scanned_code += temp + "\n"
    

# check
print(str(tokens_collected))
print(scanned_code)

# Specify the file path
file_path = "scanned_code.txt"

# Open the file in write mode ("w"), which will create the file if it doesn't exist
with open(file_path, "w") as file:
    file.write(scanned_code)

# The file is now created, and the content is written to it.

# Open the file with the default text editor or associated program on Windows
subprocess.run(["notepad", file_path], shell=True, check=True)


