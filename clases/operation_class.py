# Libreria para las operaciones matematicas
import math

# Clase encargada de realizar todas las operaciones basicas
class Operation:
    """Clase encargada de realizar todas las operaciones básicas."""

    @staticmethod
    def get_power(base: float, exponent: float) -> float:
        """Calcula la potencia de un número base elevado a un exponente."""
        return math.pow(base, exponent)
    
    @staticmethod
    def is_limit_zero(number: float, epsilon: float = 1e-9) -> float:
        """Verifica si un número es cercano a cero y lo reemplaza por 0."""
        return 0 if abs(number) < epsilon else number

class FinancialOperation(Operation):
    """Clase que usa las operaciones básicas para realizar cálculos financieros."""

    def calculate_loan_rent(self, acquired: float, interest: float, fee_number: float) -> float:
        """Calcula la renta para una amortización."""
        return (acquired * interest) / (1 - Operation.get_power((1 + interest), -fee_number))

    def calculate_investment(self, capital: float, interest: float, fee_number: int, time: float) -> float:
        """Calcula el interés sobre una inversión inicial."""
        return capital * Operation.get_power(1 + (interest / fee_number), fee_number * time)