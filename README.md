
# Simulador Yamazumi (Streamlit)

Aplicativo Streamlit para gerar gráficos Yamazumi a partir de uma planilha Excel.

## Estrutura do projeto
```
/yamazumi-app
├─ app_yamazumi_streamlit.py
├─ requirements.txt
├─ README.md
└─ modelo_yamazumi_45_estacoes.xlsx   (opcional - exemplo)
```

## Como rodar localmente
1. Crie um ambiente (opcional) e instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Rode o app:
   ```bash
   streamlit run app_yamazumi_streamlit.py
   ```
   O Streamlit abrirá em `http://localhost:8501`.

## Formato da planilha
A planilha deve conter **três colunas**:
- `Estacao`: nome/índice da estação (ex.: "Estacao 1", "E1", etc.).
- `Tempo`: valor numérico do tempo por atividade/estação.
- `Categoria`: rótulo da atividade (ex.: "VA", "NVA", "MUDA").

No app, selecione se o tempo está em **segundos** ou **minutos**.

## Publicar no Streamlit Community Cloud
1. Crie um repositório no GitHub com estes arquivos.
2. Acesse https://streamlit.io/cloud e faça login com sua conta do GitHub.
3. Clique em **"Deploy an app"** e selecione o repositório, a branch (`main`) e o caminho `app_yamazumi_streamlit.py`.
4. Concluído o deploy, o app ficará disponível em um link `https://seuapp.streamlit.app`.

## Atualizações
Faça *commit* e *push* no GitHub; o Streamlit Cloud redeploya automaticamente.
