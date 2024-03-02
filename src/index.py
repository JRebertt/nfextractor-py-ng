import os
import pdfplumber
import re

def solicit_month():
    return input("Por favor, digite o mês (MM) para a conversão: ")

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def process_files_for_month(directory, output_file, user_month, is_detailed=True):
    total_sum = 0.0
    date_pattern = r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}'
    value_pattern = r'VALOR TOTAL DA NOTA = R\$ ([\d\.,]+)'

    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.pdf'):
                try:
                    with pdfplumber.open(os.path.join(root, file_name)) as pdf:
                        text = "\n".join(page.extract_text() or '' for page in pdf.pages)
                        if is_detailed:
                            date_matches = re.findall(date_pattern, text)
                            value_matches = re.findall(value_pattern, text)
                            if date_matches and date_matches[0].split('/')[1] == user_month:
                                if value_matches:
                                    total_value_note = value_matches[0].replace('.', '').replace(',', '.')
                                    total_sum += float(total_value_note)
                                    output_file.write(f"Nome do arquivo: {os.path.splitext(file_name)[0]}\n")
                                    output_file.write(f"Data e Hora de Emissão: {date_matches[0]}\n")
                                    output_file.write(f"Valor total da nota = R$ {total_value_note}\n")
                                    output_file.write('-'*80 + '\n\n')
                        else:
                            output_file.write(f"Nome do arquivo: {os.path.splitext(file_name)[0]}\n{text}\n" + '-'*80 + '\n\n')
                except Exception as e:
                    print(f"Erro ao processar arquivo {file_name}: {e}")
    if is_detailed:
        output_file.write(f"Total somado de todas as notas = R$ {total_sum:.2f}\n")
        

def main():
    root_directory = '/Users/joaorodrigues/Documents/www/botpy/src/NFe_Vendas'
    while True:
        user_month = solicit_month()
        report_directory = os.path.join(root_directory, "Relatorio")
        categories = ["Serviços", "Vendas", "Diversos"]
        subcategories = ["Canceladas", "Remessas", "Retorno"]
        
        for category in categories:
            cat_directory = os.path.join(report_directory, f"Relatorio de {category}")
            create_directory(cat_directory)
            if category != "Diversos":
                output_path = os.path.join(cat_directory, f"relatorio_mes_{user_month}.txt")
                with open(output_path, 'w', encoding='utf-8') as output_file:
                    process_files_for_month(os.path.join(root_directory, category), output_file, user_month)
            else:
                for subcategory in subcategories:
                    subcat_directory = os.path.join(cat_directory, subcategory)
                    create_directory(subcat_directory)
                    output_path = os.path.join(subcat_directory, f"relatorio_{subcategory}.txt")
                    with open(output_path, 'w', encoding='utf-8') as output_file:
                        process_files_for_month(os.path.join(root_directory, subcategory), output_file, user_month, is_detailed=False)

        print("Relatório concluído com sucesso ✅")

        continuar = input("Deseja gerar outro relatório? (S/N): ").strip().upper()
        if continuar != "S":
            break

if __name__ == "__main__":
    main()
