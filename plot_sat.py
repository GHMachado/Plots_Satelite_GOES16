# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 11:26:49 2024

@author: Gabriel M.
"""

#%%

# Adaptado de: https://github.com/evmpython/minicurso_nowcasting_CPAM2024/blob/main/cpam_basico_satelite_2024.ipynb

#========================================================================================================================#
#                                               Importando Bibliotecas
#========================================================================================================================#
import xarray as xr                                
import matplotlib.pyplot as plt                    
from matplotlib import cm                          
import cartopy, cartopy.crs as ccrs                
import cartopy.io.shapereader as shpreader         
from datetime import datetime                     
from utilities import download_CMI, remap, loadCPT # Colocar o arquivo (utilities.py) na mesma pasta do script
import numpy as np                                 
import os                                          
import pandas as pd
import time as t  
import glob
          
#%%                  
     
#========================================================================================================================#
#                                          Diretórios de entrada (input) e saída (output)
#========================================================================================================================#
input = "D:/es2/satelite/input"; os.makedirs(input, exist_ok=True) # Os dados do Download vão para este diretório
output = "D:/es2/satelite/input/imagens"; os.makedirs(output, exist_ok=True) # As imagens serão salvas nesse diretório

#========================================================================================================================#
#                                               Download dos arquivos direto do AWS
#========================================================================================================================#

# Escolha a data inicial, final e a banda
anoi, mesi, diai, hori, mini = 2024, 4, 9, 11, 0  # ano, mês e dia inicial do período 2022-02-02 00:00
anof, mesf, diaf, horf, minf = 2024, 4, 9, 11, 0  # ano, mês e dia final do período 2022-02-02 23:50
band = '13'

# Inicia o contador de tempo
start_time = t.time()

date_in = datetime(anoi, mesi, diai, hori, mini)  # 2022-02-02 00:00:00
date_ini = date_in.strftime('%Y%m%d%H%M') # 20220202

date_en = datetime(anof, mesf, diaf, horf, minf)
date_end = date_en.strftime('%Y%m%d%H%M')

print('.... Processando Data ...:', date_ini, date_end)

for file in pd.date_range(date_ini, date_end, freq='60min'):

    # Download the file

    yyyymmddhhmn = file.strftime('%Y%m%d%H%M')
    file_name = download_CMI(yyyymmddhhmn, band, input)

    print('\n---------------------')
    print('Downloading NC File:')
    print('---------------------')
    print('Model:GOES / Canal:' + band)
    #print('File:' + file_name)
    print('---------------------')

print('\nTempo de download dos dados:', round((t.time() - start_time),2), 'segundos.')

# Padrão de nome dos arquivos (ajuste conforme necessário)
padrao_nome_arquivo = 'OR_ABI-L2-CMIPF-M6C13_G16_*'

# Lista de arquivos
arquivos = glob.glob(os.path.join(input, padrao_nome_arquivo))

#%%

#========================================================================================================================#
#                                          Reprojeção da imagem e Leitura dos dados
#========================================================================================================================#
for arquivo in arquivos:

    # Designar a extensão (West Lon, South Lat, East Lon, North Lat)
    extent = [-44.00, -27.00, -41.00, -24.00]
    
    # Executa a Função de reprojeção (file, variable, extent, resolution)
    grid = remap(arquivo, 'CMI', extent, 2)
    
    # Lê os dados do arquivo e converte para °C
    data = grid.ReadAsArray() - 273.15
    
#%%
    # Escolhe o tamanho da figura
    plt.figure(figsize=(20,20))
    
    # Utiliza a projeção da coordenada cilindrica equidistante 
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    # Define a extensão da imagem
    img_extent = [extent[0], extent[2], extent[1], extent[3]] # Min lon, Max lon, Min lat, Max lat
    
    # Converte um arquivo .cpt (Recomendado para banda 13 - Infravermelho)
    cpt = loadCPT('IR4AVHRR6.cpt') # Coloque na pasta que se encontra o código # Pode alterar para outros cmaps, só ter o arquivo.
    colormap = cm.colors.LinearSegmentedColormap('cpt', cpt)
    
    # Plota a imagem no canal 13 - IR
    vmin = -103.0; vmax = 87
    img = ax.imshow(data, origin='upper', vmin=vmin, vmax=vmax, extent=img_extent, cmap=colormap)
    
    # Plota a imagem no canal 8 - WV
    # img = ax.imshow(data, origin='upper', extent=img_extent)
    # wv_norm, wv_cmap = colortables.get_with_range('WVCIMSS_r', -98, 15)
    # img.set_cmap(wv_cmap)
    # img.set_norm(wv_norm)
    
    # Adiciona linhas costeiras, fronteiras e linhas de grade
    #ax.coastlines(resolution='10m', color='black', linewidth=0.8) # Linhas costeiras
    #ax.add_feature(cartopy.feature.BORDERS, edgecolor='black', linewidth=0.5) # Fronteiras
    gl = ax.gridlines(crs=ccrs.PlateCarree(), color='#545454',
                      alpha=1.0,
                      linestyle='-',
                      linewidth=0.25,
                      xlocs=np.arange(-180, 180, 0.5),
                      ylocs=np.arange(-90, 90, 0.5),
                      draw_labels=True)
    
    gl.xlabel_style = {'size': 15} # Altera o tamanho do graus do eixo x
    gl.ylabel_style = {'size': 15} # Altera o tamanho do graus do eixo y
    gl.top_labels = False
    gl.right_labels = False
    
    # Plota o shapefile
    shapefile = list(shpreader.Reader('D:/es2/GFS-analysis_and_forecast-main/shapefiles/BR_UF_2021/BR_UF_2021.shp').geometries())
    ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='black', facecolor='none', linewidth=0.5)
    
    for i, (nome, lon, lat) in enumerate(zip(nomes, longitudes, latitudes)):
        marcador = markers[i % num_markers]  # Cicla pelos marcadores caso existam mais estações do que marcadores
        ax.scatter(lon, lat,
                   color='purple', 
                   s=300, 
                   marker=marcador,  # Define o marcador
                   label=nome,  # Adiciona o nome da estação como rótulo
                   transform=ccrs.PlateCarree())
        
    # Adicionar a legenda automaticamente
    plt.legend(loc='lower left',
               fontsize=25,
               title="Plataformas",
               title_fontsize=25)
    
    # Adiciona uma Cbar
    cbar = plt.colorbar(img, label='Temperatura de Brilho (°C)', extend='neither', orientation='horizontal', pad=0.05, fraction=0.05, aspect=50, shrink=0.9)
    cbar.ax.tick_params(labelsize=14)
    cbar.set_label('Temperatura de Brilho (°C)', fontsize=16)
    
    # Lê o horário e a data do arquivo e converte para uma string
    date = (datetime.strptime(xr.open_dataset(arquivo).time_coverage_start, '%Y-%m-%dT%H:%M:%S.%fZ')).strftime('%d-%m-%Y %H:%M UTC')
    
    # Adiciona um título
    plt.title('GOES-16 Band 13 (10.3 µm)', fontweight='bold', fontsize=18, loc='left') # Ajuste como preferir
    plt.title(f'Análise: {date}', fontsize=18, loc='right')
    
    # Salva a imagem
    plt.savefig(f'{output}/band_13_{date.replace(":", "_")}.png', bbox_inches='tight', dpi=300) # Para mudar o diretório, mude em output
    plt.show()
