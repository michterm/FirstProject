from faza_wstepna import *
from rsa import RSA, Klucz_prywatny, Klucz_publiczny
import math

def divide_message(pubkey:Klucz_publiczny,controlsum:int)->list:
        """
        Dzieli sumę kontrolna na bloki o długości S= log256(N) bajtów, gdzie N jest współczynnikiem klucza publicznego.
        """
        S=int(math.log(pubkey.N,256))
        divided_message=["0x"+controlsum[i:i+S] for i in range(2,len(controlsum)-S,S)]
        return divided_message

def Signature_from_string(prikey:Klucz_prywatny,pubkey:Klucz_publiczny,message:str)->tuple:
        """
        Podpisuje wiadomość podaną jako str i zwraca ją oraz podpis jako listę
        """
        afterMD4=MD4.from_string(message)
        afterMD4.get_hash()
        sumkon=[int(frag,0) for frag in divide_message(pubkey,afterMD4.suma_kontrolna)]
        signed=[(x**prikey.d)%(prikey.p*prikey.q) for x in sumkon]
        return message,signed
    
def Signature_from_file(prikey:Klucz_prywatny,pubkey:Klucz_publiczny,file:str)->tuple:
        """
        Podpisuje wiadomość podaną z podanego pliku i zwraca ją oraz podpis jako listę
        """
        afterMD4=MD4.textfromFile(file)
        with open(file) as f:
            message=f.read()
        afterMD4.get_hash()
        sumkon=[int(frag,0) for frag in divide_message(pubkey,afterMD4.suma_kontrolna)]
        signed=[(x**prikey.d)%(prikey.p*prikey.q) for x in sumkon]
        return message,signed

def Check_signature(pubkey:Klucz_publiczny,message:str,sign:list)->bool:
        """
        Sprawdza podany podpis za pomocą klucza publicznego. Zwraca True, 
        jeśli wiadomość została podpisana kluczem prywatnym odpowiadającym danemu kluczowi publicznemu
        i False w przeciwnym wypadku
        """
        afterMD4=MD4.from_string(message)
        afterMD4.get_hash()
        sumkon=[int(frag,0) for frag in divide_message(pubkey,afterMD4.suma_kontrolna)]
        checksum=[(x**pubkey.e)%pubkey.N for x in sign]
        if checksum==sumkon:
            return True
        else:
            return False

def main():
    a=RSA.generate_keys()
    b=RSA.generate_keys()
    print(Signature_from_string(a[1],a[0],"Ala ma kota"))
    mes=Signature_from_string(a[1],a[0],"Ala ma kota")[0]
    sign=Signature_from_string(a[1],a[0],"Ala ma kota")[1]
    print(Check_signature(b[0],mes,sign)) #False
    print(Check_signature(a[0],mes,sign)) #True
if __name__=="__main__":
    main()
