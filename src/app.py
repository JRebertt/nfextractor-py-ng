import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
# Importa a função main ajustada
from service import generate_reports as process_main

class PDFReportApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Gerador de Relatório PDF')
        self.geometry("400x200")

        self.btn_select_directory = tk.Button(self, text="Selecionar Pasta", command=self.select_directory)
        self.btn_select_directory.pack(pady=20)

        self.btn_generate_report = tk.Button(self, text="Gerar Relatório", command=self.generate_report)
        self.btn_generate_report.pack(pady=10)

        self.selected_directory = None

    def select_directory(self):
        self.selected_directory = filedialog.askdirectory()
        if self.selected_directory:
            messagebox.showinfo("Pasta Selecionada", f"Pasta selecionada: {self.selected_directory}")
        else:
            messagebox.showerror("Erro", "Nenhuma pasta selecionada!")

    def generate_report(self):
        if not self.selected_directory:
            messagebox.showerror("Erro", "Por favor, selecione uma pasta primeiro.")
            return

        user_month = simpledialog.askstring("Mês do Relatório", "Por favor, digite o mês (MM) para a conversão:")
        if not user_month:
            messagebox.showerror("Erro", "Mês não informado.")
            return

        try:
            # Chama a função main do script de processamento com os parâmetros necessários
            process_main(self.selected_directory, user_month)
            messagebox.showinfo("Concluído", "Relatório concluído com sucesso ✅")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {e}")

if __name__ == "__main__":
    app = PDFReportApp()
    app.mainloop()
