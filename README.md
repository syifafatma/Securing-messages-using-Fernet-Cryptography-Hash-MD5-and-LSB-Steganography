Steganography is an art of hiding messages into cover object (in this case we used image) without drawing attacker’s attention. Before the messages embedded to image, messages are encypted with Fernet Cipher method and the fernet key hashed using MD5 encoder. Combination of cryptography (Fernet Cipher method), Hash MD5 function, and steganography (LSB method) increasing security level of messages.
## Initial Display
There are two main menu in this this program:
### 1. Embedding Menu
![Screenshot (1317)](https://github.com/syifafatma/Securing-messages-using-Fernet-Cryptography-Hash-MD5-and-LSB-Steganography/assets/88698082/6092cc50-ad0b-46da-9580-c27446e51649)
### 2. 'Ekstraksi' Menu
![Screenshot (1318)](https://github.com/syifafatma/Securing-messages-using-Fernet-Cryptography-Hash-MD5-and-LSB-Steganography/assets/88698082/180e243a-e270-4b2a-874f-9d31822be920)
## Embedding Process
In this Embedding menu, messages are embedded to an image. Input that are required in this process are 'Teks' (text) and 'Kunci' (fernet key).
![Screenshot (1320)](https://github.com/syifafatma/Securing-messages-using-Fernet-Cryptography-Hash-MD5-and-LSB-Steganography/assets/88698082/a881fa10-4bd6-4442-a755-67f0d40b81ae)
## Extraction Process
In 'Ekstraksi' menu, stego-image (image that have been embedded with messages) is exctracted to get the messages. Extraction process requires fernet key so that only authorized user can do it.
![Screenshot (1323)](https://github.com/syifafatma/Securing-messages-using-Fernet-Cryptography-Hash-MD5-and-LSB-Steganography/assets/88698082/c167be93-7228-4a92-92a4-ab5b95d299f7)



