import re
from spellchecker import SpellChecker

spell = SpellChecker(language='en')

text = input("Enter a text: ").lower()

raw_tokens = text.split()

best_shift = 0
max_valid_words = -1
best_decoded_words = []


for chiff in range(26):
    current_attempt = []
    valid_words_count = 0

    for token in raw_tokens:
        new_word = ""
        for letter in token:
            if 'a' <= letter <= 'z':

                new_word += chr((ord(letter) - ord('a') + chiff) % 26 + ord('a'))
            else:
                new_word += letter
        
        current_attempt.append(new_word)

        clean_word = re.sub(r'[^a-z]', '', new_word)
        if clean_word and clean_word in spell:
            valid_words_count += 1


    if valid_words_count > max_valid_words:
        max_valid_words = valid_words_count
        best_shift = chiff
        best_decoded_words = current_attempt

print("Decoded text:", " ".join(best_decoded_words))