from Crypto.Cipher import AES #used to encrpyt and decrpyt the password

def encrpyt(message):
    """Uses AES to encrpyt message. Message must be a size of 16. Returns the ciphertext"""
    encryption_suite = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')

    padded_message = pad_message(message)

    cipher_text = encryption_suite.encrypt(padded_message)
    # print(cipher_text)

    return cipher_text

def decrpyt(cipher_text):

    decryption_suite = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
    plain_text = decryption_suite.decrypt(cipher_text)
    print(plain_text)

    return plain_text

def decrpyt_password(cipher_text):
    """Trims the decrpyted text starting at the end and moving right, up to and including the first. Returns the original password"""

    plain_text_byte_string = decrpyt(cipher_text)

    plain_text = str(plain_text_byte_string, 'utf-8') #without the str conversion, plain_text is a byte object
    #find position of last character in plaintext password
    first_pad_index = plain_text.rfind('.')

    # print('Decrypted password is: ' + plain_text[0:first_pad_index])
    return plain_text[0:first_pad_index]

def pad_message(message):
    """Pads the message to be a multiple of 16 character"""

    # the length of the message cannot be a length of 16 because if it is, then no padding needed!'
    if len(message) % 16 == 0:
        return message

    # find smallest multiple of 16 larger than len(message)

    number_of_pads_needed = 16 - int(len(message) % 16)

    padded_message = message + get_pads(number_of_pads_needed)

    # print('The new message is: ' + padded_message + ' and its length is: ' + str(len(padded_message)))

    return padded_message


def get_pads(pad_count):
    """Returns the paddings. The first padded character is a . and the rest are X"""
    assert pad_count > 0, 'pad_count must be larger than 0, otherwise, nothing to pad'

    pad = '.'
    pad_count -= 1
    pad += 'X' * int(pad_count)

    # print('pad is: ' + pad)

    return pad


# c = encrpyt('mypassword 345 34  sd sdf ')
# print(c)

# p = decrpyt_password(c)
# print(p)
