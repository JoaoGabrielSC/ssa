# Pré requisitos:
- Python 3.11
- Node.js latest
- npm latest



# Instale os pré-requisitos:
1. Clone o repositório
2. Acesse a pasta do projeto
3. Instale as dependências do projeto
    
    ```bash
    # criar um ambiente virtual
    py -3.11 -m venv env
    # ativar o ambiente virtual
    .\env\Scripts\activate
    pip install -r requirements.txt
    # instalar as dependências do frontend
    cd web
    npm install
    ```
# Test de captura de região de interesse e processamento de imagem
- Para rodar o teste, execute o comando abaixo e acompanhe o resultado no terminal

```bash
    python show_region_in_video.py
```

# Executando o projeto
1. Rode o projeto

    ```bash
    cd web
    npm start
    ```
2. Rode a api

    ```bash
    python app.py
    ``` 
3. Acesse o projeto em http://localhost:3000

    
TODO:
(x) Input por vídeo -> apenas para test
(x) Na tela da camera mostrar região na imagem sem poder editar ela
(x) Fixar onde a região aparece para um tamanho fixo de 1080x720 e salvar no banco de dados
(x) VALOR INICIAL É SOMATÓRIO INICIAL DO INVERSO DE TODOS PIXELS DENTRO DA REGIÃO DE INTERESSE
() INDEX INICIAL, SLAG INDEX, IRON INDEX
() COLOCAR NA TELA DASHBOARD O SLAG INDEX X TIME, COLOCAR OS FILTROS PARA ANÁLISE


## anotações
-> if frame == 0 -> frame = 1, if frame ==255 -> frame = 256
-> Index : somatório do inverso da itensidade do pixels dentro da região delimitada
-> SlagIndex : somatório do inverso da itensidade dos pixels < threshold
-> Iron: somatório do inverso da itensidade dos pixels > threshold
