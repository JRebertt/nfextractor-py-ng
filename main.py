import tkinter as tk
from tkinter import ttk, filedialog

def submit_action():
    info1 = entry1.get()
    info2 = entry2.get()
    output_label.config(text=f"Informações Recebidas:\nInfo 1: {info1}\nInfo 2: {info2}\nDiretório: {directory_path.get()}")

def select_directory():
    directory_selected = filedialog.askdirectory()
    directory_path.set(directory_selected)

root = tk.Tk()
root.title("PyNGBot")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

entry1 = ttk.Entry(mainframe)
entry1.grid(column=2, row=1, sticky=(tk.W, tk.E))
entry2 = ttk.Entry(mainframe)
entry2.grid(column=2, row=2, sticky=(tk.W, tk.E))

ttk.Label(mainframe, text="Info 1:").grid(column=1, row=1, sticky=tk.W)
ttk.Label(mainframe, text="Info 2:").grid(column=1, row=2, sticky=tk.W)

submit_button = ttk.Button(mainframe, text="Submeter", command=submit_action)
submit_button.grid(column=2, row=4, sticky=tk.W)

# Adicionando o botão para selecionar o diretório
directory_path = tk.StringVar()
select_directory_button = ttk.Button(mainframe, text="Selecionar Pasta", command=select_directory)
select_directory_button.grid(column=2, row=3, sticky=tk.W)

# Adicionando um label para mostrar o diretório selecionado
ttk.Label(mainframe, text="Diretório Selecionado:").grid(column=1, row=5, sticky=tk.W)
directory_label = ttk.Label(mainframe, textvariable=directory_path)
directory_label.grid(column=2, row=5, sticky=(tk.W, tk.E))

output_label = ttk.Label(mainframe, text="Informações recebidas serão mostradas aqui.")
output_label.grid(column=1, row=6, columnspan=2, sticky=tk.W)

# Rodando a aplicação
root.mainloop()