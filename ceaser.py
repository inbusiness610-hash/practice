from spellchecker import SpellChecker

spell = SpellChecker(language='en')
l = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def is_word(word):
    return word in spell

text = input("Enter a text: ").lower()
words = text.split()

chiff = -25
rechifered = []

while chiff < 26:
    current_attempt = []
    all_words_valid = True

    for w in words:
        new_word = ""
        for letter in w:
            if letter in l:
                new_word += l[(l.index(letter) + chiff) % 26]
            else:
                new_word += letter
        if is_word(new_word):
            current_attempt.append(new_word)
        else:
            all_words_valid = False
            break 


    if all_words_valid:
        rechifered = current_attempt
        break 
    chiff += 1

print("Decoded text:", " ".join(rechifered))