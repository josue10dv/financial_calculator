# Dependencia tkinter para creacion de GUI
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
# Libreria para las graficas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# Dependecia os para funciones del sistema operativo
import os
# Funciones de la calculadora financiera
from clases.calculator_class import LoanCalculator, InvestmentCalculator

class WindowFinancialCalc:
    """Ventana principal para la Calculadora Financiera."""

    def __init__(self, main: tk.Tk) -> None:
        """Constructor de la ventana principal."""
        self.main = main
        main.title("Calculadora Financiera")
        main.geometry("600x400")
        self.bg_color = '#accdb8'
        main.configure(bg=self.bg_color)

        icon_path = os.path.join("repositorio", "icon_fcalc.ico")
        self.icon = tk.PhotoImage(file=icon_path)
        main.iconphoto(True, self.icon)

        self.menu = tk.Menu(main)
        main.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Operaciones", menu=self.file_menu)
        self.file_menu.add_command(label="Cálculo de Amortización", command=self.show_loan_operation)
        self.file_menu.add_command(label="Interés ganado", command=self.show_investment_operation)

        self.label = tk.Label(
            main,
            text=("Bienvenido a la Calculadora Financiera.\n"
                  "En el menú de opciones encontrarás los diferentes\n"
                  "cálculos que podrás hacer con esta herramienta."),
            bg=self.bg_color
        )
        self.label.grid(row=0, column=0, columnspan=2, pady=20)

        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_columnconfigure(1, weight=1)

    def show_loan_operation(self) -> None:
        """Mostrar pantalla para el cálculo de amortización."""
        self.clear_window()

        tk.Label(
            self.main, text="Cálculo de Amortización", bg=self.bg_color
        ).grid(row=0, column=0, columnspan=2)

        tk.Label(
            self.main, text="Monto del Préstamo:", bg=self.bg_color
        ).grid(row=1, column=0, sticky="e")
        self.loan_amount = tk.Entry(self.main)
        self.loan_amount.grid(row=1, column=1, sticky="w")

        tk.Label(
            self.main,
            text="Tasa de Interés (por ejemplo, 0.05):",
            bg=self.bg_color
        ).grid(row=2, column=0, sticky="e")
        self.loan_interest = tk.Entry(self.main)
        self.loan_interest.grid(row=2, column=1, sticky="w")

        tk.Label(
            self.main, text="Número de Cuotas:", bg=self.bg_color
        ).grid(row=3, column=0, sticky="e")
        self.loan_fees = tk.Entry(self.main)
        self.loan_fees.grid(row=3, column=1, sticky="w")

        tk.Button(
            self.main, text="Calcular", command=self.calculate_loan
        ).grid(row=4, column=0, pady=(5, 20), padx=(0, 10), sticky="e")
        tk.Button(
            self.main, text="Volver", command=self.show_welcome_screen
        ).grid(row=4, column=1, pady=(5, 20), padx=(10, 0), sticky="w")

    def show_investment_operation(self) -> None:
        """Mostrar pantalla para el cálculo de interés compuesto."""
        self.clear_window()

        tk.Label(
            self.main, text="Cálculo de Interés Compuesto", bg=self.bg_color
        ).grid(row=0, column=0, columnspan=2)

        tk.Label(
            self.main, text="Capital Inicial:", bg=self.bg_color
        ).grid(row=1, column=0, sticky="e")
        self.investment_capital = tk.Entry(self.main)
        self.investment_capital.grid(row=1, column=1, sticky="w")

        tk.Label(
            self.main,
            text="Tasa de Interés (por ejemplo, 0.05):",
            bg=self.bg_color
        ).grid(row=2, column=0, sticky="e")
        self.investment_interest = tk.Entry(self.main)
        self.investment_interest.grid(row=2, column=1, sticky="w")

        tk.Label(
            self.main, text="Número de Periodos por Año:", bg=self.bg_color
        ).grid(row=3, column=0, sticky="e")
        self.investment_fees = tk.Entry(self.main)
        self.investment_fees.grid(row=3, column=1, sticky="w")

        tk.Label(
            self.main, text="Número de Años:", bg=self.bg_color
        ).grid(row=4, column=0, sticky="e")
        self.investment_time = tk.Entry(self.main)
        self.investment_time.grid(row=4, column=1, sticky="w")

        tk.Button(
            self.main, text="Calcular", command=self.calculate_investment
        ).grid(row=5, column=0, pady=(5, 20), padx=(0, 10), sticky="e")
        tk.Button(
            self.main, text="Volver", command=self.show_welcome_screen
        ).grid(row=5, column=1, pady=(5, 20), padx=(10, 0), sticky="w")

    def clear_window(self) -> None:
        """Limpiar la ventana principal."""
        for widget in self.main.winfo_children():
            widget.destroy()

    def show_welcome_screen(self) -> None:
        """Mostrar pantalla de bienvenida."""
        self.clear_window()
        self.__init__(self.main)

    def calculate_loan(self) -> None:
        """Calcular la amortización y mostrar los resultados."""
        try:
            acquired = float(self.loan_amount.get())
            interest = float(self.loan_interest.get())
            fee_number = int(self.loan_fees.get())

            loan_calculator = LoanCalculator(acquired, interest, fee_number)
            rent, loan_table = loan_calculator.calculate()

            self.show_results(
                f"Renta del préstamo: {rent}",
                loan_table,
                ["Periodo", "Renta", "Interés", "Amortización", "Saldo"]
            )
            self.show_graph(loan_table, "Tabla de Amortización", "loan")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa valores válidos.")

    def calculate_investment(self) -> None:
        """Calcular el interés compuesto y mostrar los resultados."""
        try:
            capital = float(self.investment_capital.get())
            interest = float(self.investment_interest.get())
            fee_number = int(self.investment_fees.get())
            time = int(self.investment_time.get())

            investment_calculator = InvestmentCalculator(
                capital, interest, fee_number, time
            )
            rent, investment_table = investment_calculator.calculate()

            self.show_results(
                f"Renta de la inversión: {rent}",
                investment_table,
                ["Periodo", "Capital Actual", "Interés del Periodo", "Capital + Interés"]
            )
            self.show_graph(investment_table, "Tabla de Interés Compuesto", 'invest')
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa valores válidos.")

    def show_results(self, result_text: str, table_data: list, headers: list) -> None:
        """Mostrar los resultados en una tabla."""
        self.clear_window()

        tk.Label(self.main, text=result_text, bg=self.bg_color).grid(row=0, column=0, columnspan=2)

        columns = [str(i) for i in range(len(headers))]
        tree = ttk.Treeview(self.main, columns=columns, show="headings", height=10)
        tree.grid(row=1, column=0, columnspan=2)

        for i, header in enumerate(headers):
            tree.heading(i, text=header)
            tree.column(i, width=100, anchor="center")

        for row in table_data:
            tree.insert("", "end", values=row)

        tk.Button(self.main, text="Volver", command=self.show_welcome_screen).grid(row=2, column=0, columnspan=2)

    def show_graph(self, table_data: list, title: str, graph_type: str) -> None:
        """Mostrar gráfico en una nueva ventana."""
        graph_window = tk.Toplevel(self.main)
        graph_window.title(title)
        
        values_index = 4 if graph_type == 'loan' else 1

        periods = [row[0] for row in table_data]
        values = [row[values_index] for row in table_data]

        fig, ax = plt.subplots()
        ax.plot(periods, values, marker='o')
        ax.set_title(title)
        ax.set_xlabel('Periodo')
        ax.set_ylabel('Valor')

        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack()


def start_calculator() -> None:
    """Iniciar la aplicación de la calculadora financiera."""
    main_window = tk.Tk()
    WindowFinancialCalc(main_window)
    main_window.mainloop()