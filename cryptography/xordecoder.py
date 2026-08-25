#k= bytes.fromhex("0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104")
k=bytes.fromhex(input("Enter the hex string: ").strip())
p=input("Enter the plaintext: ")
#p="crypto{"
l=len(p)
key=""
K=""
i=0
for b in k:
    if i==len(p):
        break
    K+=chr(b)


for a, b in zip(K, p):
    key+=chr(ord(a) ^ ord(b))

print(f"first: {l} letters of key: " + key)
KEY=input("so what will be the key?: ").encode()

decrypted_list = []
for i in range(len(k)):
    key_byte=KEY[i%len(KEY)]
    decrypted_list.append(k[i] ^ key_byte)

print("DECRYPTED: " + "".join(chr(b) for b in decrypted_list))