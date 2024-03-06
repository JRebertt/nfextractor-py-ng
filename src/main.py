import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
# Importa a classe ReportGenerator
from report_generator import ReportGenerator

class PDFReportApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Gerador de Relatório PDF')
        self.geometry("500x300")  # Ajuste o tamanho conforme necessário
        self.configure(background='light gray')  # Define a cor de fundo da janela

        # Cria um frame para os botões
        self.frame_buttons = tk.Frame(self, bg='light gray')
        self.frame_buttons.pack(fill=tk.X, pady=20)

        # Botão para selecionar a pasta
        self.btn_select_directory = tk.Button(self.frame_buttons, text="Selecionar Pasta", command=self.select_directory, width=20, height=2, bg='light blue', fg='black')
        self.btn_select_directory.pack(side=tk.LEFT, padx=10)

        # Botão para gerar o relatório
        self.btn_generate_report = tk.Button(self.frame_buttons, text="Gerar Relatório", command=self.generate_report, width=20, height=2, bg='light green', fg='black')
        self.btn_generate_report.pack(side=tk.RIGHT, padx=10)

        # Cria um frame para a mensagem de status
        self.frame_status = tk.Frame(self, bg='light gray')
        self.frame_status.pack(fill=tk.BOTH, expand=True)

        # Label para exibir mensagens de status
        self.label_status = tk.Label(self.frame_status, text="Aguardando ação...", bg='light gray', fg='black', font=('Arial', 12))
        self.label_status.pack(pady=20)

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

        user_month = simpledialog.askstring("Mês do Relatório", "Por favor, digite o mês (MM) para o relatório:")
        if not user_month:
            messagebox.showerror("Erro", "Mês não informado.")
            return

        # Cria uma instância da classe ReportGenerator
        generator = ReportGenerator(self.selected_directory, user_month)

        try:
            # Chama o método generate_reports da instância
            generator.generate_reports()
            self.label_status.config(text=f"Relatório do mês {user_month} realizado com sucesso ✅")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {e}")

if __name__ == "__main__":
    app = PDFReportApp()
    app.mainloop()