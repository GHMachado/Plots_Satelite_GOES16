# 🛰️ Imagens de Satélite GOES16 - Canal 13 ☁️

> Adaptado de: https://github.com/evmpython/minicurso_nowcasting_CPAM2024

## Bibliotecas necessárias

Para utilizar o script, algumas bibliotecas devem ser instaladas em uma determinada sequência no ambiente anaconda (Recomenda-se instalar em um ambiente virtual separado):
```
conda install -c conda-forge xarray cartopy boto3 gdal salem rasterio pyproj geopandas descartes
```
> Caso ocorra erro na instalação de alguma biblioteca, reinstale separadamente as bibliotecas, uma por uma, nessa mesma sequência.
> As bibliotecas geopandas e descartes são opcionais.

## Arquivos Auxiliares

Para o uso desse script, são necessário dois arquivos auxiliares:

- [utilities.py](https://github.com/GHMachado/Plots_Satelite_GOES16/blob/main/plot_sat.py): Script auxiliar para processamento das imagens.
- [IR4AVHRR6.cpt](https://github.com/GHMachado/Plots_Satelite_GOES16/blob/main/IR4AVHRR6.cpt): Paleta de cores para o Canal-13 utilizado nas imagens do CPTEC.

## Utilizando o Script

O script começa importando as bibliotecas necessárias, inclusive o [utilities.py](https://github.com/GHMachado/Plots_Satelite_GOES16/blob/main/utilities.py), que deve ficar na mesma pasta do script principal.

### Diretórios

A primeira parte do script, insira os seus próprios diretórios para o Download dos dados e imagens
```
input = "D:/es2/satelite/input"; os.makedirs(input, exist_ok=True) # Os dados do Download vão para este diretório
output = "D:/es2/satelite/input/imagens"; os.makedirs(output, exist_ok=True) # As imagens serão salvas nesse diretório
```

### Download de dados

Caso você não possua os dados .nc de satélite, é possível baixar pelo script.
Insira o Ano, Mês, Dia, Hora e Minuto inicial e final, junto do canal:
```
anoi, mesi, diai, hori, mini = 2024, 4, 9, 11, 0  # ano, mês e dia inicial do período 2024-04-09 11:00
anof, mesf, diaf, horf, minf = 2024, 4, 11, 23, 50  # ano, mês e dia final do período 2024-04-11 23:50
band = '13'
```
Para determinar o intervalo de tempo entre um download e outro, altere nessa linha:
```
for file in pd.date_range(date_ini, date_end, freq='60min'):
```
O intervalo precisa ser em minutos, então se eu quiser um intervalo de 12 em 12 horas de dados:
```
for file in pd.date_range(date_ini, date_end, freq='720min'):
```

### Gerando as imagens

Após fazer o download dos dados, ou caso já tenha os dados, apenas execute o código a partir de:
```
# Padrão de nome dos arquivos (ajuste conforme necessário)
padrao_nome_arquivo = 'OR_ABI-L2-CMIPF-M6C13_G16_*'
```
Caso queira mudar a paleta de cores em outro arquivo .cpt, apenas altere essa linha:
```
# Converte um arquivo .cpt (Recomendado para banda 13 - Infravermelho)
cpt = loadCPT('IR4AVHRR6.cpt') # Coloque na pasta que se encontra o código # Pode alterar para outros cmaps, só ter o arquivo.
colormap = cm.colors.LinearSegmentedColormap('cpt', cpt)
```
Sinta-se a vontade para personalizar o mapa do seu gosto.

### Possíves erros e soluções

Ao ler os arquivos e gerar imagens, o código cria arquivos adicionais na pasta em que os mesmo se encontram. Caso for executar novamente, você precisa excluir esses arquivos adicionais que foram gerados. Caso não faça isso, o código irá tentar ler esses arquivos e dará erro.

## Exemplos de imagens geradas



## Contribuidores

<a href="https://github.com/GHMachado/Plots_Satelite_GOES16/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=GHMachado/Plots_Satelite_GOES16" />
</a>
