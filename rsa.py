#!/usr/bin/env python
import random
import pickle

def xgcd(a, b):
    """
    Rozszerzony algorytm Euklidesa.
    Zwraca krotkę (g, x, y), gdzie g jest największym wspólnym dzielnikiem liczb 
    a i b, a x i y są takimi liczbami, że g = ax + by.
    """
    if b==0:
        return (a, 1, 0)
    else:
        (gcd, c, d) = xgcd(b, a%b)
        return (gcd, d, c-a//b*d)

        
LINES = open('b000040.txt').read().splitlines()
def random_prime():
    """
    Funkcja zwraca losową liczbę pierwszą z pliku b000040.txt
    """
    global LINES
    myline =random.choice(LINES[100:200])
    myline = myline.split(" ")
    myline = myline[1] 
    myline = int(myline)  
    return myline


class Klucz_publiczny:

    def __init__(self, N, e, name=None):
        """
        Konstrutor klasy Klucz_publiczny.
        Tworzy klucz publiczny (N, e) o nazwie name,
        która jest potem przekazywana w Aplikacji. 
        """
        self.N = N
        self.e = e
        self.key = name or f"<{N}, {e}>"

    def encrypt(self, m):
        """
        Szyfrowanie RSA.
        Szyfruje liczbę m przy użyciu klucza publicznego (e, N).
        """
        E = (m**self.e) % self.N
        
        return E

class Klucz_prywatny:
    
    def __init__(self, d, p, q, name=None):
        """
        Konstrutor klasy Klucz_prywatny.
        Tworzy klucz prywatny (d, p, q) o nazwie name,
        która jest potem przekazywana w Aplikacji.
        """
        self.d = d
        self.q = q
        self.p = p
        self.key = name or f"<{d}, {p}, {q}>"

    def decrypt(self, E):
        """
        Deszyfrowanie RSA.
        Deszyfruje liczbę E przy użyciu klucza prywatnego (d, p, q).
        """
        D = (E**self.d)  %  (self.p*self.q)
        
        return D
    
 
class RSA():

    def __init__(self):
        """
        Konstruktor klasy RSA. 
        Tworzy obiekt keys, który jest 
        później przekazywany w Aplikacji.
        """
        self.keys = None 
    
    @classmethod
    def generate_keys(cls):
        """
        Generuje klucze publiczny i prywatny.
        """
        p = random_prime()
        q = random_prime()
        N = p*q
        phi = (p - 1)*(q - 1)
        e = phi
        while xgcd(e, phi)[0] != 1:
            e = random_prime()
        d = xgcd(e, phi)[1]
        while d<0:
            d+=phi
        klucz_publiczny = Klucz_publiczny(N, e)
        klucz_prywatny = Klucz_prywatny(d, p, q)
        
        return klucz_publiczny, klucz_prywatny
    
    @staticmethod
    def save_keys(klucz_publiczny, klucz_prywatny,nazwa):
        """
        Zapisuje klucze RSA do pliku.
        """
        file1 = pickle.dump(klucz_publiczny, open(nazwa+"_pub.txt", "wb"))
        file2 = pickle.dump(klucz_prywatny, open(nazwa+"_pri.txt", "wb"))
        
        return file1, file2
        
    @staticmethod
    def load_keys():
        """
        Wczytuje klucze RSA z pliku.
        """
        klucz_publiczny = pickle.load(open("Klucz publiczny.txt", "rb"))
        klucz_prywatny = pickle.load(open("Klucz prywatny.txt", "rb"))
        
        return klucz_publiczny, klucz_prywatny