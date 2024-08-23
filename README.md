# ⚽ Escalador Cartola FC

### Descrição

O **Escalador Cartola FC** é um aplicativo desenvolvido com Streamlit que permite aos usuários escolher uma formação de futebol e gerar uma escalação com base em uma lógica pré-estabelecidade. O aplicativo exibe a escalação selecionada e permite o download dos dados em formato CSV.

### Funcionalidades

- Seleção de formações de futebol
- Geração de escalação com base na formação escolhida
- Exibição da escalação em uma tabela
- Cálculo e exibição dos totais de média e preço
- Opção para baixar a escalação em formato CSV

#### Link: <https://escalador01.streamlit.app/>

------

### Parâmetros para a Escalação

Este projeto tem como objetivo montar uma escalação vencedora utilizando exclusivamente as informações extraídas da API Oficial do Cartola FC.

A API disponibiliza as informações sobre os jogos válidos para a próxima rodada, além dos resultados dos últimos 5 jogos de cada time. Com base nesses 5 jogos, atribuo uma pontuação a cada time: vitória vale 3 pontos, empate vale 1 ponto, e derrota não pontua. Em seguida, divido o total por 5 para gerar uma nota de 0 a 3 para cada time.

A diferença entre as notas dos times que irão se enfrentar é então calculada. Damos preferência para times mandantes com vantagem positiva e para times visitantes com vantagem superior a 0.25. Com esses parâmetros, o código seleciona os jogadores prováveis com as melhores médias dos times que apresentam vantagem.
