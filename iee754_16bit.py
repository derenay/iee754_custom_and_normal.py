import math


class Halfprecison:
    def __init__(self, number) -> None:
        self.number = number
        if not isinstance(number, float):
            raise TypeError("Wrong type:: Must be Float")

    def __str__(self) -> str:
        try:
            if self.number == 0:
                return "0" * 10
            if math.isnan(self.number):
                return '0' + '1' * 15
            elif math.isinf(self.number):
                return '0' + '1' * 5 + '0' * 10 if self.number > 0 else '1' + '1' * 5 + '0' * 10
            else:
                self.results()
        except(ValueError, TypeError):
            raise TypeError("Invalid input type or value, expected a valid number")

    def results(self):
        pass


class ieee_calculator:
    def __init__(self, number) -> None:
        self.number = number
        self.IntPart = int(abs(self.number))
        self.decimalIntPart = abs(self.number) - self.IntPart
        self.exp_number = 0
        self.binary_rep = ""
        self.exp_bits = ""
        self.int_part = ""
        self.decimal_part = ""

        print("Function working...")

    def float_to_bits(self) -> None:
        self.int_part = self.int_converter()
        self.decimal_part = self.decimal_conventer()
        self.binary_rep = self.int_part + self.decimal_part
        # exponent_calcator çağırılacak

        self.exponent_calcator()
        self.ieee_conventer()

    def exponent_calcator(self):
        binary_repi = f"{self.int_part}.{self.decimal_part}"
        if self.int_part == "0":
            nonZeroIndex = binary_repi.find("1")
            shiftAmount = nonZeroIndex - 1
            self.binary_rep = binary_repi[1 + shiftAmount:]
            self.exp_number = 15 - shiftAmount
            self.exp_bits = self.int_converter
            print(f"-------++++--{self.binary_rep}")
        else:
            self.exp_number = len(self.int_part) - 1 + 15
            self.exp_bits = self.int_converter

    def int_converter(self) -> str:
        number = self.IntPart if self.exp_number == 0 else self.exp_number
        binary_rep = ""
        if number == 0: return "0"
        while number > 0:
            if number % 2 == 1:
                binary_rep += "1"
            else:
                binary_rep += "0"
            number = number // 2
        print("Int convernter working...")
        return binary_rep[::-1]

    def decimal_conventer(self) -> str:
        number = self.decimalIntPart
        binary_rep = ""
        while number > 0 and len(binary_rep) < 10:
            number *= 2
            binary_rep += f"{int(number)}"
            number = number - int(number)
            
        return binary_rep.ljust(10, '0')  # add 0 if needed

    def ieee_conventer(self) -> str:
        singbit = "0" if self.number == abs(self.number) else "1"
        exponent  = self.exp_bits().rjust(5, '0')
        mantissa = self.binary_rep[1:11].ljust(10, '0')
        # burası daha iyi hale getirilcek
        print(f"binary rep is: {self.int_part}.{self.decimal_part}")
        print(f"scientific notaion: {self.int_part[0]}.{self.int_part[1:]}{self.decimal_part} x 2*{self.exp_number}")

        return print(f"iee rep: {singbit}{exponent}{mantissa}")


if __name__ == "__main__":
    ieee_calculator(12.4).float_to_bits()
    pass
    #0 10010 1000110010