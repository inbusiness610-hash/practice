
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


from collections import Counter

ENGLISH_FREQS = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702,
    'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153,
    'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
    'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
    'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974,
    'Z': 0.00074
}

def calculate_ioc(text: str) -> float:
    """Calculates the Index of Coincidence for a given text string."""
    N = len(text)
    if N <= 1:
        return 0.0
    counts = Counter(text)
    return sum(n * (n - 1) for n in counts.values()) / (N * (N - 1))

def find_key_length(ciphertext: str, max_length: int = 20) -> int:
    """Finds the most likely key length by testing average IoC across slices."""
    best_length = 1
    best_ioc_diff = float('inf')

    TARGET_IOC = 0.067 

    for k in range(1, max_length + 1):
        # Create k streams
        slices = [ciphertext[i::k] for i in range(k)]
        avg_ioc = sum(calculate_ioc(s) for s in slices) / k
        
        diff = abs(avg_ioc - TARGET_IOC)
        if diff < best_ioc_diff:
            best_ioc_diff = diff
            best_length = k
            
    return best_length

def solve_caesar_shift(stream: str) -> str:
    """Finds the single key character for a stream using Chi-Square testing."""
    N = len(stream)
    best_shift = 0
    min_chi2 = float('inf')
    
    for shift in range(26):
        decrypted_stream = [chr((ord(char) - 65 - shift) % 26 + 65) for char in stream]
        counts = Counter(decrypted_stream)

        chi2 = 0.0
        for letter, freq in ENGLISH_FREQS.items():
            expected = N * freq
            observed = counts.get(letter, 0)
            chi2 += ((observed - expected) ** 2) / expected
            
        if chi2 < min_chi2:
            min_chi2 = chi2
            best_shift = shift
            
    return chr(best_shift + 65)

def break_vigenere(max_key_len: int = 20) -> tuple[str, str]:
    ciphertext = input("input your text: ").strip()
    

    if not ciphertext:
        print("Error: Input text cannot be empty!")
        return "", ""

    clean_ct = ''.join(c.upper() for c in ciphertext if c.isalpha())

    if len(clean_ct) < 20:
        print("Warning: Ciphertext is too short for reliable frequency analysis. Provide a longer text (ideally 100+ chars).")


    effective_max_len = min(max_key_len, max(1, len(clean_ct) // 2))


    key_len = find_key_length(clean_ct, max_length=effective_max_len)
    

    key_chars = []
    for i in range(key_len):
        stream = clean_ct[i::key_len]
        key_chars.append(solve_caesar_shift(stream))
        
    recovered_key = ''.join(key_chars)
    

    plaintext = []
    key_idx = 0
    for char in ciphertext:
        if char.isalpha():
            is_upper = char.isupper()
            c_val = ord(char.upper()) - 65
            k_val = ord(recovered_key[key_idx % key_len]) - 65
            
            p_val = (c_val - k_val) % 26
            p_char = chr(p_val + 65) if is_upper else chr(p_val + 97)
            
            plaintext.append(p_char)
            key_idx += 1
        else:
            plaintext.append(char)

    print(f"Recovered Key: {recovered_key}")
    print(f"Decrypted Plaintext: {''.join(plaintext)}")
            
    return recovered_key, ''.join(plaintext)

if __name__ == "__main__":
    while 1:
        print("\n\n")
        print("Welcome to the Vigenère Cipher Program!")
        print("1. Encode")
        print("2. Decode")
        print("3. Break Cipher")
        print("4. Exit")
        type = input("Enter your choice(1/2/3/4): ")
        if type=='1':
            vigenere_encode()
        elif type=='2':
            vigenere_decode()
        elif type=='3':
            break_vigenere()
        elif type=='4':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
