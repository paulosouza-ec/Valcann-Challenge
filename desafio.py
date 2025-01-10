import os
import shutil
import time
from datetime import datetime, timedelta

'''Diretorios'''
origem = '/home/valcann/backupsFrom'
destino = '/home/valcann/backupsTo'
log_origem = '/home/valcann/backupsFrom.log'
log_destino = '/home/valcann/backupsTo.log'

'''listar os arquivos com informações de nome, tamanho, data de criação e última modificação'''
def listar_arquivos(caminho):
    arquivos_info = []
    for arquivo in os.listdir(caminho):
        arquivo_path = os.path.join(caminho, arquivo)
        if os.path.isfile(arquivo_path):
            info = os.stat(arquivo_path)
            nome = arquivo
            tamanho = info.st_size
            data_criacao = datetime.fromtimestamp(info.st_ctime)
            data_modificacao = datetime.fromtimestamp(info.st_mtime)
            arquivos_info.append((nome, tamanho, data_criacao, data_modificacao))
    return arquivos_info

''' Função para salvar o log de arquivos'''

def salvar_log(arquivos_info, arquivo_log):
    with open(arquivo_log, 'w') as log:
        for arquivo in arquivos_info:
            log.write(f"{arquivo[0]} - Tamanho: {arquivo[1]} bytes - "
                      f"Data de criação: {arquivo[2]} - Última modificação: {arquivo[3]}\n")

''' Função para remover arquivos com mais de 3 dias'''

def remover_arquivos_antigos(caminho, arquivos_info):
    data_limite = datetime.now() - timedelta(days=3)
    for arquivo in arquivos_info:
        if arquivo[2] < data_limite:
            arquivo_path = os.path.join(caminho, arquivo[0])
            os.remove(arquivo_path)
            print(f"Arquivo removido: {arquivo[0]}")

''' Função para copiar arquivos com até 3 dias para o destino'''

def copiar_arquivos_recentemente_criados(caminho_origem, caminho_destino, arquivos_info):
    data_limite = datetime.now() - timedelta(days=3)
    for arquivo in arquivos_info:
        if arquivo[2] >= data_limite:
            arquivo_origem_path = os.path.join(caminho_origem, arquivo[0])
            arquivo_destino_path = os.path.join(caminho_destino, arquivo[0])
            shutil.copy(arquivo_origem_path, arquivo_destino_path)
            print(f"Arquivo copiado: {arquivo[0]}")

    arquivos_origem = listar_arquivos(origem)
    

    salvar_log(arquivos_origem, log_origem)
    
  
    remover_arquivos_antigos(origem, arquivos_origem)
    

    copiar_arquivos_recentemente_criados(origem, destino, arquivos_origem)

    arquivos_destino = listar_arquivos(destino)

    salvar_log(arquivos_destino, log_destino)

