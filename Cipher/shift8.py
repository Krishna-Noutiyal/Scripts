# This program uses shift cyper techique to encrypt a message

a = "hello";

char_string = [ord(i)-8 for i in a];


print(char_string)


cipher_string = "".join([chr(i) for i in char_string]);

print(cipher_string)

org_string = "".join([chr(ord(i) +8) for i in cipher_string]);

print(org_string)
