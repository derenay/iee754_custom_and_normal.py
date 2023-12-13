import numpy as np
from decimal import Decimal, getcontext

class Iee754_Calculator:
    def __init__(self,
                 number:float,
                 force_exponent: int = None,
                 presicion: int = 0,
                 force_mantissa: int = None
    ) -> None:
        self.number = number
        self.presicion = presicion
        if not isinstance(number, float):
            raise TypeError("Number must be float")
        """ 
        exponent kısmı kaç bit olsun gözüküyor ama hesaplama kısmında bunun exponent değerini böyle alıroyrum bundan dolayı yanlışlık oluyor
        exponent hesaplamada exponent değerini düzgün al
        ve bu mantissa listi ne oluyor mantissa değerini nasıl hesaplıyoruz
        bunun aynısı exponent içinde geçerli
        bunu yaparsan kod biter her şey hazır 
        kurallar yaz sayıyı kurallardan geçir  
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! halledildi !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        """
        exponent_list: list[int] = [5, 8, 11, 15, 19]
        mantissa_list: list[int] = [10, 23, 52, 112, 236]
        
        self.__edge_case:str = None
        
        self.intNumber = int(abs(self.number))
        self.decimalNumber = abs(self.number) - self.intNumber
        self.intbinnary:str = None
        self.decimalbinnary:str = None
        self.binary_rep:str = None   #binary representation of number
        self.__exponent: int = (force_exponent if force_exponent is not None else exponent_list[self.presicion])
        self.__mantissa: int = (force_mantissa if force_mantissa is not None else mantissa_list[self.presicion])   #geliştirilecek
        self.mantisa_bits: str = ""
        self.exponent_number: int = 0
        self.exponent_bits: str = ""
        
    def run(self):
        self.intbinnary = self.int2Binary()
        self.decimalbinnary = self.decimal2Binary()
        print(f"{self.intbinnary}.{self.decimalbinnary}") 
        self.iee754Rep()
        
    def validate_number(self, number) -> Decimal:
        if Decimal(number).is_infinite():
            if Decimal(number) > 0:
                # +inf: 0 11111111 00000000000000000000000
                self.__edge_case = f"0 {'1' * self.__exponent} {'0' * self.__mantissa}"
                return Decimal("Infinity")
            # -inf: 1 11111111 00000000000000000000000
            self.__edge_case = f"1 {'1' * self.__exponent} {'0' * self.__mantissa}"
            return Decimal("-Infinity")
        if Decimal(number).is_nan() and Decimal(number).is_snan():
            # snan: 0 11111111 00000000000000000000001
            self.__edge_case = (
                f"0 {'1' * self.__exponent} {'0' * (self.__mantissa - 1)}1"
            )
            return Decimal("NaN")
        if Decimal(number).is_nan() and Decimal(number).is_qnan():
            # qnan: 0 11111111 10000000000000000000000
            self.__edge_case = (
                f"0 {'1' * self.__exponent} {'1' * (self.__mantissa - 1)}0"
            )
            return Decimal("NaN")
               
    
    def int2Binary(self) -> str:
        number = self.intNumber if self.exponent_number == 0 else self.exponent_number
        binary_rep = ""
        if number == 0: return "0"
        while number > 0:
            binary_rep = binary_rep + str(number % 2)
            number = number // 2
        return binary_rep[::-1]
        
    def decimal2Binary(self):
        number = self.decimalNumber
        binary_rep = ""
        while number > 0 and len(binary_rep) < self.__mantissa:
            number *= 2
            binary_rep += f"{int(number)}"
            number = number - int(number)
        return binary_rep.ljust(self.__mantissa, '0')
        
    def singBit(self) -> str:
        number = self.number
        return "0" if number == abs(number) else "1"
    
    def bias(self) -> int:
        return 2 ** (self.__exponent - 1) - 1
    
    def exponent(self)-> str:
        binary_repi = f"{self.intbinnary}.{self.decimalbinnary}"
        print(f"---------{self.intbinnary}")
        if self.intbinnary == "0":
            print("seanasfhaısukhfasfa")
            nonZeroIndex = binary_repi.find("1")
            shiftAmount = nonZeroIndex - 1
            self.binary_rep = binary_repi[1 + shiftAmount:]
            self.exponent_number = self.bias() - shiftAmount
            self.exponent_bits = self.int2Binary
            print(f"exponent number = {self.exponent_number} : int binnary len = {len(self.intbinnary)} : bias = {self.bias()}")
        else:
            self.exponent_number = len(self.intbinnary) - 1 + self.bias()
            print(f"exponent number = {self.exponent_number} : int binnary len = {len(self.intbinnary)} : bias = {self.bias()}")
            self.binary_rep = f"{self.intbinnary}{self.decimalbinnary}"
            self.exponent_bits = self.int2Binary
    
    def masntisa(self) -> str:
        self.mantisa_bits = self.binary_rep[1:self.__mantissa + 1].ljust(self.__mantissa, '0')
        
    def iee754Rep(self):
        self.exponent()
        self.masntisa()
        message = f"{self.singBit()} {self.exponent_bits().rjust(self.__exponent, '0')} {self.mantisa_bits}"
        
        print(f"exponent: {self.exponent_bits().rjust(self.__exponent, '0')}")
        print(f"mantisa: {self.mantisa_bits}")
        print(f"Ieee754: {message}")

if __name__ == "__main__":
    Iee754_Calculator(number = 12.4, force_exponent = 6, force_mantissa = 56).run()
    print(2**8)


