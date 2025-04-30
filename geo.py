#TODO: Dado um endereço, retorna a latitude e longitude
#TODO: dado duas coordenadas, retorna a distância entre elas (na malha viária)
#TODO: dado um polígono, ou uma localidade, plotar um mapa.
#TODO: dados duas coordenadas,plotar o caminho entre elas (rua a rua).

import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import folium
import os
import pickle
from shapely.geometry import Polygon
# from osmnx import utils_graph

def retorna_coordenada(endereco :str) -> tuple:
    """
    Dado um endereço, retorna a latitude e longitude
    """
    localizacao = ox.geocode(endereco)
    return localizacao

def dist_malha_viaria(origem:float, destino:float):
    """Recebe duas coordenadas geograficas e retorna a distância entre elas na malha viária"""
    rede = ox.graph_from_point(origem, dist=10000, network_type='drive')

    no_origem = ox.distance.nearest_nodes(rede, origem[1], origem[0])
    no_destino = ox.distance.nearest_nodes(rede, destino[1], destino[0])

    rota = nx.shortest_path(rede, no_origem, no_destino, weight='length')
    distancia = nx.shortest_path_length(rede, no_origem, no_destino, weight='length')
    return distancia, rede, rota

def plota_rota(rota, rede, titulo=None, salvar_arquivo=None):
    fig, ax = ox.plot_graph_route(rede, rota, node_size=0, edge_color='gray', bgcolor='white',show=False, close=False)

    if titulo:
        ax.set_title(titulo, color='white', fontsize=14)
    
    # Salva a figura em arquivo (opcional)
    if salvar_arquivo:
        fig.savefig(
            salvar_arquivo,
            dpi=300,
            bbox_inches='tight',
            facecolor='k'  # Mantém o fundo preto no arquivo
        )
    
    return fig, ax


def salva_mapa(nome_mapa: str) -> bool:
    if os.path.exists(f'{nome_mapa}.html'):
        # with open(f'{nome_mapa}.pkl', 'rb') as f:
        #     mapa = pickle.load(f)
        return nome_mapa
    else:
        rede = ox.graph_from_place(nome_mapa, network_type='drive')
        nodes, edges =  ox.graph_to_gdfs(rede)

        center = ox.geocode(nome_mapa)
        mapa = folium.Map(location = [center[0],center[1]], zoom_start=12)
        # Salva o mapa em um arquivo
        mapa.save(nome_mapa+'.html')
        print(f"Mapa salvo como {nome_mapa}.html")
        return rede


def plota_rota_mapa(rede, rota, origem=None, destino= None, zoom = 14, salvar_html = False, nome_mapa=None):
    
    coordenadas_rota = []
    origem_coord = retorna_coordenada(origem)
    destino_coord = retorna_coordenada(destino)

    for node in rota:
        node_data = rede.nodes[node]
        coordenadas_rota.append((node_data['y'], node_data['x']))
    
    if origem:
        centro = [(origem_coord[0] + destino_coord[0]) / 2, (origem_coord[1] + destino_coord[1]) / 2]
    else:
        lats = [coord[0] for coord in coordenadas_rota]
        lons = [coord[1] for coord in coordenadas_rota]
        centro = [(sum(lats) / len(lats)), (sum(lons) / len(lons))]
        # centro = [(max(lats) + min(lats)) / 2, (max(lons) + min(lons)) / 2]

    mapa = folium.Map(location=centro, zoom_start=zoom, tiles='OpenStreetMap')

    folium.PolyLine(
        locations=coordenadas_rota,
        color='#1a75ff',  # Azul vibrante
        weight=6,
        opacity=0.8,
        line_cap='round',
        popup='Rota calculada'
    ).add_to(mapa)
    
    # 5. Adiciona marcadores (usando coordenadas reais se fornecidas, ou primeiro/último nó)
    ponto_inicio =  origem_coord if origem_coord else coordenadas_rota[0]
    ponto_fim = destino_coord if destino_coord else coordenadas_rota[-1]
    
    folium.Marker(
        location=ponto_inicio,
        icon=folium.Icon(color='green', icon='play', prefix='fa'),
        popup='Origem'
    ).add_to(mapa)
    
    folium.Marker(
        location=ponto_fim,
        icon=folium.Icon(color='red', icon='stop', prefix='fa'),
        popup='Destino'
    ).add_to(mapa)

    if salvar_html:
        if not nome_mapa:
            nome_mapa = f'rota de {origem} para {destino}'
        mapa.save(f'{nome_mapa}.html')
        print(f'Mapa salvo como: {nome_mapa}.html')
    return mapa, distancia
    
   

if __name__=='__main__':
    # Testando as funções
    # localizacao = 'Caucaia, Ceará'
    # area_interesse = {'place': ox.geocode_to_gdf(localizacao), }
    # print(area_interesse['place'], area_interesse['polygon'])
    origem = 'Rua 347, Nova Metrópole, Caucaia, Ceará'
    destino = 'Centro de ciências, Campus do Pici, Fortaleza, Ceará'

    

    # print(f'Coordenadas de origem: {coordenadas_origem}')
    # print(f'Coordenadas de destino: {coordenadas_destino}')
    # print(f'Distância entre os pontos: {distancia} metros')
    # Exemplo de uso
    coords_origem = retorna_coordenada(origem)
    coords_destino = retorna_coordenada(destino)
    distancia, rede, rota = dist_malha_viaria(coords_origem, coords_destino)
    # fig, ax = plota_rota(rota, rede, titulo="Rota UFC", salvar_arquivo="minha_rota.png")
    # print(rota, rede)
    # Plota o caminho e salva como HTML
    mapa, distancia = plota_rota_mapa(rede, rota, origem, destino,  salvar_html=True)
    
    # print(f"Distância entre os pontos: {distancia} metros")
    
    # Para exibir o mapa diretamente no Jupyter Notebook:
    # mapa

    # salva_mapa('Caucaia')