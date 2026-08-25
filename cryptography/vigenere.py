
letters=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def vigenere_encode():
    ciphertext = input("input your text here: ").lower()
    key = input("input your key here: ").lower()
    encoded_text = ""
    key_length = len(key)
    key_index = 0

    for char in ciphertext:
        if char.lower() in letters:
            char_index = letters.index(char.lower())
            key_char = key[key_index % key_length].lower()
            key_index_value = letters.index(key_char)
            encoded_index = (char_index + key_index_value)%26
            encoded_char = letters[encoded_index]
            encoded_text += encoded_char
            key_index += 1
        else:
            encoded_text += char
    print(f"Encoded text: {encoded_text}")  
    return encoded_text

def vigenere_decode():
    encoded_text = input("input your text here: ").lower()
    key = input("input your key here: ").lower()
    decoded_text = ""
    key_length = len(key)
    key_index = 0

    for char in encoded_text:
        if char.lower() in letters:
            char_index = letters.index(char.lower())
            key_char = key[key_index % key_length].lower()
            key_index_value = letters.index(key_char)
            decoded_index = (char_index - key_index_value) % 26
            decoded_char = letters[decoded_index]
            decoded_text += decoded_char
            key_index += 1
        else:
            decoded_text += char
    print(f"Decoded text: {decoded_text}")  
    return decoded_text




if __name__ == "__main__":
    while 1:
        print("\n\n")
        print("Welcome to the Vigenère Cipher Program!")
        print("1. Encode")
        print("2. Decode")
        print("3. Exit")
        type = input("Enter your choice(1/2/3): ")
        if type=='1':
            vigenere_encode()
        elif type=='2':
            vigenere_decode()
        elif type=='3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")