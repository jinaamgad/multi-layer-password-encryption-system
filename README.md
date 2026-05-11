# Multi-Layer Password Encryption System

## Overview
This project is a Python-based password authentication system that applies multiple layers of encryption to enhance security. It combines hashing and encryption techniques to securely process and store user credentials.

---

## Features
- Multi-layer encryption pipeline (SHA → DES → AES → RSA)
- Secure password storage in encrypted format
- User authentication through re-encryption and comparison
- File-based storage system

---

## How It Works
1. User enters username and password  
2. Password is hashed using SHA  
3. The hash is encrypted using DES  
4. The result is encrypted again using AES  
5. Final encryption is done using RSA  
6. Encrypted data is stored in a file  
7. During login, the same process is repeated for verification  

---

## Technologies Used
- Python  
- SHA Hashing  
- DES Encryption  
- AES Encryption  
- RSA Encryption  
- File Handling  

---

## Security Concept
This project demonstrates how combining multiple encryption techniques can significantly increase data protection and reduce the risk of unauthorized access.

---


## Future Improvements
- Implement database storage instead of text files  
- Add a graphical user interface (GUI)  
- Improve key management system  
- Enhance performance and scalability  

---

## Note
This project is for educational purposes and demonstrates core concepts of secure authentication and encryption.
