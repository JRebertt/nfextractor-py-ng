import os

class FileManager:
    @staticmethod
    def create_directory(path):
        """
        Cria um diretório no caminho especificado se ele não existir.

        :param path: Caminho para o diretório a ser criado.
        """
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def find_pdf_files(directory):
        """
        Encontra todos os arquivos PDF em um diretório e seus subdiretórios.

        :param directory: O diretório raiz onde a busca por arquivos PDF começará.
        :return: Uma lista de tuplas, onde cada tupla contém o caminho do diretório e o nome do arquivo PDF.
        """
        pdf_files = []
        for root, _, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith('.pdf'):
                    pdf_files.append((root, file_name))
        return pdf_files