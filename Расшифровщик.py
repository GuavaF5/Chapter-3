def xor_decrypt(encoded_message: str, key: str) -> str:
    decrypted_message = ""
    for i in range(len(encoded_message)):
        decrypted_message += chr(ord(encoded_message[i]) ^ ord(key[i % len(key)]))
    return decrypted_message

# Закодированное сообщение
encoded_message = "ѮѕCцјсSћєчХфSФљвЮжSћСрѐж_EѐцѐTфћјьЧъSўіфѝж]"

# Ключ
key = "secret"

# Расшифровка
decrypted_message = xor_decrypt(encoded_message, key)
print("Расшифрованное сообщение:", decrypted_message)