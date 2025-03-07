import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID =  os.getenv("Client_ID") 
CLIENT_SECRET = os.getenv("Client_Secret")
SPOTIPY_REDIRECT_URI = "http://localhost:8888/callback"

scope = "playlist-modify-public"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = CLIENT_ID, 
                                                   client_secret = CLIENT_SECRET,
                                                   redirect_uri = SPOTIPY_REDIRECT_URI,
                                                   scope = scope))

# FUNÇÃO 1: PLAYLIST COM AS MELHORES MUSICAS DE ARTISTAS SUGERIDOS PELO USUÁRIO #
def as_melhores():

    artistas = [] # lista de artistas inicialmente vazia
    playlist = [] # lista de musicas inicalmente vazia

    while True: # loop para coletar os artistas e o número de musicas desejadas
        artista = input("Digite o nome de um artista (ou 'sair' para encerrar): ")
        if artista.lower() == "sair": # verifica se o usuário quer encerrar o loop
            break
        num_musicas = int(input(f"Quantas músicas deseja para {artista}? ")) # pede o número de musicas desejada
        artistas.append((artista, num_musicas)) # armazena o artista/banda e o respectivo numero de musicas sugeridos pelo usuario à lista

    for artista, num_musicas in artistas: # monta playlist com as melhores de cada artista da lista
        resultado = sp.search(q=artista, type='artist', limit = 1) # busca o artista escolhido no spotify
        if resultado['artists']['items']: # verifica se o artista ou banda foi escolhido
            id_artista = resultado['artists']['items'][0]['id'] # armazena o id do artista ou banda
            top_musicas = sp.artist_top_tracks(id_artista, country = 'US') # obtem as melhores musicas do artista ou banda selecionada
            for track in top_musicas['tracks'][:num_musicas]: # seleciona a quantidade escolhida de musica para o determinado artista ou banda
                playlist.append(track['name']) # armazena as musicas à lista

    print("\nLista de artistas escolhidos:") # imprime lista de artista
    for artista in artistas:
        print(artista)

    print("\nPlaylist gerada:") # imprime a playlist gerada
    for musica in playlist:
        print(musica)

    return playlist


# FUNÇÃO 2: USUARIO ESCREVE PLAYLIST MANUALMENTE COM AS MUSICAS QUE DESEJAR #
def escrever_playlist():
    playlist = [] # lista de musicas inicalmente vazia

    print("\nDigite o nome das músicas que deseja adicionar à sua playlist! Digite 'sair' para finalizar.") # imprime instruções para o usuário

    while True:
        musica = input("Digite o nome da música: ") # pede o nome da musica que o usuario deseja adicionar à playlist
        if musica.lower() == "sair": # verifica se o usuário quer encerrar
            break
        playlist.append(musica) # armazena as musicas à lista 

    print("\nEssa é a sua playlist!") # Imprimir playlist enumerada
    for i, item in enumerate(playlist, 1): 
        print(f"{i}. {item}")

    return playlist 


# FUNÇÃO QUE INTEGRA A PLAYLIST AO SPOTIFY #
def cria_playlist(lista_musicas):

    playlist_nome = input("\nDigite o nome que deseja colocar na sua playlist: ") # armazena o nome escolhido pelo usuário
    playlist_descricao = input("\nDigite a descrição que deseja ter em sua playlist: ") # armazena a descrição ecrita pelo usuário

    user_id = sp.current_user()["id"] # nome do usuário no spotify

    # cria a playlist de acordo com o escolhido pelo usuário
    playlist = sp.user_playlist_create(
        user = user_id, 
        name = playlist_nome, 
        public = True, 
        description = playlist_descricao)

    playlist_id = playlist["id"] # obtem o id da playlist criada

    # loop que busca o id das músicas no Spotify
    track_ids = [] # lista de ids inicialmente vazia
    for musica in lista_musicas:
        result = sp.search(q=musica, limit=1, type="track") # busca o id da musica
        if result["tracks"]["items"]: # verifica se a busca retornou algumn id
            track_ids.append(result["tracks"]["items"][0]["id"]) # adiciona o id da musica buscada à lista de ids

    if track_ids:
        sp.playlist_add_items(playlist_id, track_ids) # adiciona as musicas na playlist criada
        print(f"{playlist_nome} criada com sucesso!")
    else:
        print("Nenhuma música encontrada.")


# FUNÇÃO PARA ESCOLHA DO CRIADOR DE PLAYLIST #
def menu(): 
    funcoes = {
        "1": as_melhores,
        "2": escrever_playlist,
    }
    
    while True:
        print("\nEscolha uma função para executar:")
        print("1 - Play list com 5 melhores de artistas ou bandas da sua escolha")
        print("2 - Digitar playlist manualmente")
        print("0 - Sair")
        
        escolha = input("Digite o número da opção desejada: ")
        
        if escolha == "0": # encerra o programa caso o usuário escolha 0
            print("Saindo...")
            break
        
        funcao = funcoes.get(escolha) # executa a função de acordo com a escolha do usuário
        if funcao:
            playlist = funcao() # executa a função de criar playlist e armazena na variavel playlist
            cria_playlist(playlist) # executa a função que integra a playlist ao spotify
            break # sai do loop após executar a função escolhida
        else:
            print("Opção inválida! Tente novamente.")


# executar o programa #
menu()