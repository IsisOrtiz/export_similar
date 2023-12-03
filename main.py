from io import StringIO
import numpy as np
import spacy
import streamlit as st
import pandas as pd

nlp = spacy.load('pt_core_news_sm')
dados1 = []
dados2 = []
dados_processados = []
btnExport = None
btnProcess = None
indice_predict = st.sidebar.slider(
    'selecione o indice de similaridade ',
    0.0, 1.0, (0.1)
    )



def get_sentence_vector(sentence):
    doc = nlp(sentence)
    vectors = [word.vector for word in doc if word.has_vector]
    if vectors:
        return np.mean(vectors, axis=0)
    else:
        return np.zeros_like(nlp.vocab.vectors[0])
    
def convert_df(_data):
    df = pd.DataFrame(_data, columns = ['frase1', 'frase2', 'similaridade', 'indice'])
    return df.to_csv(index=False, sep=";").encode('utf-8')


#funcao para obter o indice de similaridade
def getindice():
    indice_predict = st.sidebar.slider(
    'selecione o indice de similaridade ',
    0.0, 1.0, (0.1)
    )
    return indice_predict
#funcao para processar os dados
def process(_data1, _data2, _cosine_similarities):
    _dados_processados = []

    total_iterations_raiz = len(_data1)

    progress_text_raiz = "Agurade o processamento dos dados do arquivo raiz"
    progess_bar_raiz = st.progress(0, text=progress_text_raiz)

    progress_text = "Por favor agurde o processamento dos dados."
    progess_bar = st.progress(0, text=progress_text)


    for i, sentence1 in enumerate(_data1):

        current_progress_raiz = i / total_iterations_raiz
        progess_bar_raiz.progress(current_progress_raiz, text=progress_text_raiz)

        for j, sentence2 in enumerate(_data2):

            current_progress = j / len(_data2)
            progess_bar.progress(current_progress, text=progress_text)

            similarity = _cosine_similarities[i, j]
            
            if similarity >= indice_predict:
                _dados_processados.append([sentence1, sentence2, similarity, indice_predict])

    progess_bar_raiz.empty()
    progess_bar.empty()

    return _dados_processados


#Calcula a similaridade de frases########################
def getsimilarity(phrase1:str , phrase2:str):

    doc1 = nlp(phrase1)
    doc2 = nlp(phrase2)

    similaridade = doc1.similarity(doc2)

    return similaridade

#faz upload do arquivo 1
def upload_file1():
    # Widget para upload de arquivo
    uploaded_file = st.file_uploader("Selecione o primeiro arquivo txt", type="txt")

    if uploaded_file is not None:

        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

        # To read file as string:
        string_data = stringio.readlines()
        # To read file line by line:
        for line in string_data:
            # Exibir cada linha no Streamlit
            line = line.strip()
            dados1.append(line)
#faz upload do arquivo 2
def upload_file2():
    # Widget para upload de arquivo
    uploaded_file = st.file_uploader("Selecione o segundo arquivo txt", type="txt")

    if uploaded_file is not None:

        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

        # To read file as string:
        string_data = stringio.readlines()
        # To read file line by line:
        for line in string_data:
            # Exibir cada linha no Streamlit
            line = line.strip()
            dados2.append(line)

def main():
    
    cosine_similarities = None

    st.title('Exportação de frases, conforme similaridade - v0.2.1 !')
    st.title(':blue[Isis] :sunglasses:')
    st.write('Similaridade selecionada: ', indice_predict)
    upload_file1()
    upload_file2()

    if len(dados1) > 0 and len(dados2) > 0:
        # Calculando os vetores médios para cada lista de frases
        vectors_data1 = [get_sentence_vector(sentence) for sentence in dados1]
        vectors_data2 = [get_sentence_vector(sentence) for sentence in dados2]

        # Normalizando os vetores
        vectors_data1_normalized = [vector / np.linalg.norm(vector) for vector in vectors_data1]
        vectors_data2_normalized = [vector / np.linalg.norm(vector) for vector in vectors_data2]

        # Calculando a similaridade de cosseno para todas as combinações de frases
        cosine_similarities = np.zeros((len(dados1), len(dados2)))

        for i, vector1 in enumerate(vectors_data1_normalized):
            for j, vector2 in enumerate(vectors_data2_normalized):
                cosine_similarities[i, j] = np.dot(vector1, vector2)

    col1, col2, col3, col4, col5, col6  = st.columns(6, gap="small")

    with col1:
        btnProcess = st.button("processar")

    with col2:
        btnExport = st.button("exportar")

    if btnProcess:
        if len(dados1) == 0 or len(dados2) == 0:
            st.write("Não existem dados para processar!")
        else:
            #Processar dados
            dados_processados = process(dados1, dados2, cosine_similarities)
            st.write(dados_processados)
    elif btnExport:
        if len(dados1) == 0 or len(dados2) == 0:
            st.write("Não existem dados para processar!")
        else:
            #Processar dados
            dados_processados = process(dados1, dados2, cosine_similarities)
            csv = convert_df(dados_processados)
            st.download_button(
            "Press to Download CSV",
            csv,
            "file.csv",
            "text/csv",
            key='download-csv'
            )

##########################################################


if __name__ == "__main__":
    main()


