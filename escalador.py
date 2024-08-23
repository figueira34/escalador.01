import pandas as pd
import requests
import json

# Formations dictionary
formacao = {
    "3-4-3": {"Goleiro": 1, "Zagueiro": 3, "Lateral": 0, "Meia": 4, "Atacante": 3, "Técnico": 1},
    "3-5-2": {"Goleiro": 1, "Zagueiro": 3, "Lateral": 0, "Meia": 5, "Atacante": 2, "Técnico": 1},
    "4-3-3": {"Goleiro": 1, "Zagueiro": 2, "Lateral": 2, "Meia": 3, "Atacante": 3, "Técnico": 1},
    "4-4-2": {"Goleiro": 1, "Zagueiro": 2, "Lateral": 2, "Meia": 4, "Atacante": 2, "Técnico": 1},
    "5-3-2": {"Goleiro": 1, "Zagueiro": 3, "Lateral": 2, "Meia": 3, "Atacante": 2, "Técnico": 1},
    "5-4-1": {"Goleiro": 1, "Zagueiro": 3, "Lateral": 2, "Meia": 4, "Atacante": 1, "Técnico": 1}
}

def run_my_code(selected_formation):
    url = 'https://api.cartola.globo.com/partidas'
    resposta = requests.get(url)
    objetos = json.loads(resposta.text)

    clubes = pd.json_normalize(objetos['clubes'].values())
    partidas = pd.json_normalize(objetos['partidas'])

    mapping = {'d': 0, 'e': 1, 'v': 3}

    def calculate_score(results):
        scores = [mapping[result] for result in results]
        total_score = sum(scores)
        average_score = total_score / len(scores)
        return average_score

    partidas['mandante_nota'] = partidas['aproveitamento_mandante'].apply(calculate_score)
    partidas['visitante_nota'] = partidas['aproveitamento_visitante'].apply(calculate_score)

    mandante = pd.merge(partidas, clubes[['id', 'nome']], left_on='clube_casa_id', right_on='id')
    mandante = mandante.rename(columns={'nome': 'Mandante', 'clube_casa_id': 'ID Mandante'})
    mandante = mandante.drop(columns=['id'])

    final = pd.merge(mandante, clubes[['id', 'nome']], left_on='clube_visitante_id', right_on='id')
    final = final.rename(columns={'nome': 'Visitante', 'clube_visitante_id': 'ID Visitante'})
    final = final.drop(columns=['id'])

    final['Diferença'] = final['mandante_nota'] - final['visitante_nota']
    final = final[['Mandante', 'ID Mandante', 'mandante_nota', 'Visitante', 'ID Visitante', 'visitante_nota', 'Diferença']].rename(columns={'mandante_nota': 'Nota Mandante', 'visitante_nota': 'Nota Visitante'})

    mandante_df = final[final['Diferença'] > 0.5][['Mandante', 'ID Mandante', 'Diferença']].rename(columns={'Mandante': 'Time', 'ID Mandante': 'ID'})
    visitante_df = final[final['Diferença'] < -0.5][['Visitante', 'ID Visitante', 'Diferença']].rename(columns={'Visitante': 'Time', 'ID Visitante': 'ID'})
    escalar = pd.concat([mandante_df, visitante_df], ignore_index=True)
    escalar['Diferença'] = abs(escalar['Diferença'])
    escalar = escalar.sort_values(by='Diferença', ascending=False).reset_index(drop=True)

    url2 = 'https://api.cartola.globo.com/atletas/mercado'
    resposta2 = requests.get(url2)
    objetos2 = json.loads(resposta2.text)

    atletas = pd.json_normalize(objetos2['atletas'])
    provavel = atletas[atletas['status_id'] == 7]

    jogadores = pd.merge(provavel, escalar[['ID']], left_on='clube_id', right_on='ID')
    jogadores = jogadores.drop(columns=['ID'])

    posicao_map = {
        1: 'Goleiro',
        2: 'Lateral',
        3: 'Zagueiro',
        4: 'Meia',
        5: 'Atacante',
        6: 'Técnico'
    }

    posicoes = {
        1: selected_formation["Goleiro"],
        2: selected_formation["Lateral"],
        3: selected_formation["Zagueiro"],
        4: selected_formation["Meia"],
        5: selected_formation["Atacante"],
        6: selected_formation["Técnico"]
    }

    starters = []
    for pos_id, count in posicoes.items():
        starters += jogadores[jogadores['posicao_id'] == pos_id] \
                        .nlargest(count, 'media_num').to_dict('records')

    starters_df = pd.DataFrame(starters)
    starters_df = starters_df[['atleta_id', 'apelido', 'media_num', 'pontos_num', 'jogos_num', 'preco_num', 'posicao_id']]

    reserves = []
    for pos_id in [1, 2, 3, 4, 5]:  # Excluding Técnico (6)
        cheapest_starter_price = starters_df[starters_df['posicao_id'] == pos_id]['preco_num'].min()
        
        reserve = jogadores[
            (jogadores['posicao_id'] == pos_id) & 
            (jogadores['preco_num'] < cheapest_starter_price)
        ].nlargest(1, 'media_num')
        
        if not reserve.empty:
            reserves.append(reserve.iloc[0].to_dict())

    reserves_df = pd.DataFrame(reserves)

    final_roster = pd.concat([starters_df, reserves_df]).rename(columns={'atleta_id': 'Id', 'apelido': 'Nome', 'media_num': 'Média', 'pontos_num': 'Última Rodada', 'jogos_num': 'Jogos', 'preco_num': 'Preço', 'posicao_id': 'Posição'})
    final_roster['Posição'] = final_roster['Posição'].map(posicao_map)

    # Return both DataFrames
    return starters_df, final_roster[['Id', 'Nome', 'Média', 'Última Rodada', 'Jogos', 'Preço', 'Posição']]
