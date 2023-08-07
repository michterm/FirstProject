import struct
import doctest 

class MD4:
    """
    Atribbutes
    -----------
    wiadomosc(może zostać podana w celu stworzenia nowego obiektu): bytes
        Tekst, lub zmienna "bytes" dla której zostanie policzona funkcja skrótu algorytmem MD4
    suma_kontrolna: str
        Suma kontrolna liczona na podstawie tekstu obliczana za pomocą metody get_hash

    
    Methods
    -----------
    get_hash(self):
        Metoda liczy wartość sumy kontrolnej dla obiektu z wiadomością zakodowaną w atrybucie C
    uzupelnienie2(tekst:str):
        Metoda koduje tekst i dzieli go na bajty
    @staticmethod F(x,y,z):
        Metoda zwraca 1 w bicie jeśli 2 pierwsze zmienne mają tam binarne 1 lub pierwsza zmienna ma w tym miejscu 0, a trzecia 1.  
    @staticmethod G(x,y,z):
        Metoda zwraca 1 w bicie jeśli przynajmniej 2 zmienne mają w tym bicie 1.
    @staticmethod H(x,y,z):
        Metoda zwraca 1 w bicie jeśli dokładnie 1 zmienna ma w tym bicie 1. 
    @staticmethod Bfunct(par,i,j,w,X,y,f):
        Metoda liczy funkcję potrzebna do wypełnienia listy par1 przez metodę "rundy"
    @staticmethod rundy(par,X):
        Metoda wypełnia listę "par1" przy użyciu metody "Bfunct"
    @classmethod from_string(cls, x):
        Konstruktor opcjonalny przyjmujący wiadomomość w typie "str"
    @classmethod textfromFile(cls,nazwa):
        Konstruktor opcjonalny odczytujący wiadomość w typie "str" z pliku o podanej nazwie (plik musi się znajdować w folderze projektu)
    """


    def uzupelnienie2(self)->bytes:
        """
        Metoda dzieli na bloki odpowiedniej długości zakodowaną wiadomość
        Returns:
            Tekst podzielony na bloki długości 64 bajtów    
        """   
        n=len(self.wiadomosc)
        self.wiadomosc+=b'\x80'
        self.wiadomosc+=b'\x00'*(64-(n+9)%64)
        self.wiadomosc+=struct.pack("<Q",8*n)
        return self.wiadomosc

    @staticmethod
    def F(x:int,y:int,z:int)->int:
        """ 
        Args:
            x(int)
            y(int)
            z(int)
        Returns:
            Metoda zwraca 1 w bicie jeśli 2 pierwsze zmienne mają tam binarne 1 lub pierwsza zmienna ma w tym miejscu 0, a trzecia 1.   
        """
        return (x & y) | ((~x) & z)

    @staticmethod
    def G(x:int,y:int,z:int):
        """
        Args:
            x(int)
            y(int)
            z(int)
        Returns:
            Metoda zwraca 1 w bicie jeśli przynajmniej 2 zmienne mają w tym bicie 1.   
        """
        return (x & y) | (x & z) | (y & z)

    @staticmethod
    def H(x:int,y:int,z:int):
        """
        Args:
            x(int)
            y(int)
            z(int)
        Returns:
            Metoda zwraca 1 w bicie jeśli dokładnie 1 zmienna ma w tym bicie 1.   
        """
        return x^y^z
    
    @staticmethod
    def Bfunct(par:list,i:int,j:int,w:int,X:list,y:int,f:int)->int:
        """
        Funkcja liczy wartość wyrażenia wart=(par[j]+ f(par[(j+1)%4],par[(j+2)%4], par[(j+3)%4]) + X[i] + y)& 0xffffffff), a następnie
        dokonuje operacji ((wart << w)&maska) | (wart >> (32 - w)). W ten sposób obliczamy funkcję B z algorytmu md4.
        Args:
            par(list)
            i(int)
            j(int)
            w(int)
            X(list)
            y(int)
            f(int)
                Funkcja F(x,y,z) lub G(x,y,z) lub K(x,y,x)
        """
        maska=0xffffffff
        wart=(par[j]+f(par[(j+1)%4],par[(j+2)%4],par[(j+3)%4])+X[i]+y)&maska
        return ((wart << w)&maska) | (wart >> (32 - w))

    @staticmethod
    def rundy(par:list,X:list)->list:
        """
        Funkcja wykonuje 3 rundy, wypełniając listę "par" za pomocą funkcji "Bfunct(par,i,j,w,X,y,f)", gdzie pierwsze 16 elementów f=F(x,y,z);
        kolejne 16 elementów f=G(x,y,z), a ostatnie 16 elementów f=H(x,y,z)
        Args:
            par(list)
            X(list)
        Returns:
            Lista "par1" uzupełniona o odpowiednie elementy.
        """
        par1=par.copy()
        y=0x00000000
        lista=[3,7,11,19]
        for i in range(16):
            par1[-i%4]=MD4.Bfunct(par1,i,-i%4,lista[i%4],X,y,MD4.F)
        y=0x5a827999
        lista=[3,5,9,13]
        for i in range(16):
            k=i//4+4*(i%4)
            par1[-i%4]=MD4.Bfunct(par1,k,-i%4,lista[i%4],X,y,MD4.G)
        y=0x6ed9eba1
        lista=[3,9,11,15]
        for i in range(16):
            pom=[0,8,4,12,2,10,6,14,1,9,5,13,3,11,7,15]
            par1[-i%4]=MD4.Bfunct(par1,pom[i],-i%4,lista[i%4],X,y,MD4.H)
        return par1
        

    #Konstruktor domyślny
    def __init__(self, x:bytes):
        if isinstance(x, bytes): 
            self.wiadomosc=x
        else:
            print(f'{x} nie jest ciągiem bajtów.')

    #Konstruktor opcjonalny from string
    @classmethod
    def from_string(cls, x:str)->bytes:
        if isinstance(x, str):
            wiadomosc = x.encode()
            return cls(wiadomosc)
        else:
            print(f'{x} nie jest ciągiem znaków.')
    #Konstruktor opcjonalny, odczytujący tekst z pliku
    @classmethod
    def textfromFile(cls,nazwa:str)->bytes:
        with open(nazwa) as f:
            x=f.read()
        wiadomosc = x.encode()
        return cls(wiadomosc)
    def get_hash(self):
        """
        Oblicza sumę kontrolną dla podanej wiadomości dla atrybutu C obiektu
        
        >>> Suma=MD4.from_string("Suma kontrolna")
        >>> Suma.get_hash()
        >>> Suma.suma_kontrolna
        '0x4c2058c2167a91f549a57100d965fbb9'
        >>> type(Suma.suma_kontrolna)
        <class 'str'>
        """
        maska=0xffffffff
        par=[0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]
        napis=self.uzupelnienie2()
        podzielony_napis=[napis[i:i+64] for i in range(0,len(napis),64)]
        for wycinek in podzielony_napis:
            X=list(struct.unpack("<16I", wycinek))
            par=[(i+j)&maska for i,j in zip(self.rundy(par,X), par)]
        do_wyjscia=[struct.pack("<L",i) for i in par]
        do_wyjscia_hex=[bajt.hex() for bajt in do_wyjscia]

        self.suma_kontrolna = '0x'+''.join(do_wyjscia_hex)
        #self.wiadomosc = tekst
        self.pod = None 
        self.priKey = None


doctest.testmod()
def main():
    a=MD4.textfromFile("plik.txt")
    a.get_hash()
    print(a.suma_kontrolna)
if __name__ == "__main__":
    main()