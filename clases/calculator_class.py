# Importación de la dependencia de abstracción
from abc import ABC, abstractmethod
# Importación de operaciones financieras para los diferentes cálculos
from clases.operation_class import FinancialOperation


class Calculator(ABC, FinancialOperation):
    """Clase base abstracta para las calculadoras financieras."""

    @staticmethod
    def round_two_decimals(numero: float) -> float:
        """Redondea un número a dos decimales."""
        return round(numero, 2)

    @abstractmethod
    def calculate(self) -> tuple:
        """Método abstracto que calculará dependiendo de la operación seleccionada."""
        pass


class LoanCalculator(Calculator):
    """Calculadora para préstamos."""

    def __init__(self, acquired: float, interest: float, fee_number: int) -> None:
        self.acquired = acquired
        self.interest = interest
        self.fee_number = fee_number

    def calculate(self) -> tuple:
        """Calcula la renta y genera la tabla de amortización."""
        self.rent = self.calculate_loan_rent(self.acquired, self.interest, self.fee_number)
        return self.round_two_decimals(self.rent), self.__get_loan_table()

    def __get_loan_table(self) -> list:
        """Genera la tabla de amortización."""
        # Columnas:
        # 0 - Periodo
        # 1 - Renta
        # 2 - Interés
        # 3 - Amortización
        # 4 - Saldo
        loan_table = []
        residue = self.acquired
        for period in range(self.fee_number + 1):
            if period == 0:
                loan_table.append((period, 0, 0, 0, residue))
                continue

            interest_item = residue * self.interest
            loan_item = self.rent - interest_item
            residue -= loan_item
            loan_table.append((
                period,
                self.round_two_decimals(self.rent),
                self.round_two_decimals(interest_item),
                self.round_two_decimals(loan_item),
                self.round_two_decimals(FinancialOperation.is_limit_zero(residue))
            ))

        return loan_table


class InvestmentCalculator(Calculator):
    """Calculadora para inversiones."""

    def __init__(self, capital: float, interest: float, fee_number: int, time: int) -> None:
        self.capital = capital
        self.interest = interest
        self.fee_number = fee_number
        self.time = time

    def calculate(self) -> tuple:
        """Calcula el interés compuesto y genera la tabla de inversión."""
        self.rent = self.calculate_investment(self.capital, self.interest, self.fee_number, self.time)
        return self.round_two_decimals(self.rent), self.__get_investment_table()

    def __get_investment_table(self) -> list:
        """Genera la tabla de intereses obtenidos."""
        # Columnas:
        # 0 - Periodo
        # 1 - Capital Actual
        # 2 - Interés del periodo
        # 3 - Capital más interés
        investment_table = []
        gained = self.capital
        for period in range(self.time + 1):
            if period == 0:
                investment_table.append((period, self.capital, 0, self.capital))
                continue

            interest_item = gained * (self.interest / self.fee_number)
            gained += interest_item
            investment_table.append((
                period,
                self.round_two_decimals(gained - interest_item),
                self.round_two_decimals(interest_item),
                self.round_two_decimals(gained)
            ))

        return investment_table
