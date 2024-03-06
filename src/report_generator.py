import os
import re
from file_manager import FileManager
from pdf_processor import PDFProcessor

class ReportGenerator:
    def __init__(self, root_directory, user_month, is_detailed=True):
        self.root_directory = root_directory
        self.user_month = user_month  # Mês especificado pelo usuário no formato MM
        self.is_detailed = is_detailed
        self.report_directory = os.path.join(root_directory, "Relatorios", self.user_month)
        FileManager.create_directory(self.report_directory)

        self.categories = ["NFe VENDAS", "NFS-e SERVIÇO"]
        self.subcategories = ["NOTAS CANCELADAS", "REMESSA PARA VENDA E VASILHAME", "RETORNO DE MERCADORIAS"]
        self.initialize_report_structure()

    def initialize_report_structure(self):
        FileManager.create_directory(os.path.join(self.report_directory, "Diversos"))
        for subcategory in self.subcategories:
            FileManager.create_directory(os.path.join(self.report_directory, "Diversos", subcategory))
        
        for category in self.categories:
            FileManager.create_directory(os.path.join(self.report_directory, category))
        
        FileManager.create_directory(os.path.join(self.report_directory, "NFS-e SERVIÇO", "NFS-e SERVIÇO Cancelados"))

    def generate_report_for_directory(self, directory, category=""):
        total_value = 0.0
        total_cancelled_value = 0.0  # Acumula o valor total para NFS-e SERVIÇO cancelados
        data_entries = []
        data_entries_cancelled = []

        pdf_files = FileManager.find_pdf_files(directory)
        for root, file_name in pdf_files:
            pdf_path = os.path.join(root, file_name)
            text = PDFProcessor.extract_text_from_pdf(pdf_path)

            title = os.path.splitext(file_name)[0]
            date_match = re.search(r'(\d{2})/(\d{2})/(\d{4})', text)
            if date_match:
                month_found = date_match.group(2)  # Extrai o mês da data
                if self.user_month != month_found:
                    continue  # Ignora arquivos que não correspondem ao mês especificado

            date = date_match.group(0) if date_match else 'Data não encontrada'

            if category == "NFS-e SERVIÇO" and re.search(r'\(CANCELADA\)|\(CANCELADO\)', title, re.IGNORECASE):
                value_match = re.search(r'R\$ ([\d\.,]+)', text)
                value_str = value_match.group(1).replace('.', '').replace(',', '.') if value_match else "0.0"
                value = float(value_str)
                total_cancelled_value += value
                data_entries_cancelled.append({"title": title, "date": date, "value_str": f"R$ {value_str}"})
            else:
                value_match = re.search(r'R\$ ([\d\.,]+)', text)
                value_str = value_match.group(1).replace('.', '').replace(',', '.') if value_match else "0.0"
                value = float(value_str)
                total_value += value
                data_entry = {"title": title, "date": date, "value_str": f"R$ {value_str}"}
                data_entries.append(data_entry)

        data_entries.sort(key=lambda x: x["title"])
        self.write_consolidated_report(category, data_entries, total_value, include_value=True)

        if data_entries_cancelled:
            data_entries_cancelled.sort(key=lambda x: x["title"])
            self.write_consolidated_report("NFS-e SERVIÇO Cancelados", data_entries_cancelled, total_cancelled_value, include_value=True)

    def write_consolidated_report(self, category, data_entries, total_value, include_value):
        if category == "NFS-e SERVIÇO Cancelados":
            category_report_directory = os.path.join(self.report_directory, "NFS-e SERVIÇO", "NFS-e SERVIÇO Cancelados")
            report_title = "NFS-e SERVIÇO Cancelados"
        elif category in self.subcategories:
            category_report_directory = os.path.join(self.report_directory, "Diversos", category)
            report_title = category
        else:
            category_report_directory = os.path.join(self.report_directory, category)
            report_title = category

        FileManager.create_directory(category_report_directory)
        
        report_file_path = os.path.join(category_report_directory, "relatorio.txt")
        with open(report_file_path, 'w', encoding='utf-8') as report_file:
            # Inclui o nome do relatório no início do arquivo
            report_file.write(f"Relatório: {report_title}\n\n")
            for entry in data_entries:
                line = f"{entry['title']}, {entry['date']}"
                if include_value:
                    line += f", {entry['value_str']}"
                report_file.write(line + '\n')
            if include_value:
                report_file.write('-' * 80 + '\n')
                report_file.write(f"Valor total: R$ {total_value:.2f}\n")

    def generate_reports(self):
        for category in self.categories:
            category_path = os.path.join(self.root_directory, category)
            self.generate_report_for_directory(category_path, category=category)

        for subcategory in self.subcategories:
            subcategory_path = os.path.join(self.root_directory, subcategory)
            self.generate_report_for_directory(subcategory_path, category="Diversos/" + subcategory)

        print("Relatórios gerados com sucesso.")
