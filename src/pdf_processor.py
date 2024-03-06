import pdfplumber
import re
from file_manager import FileManager

class PDFProcessor:
    date_pattern = r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}'
    value_pattern = r'VALOR TOTAL DA NOTA = R\$ ([\d\.,]+)'

    @staticmethod
    def extract_text_from_pdf(pdf_path):
        """
        Extrai todo o texto de um arquivo PDF.

        :param pdf_path: Caminho completo para o arquivo PDF.
        :return: O texto extraído do PDF.
        """
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text += (page.extract_text() or "") + "\n"
        except Exception as e:
            print(f"Erro ao abrir o arquivo PDF {pdf_path}: {e}")
        return text

    @staticmethod
    def find_data_in_text(text, user_month):
        """
        Procura por datas e valores monetários no texto extraído de um PDF.

        :param text: O texto extraído de um arquivo PDF.
        :param user_month: O mês especificado pelo usuário, usado para filtrar os dados.
        :return: Uma lista de dicionários com os dados encontrados ou uma lista vazia se nenhum dado for encontrado.
        """
        data_found = []
        date_matches = re.findall(PDFProcessor.date_pattern, text)
        value_matches = re.findall(PDFProcessor.value_pattern, text)

        for date, value in zip(date_matches, value_matches):
            if date.split('/')[1] == user_month:
                total_value_note = value.replace('.', '').replace(',', '.')
                data_found.append({'date': date, 'value': float(total_value_note)})

        return data_found

