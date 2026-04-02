# ===== Step 1: Take article input from user and save to file =====
file = open("article.txt", "w")

print("Enter your article (type 'END' on a new line to finish):")

while True:
    line = input()
    if line == "END":
        break
    file.write(line + "\n")

file.close()


# ===== Step 2: Read the file and count lines, words, characters =====
file = open("article.txt", "r")

lines = 0
words = 0
characters = 0

for line in file:
    lines += 1
    words += len(line.split())
    characters += len(line)

file.close()


# ===== Step 3: Display results =====
print("\nArticle Analysis:")
print("Number of lines:", lines)
print("Number of words:", words)
print("Number of characters:", characters)