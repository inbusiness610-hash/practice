def hack_caesar_cipher():
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

    print("Decoded text:", " ".join(best_decoded_words), " key: ", best_shift)
    return best_shift, best_decoded_words

def ceasar_encoder():
    text = input("Enter a text: ").lower()
    shift = int(input("Enter a shift value (0-25): "))

    encoded_text = ""
    for letter in text:
        if 'a' <= letter <= 'z':
            encoded_text += chr((ord(letter) - ord('a') + shift) % 26 + ord('a'))
        else:
            encoded_text += letter

    print("Encoded text:", encoded_text)
    return encoded_text

def ceasar_decoder():
    text = input("Enter a text: ").lower()
    shift = int(input("Enter a shift value (0-25): "))

    decoded_text = ""
    for letter in text:
        if 'a' <= letter <= 'z':
            decoded_text += chr((ord(letter) - ord('a') - shift) % 26 + ord('a'))
        else:
            decoded_text += letter

    print("Decoded text:", decoded_text)
    return decoded_text

def main():
    while True:
        print("\nCaesar Cipher Tool")
        print("1. Encode")
        print("2. Decode")
        print("3. Hack (Brute Force)")
        print("4. Exit")

        choice = input("Choose an option (1-4): ")

        if choice == '1':
            ceasar_encoder()
        elif choice == '2':
            ceasar_decoder()
        elif choice == '3':
            hack_caesar_cipher()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()