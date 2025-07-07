from flask import Flask, render_template, request, send_file, redirect, url_for
import os
import datetime
import sys
# Adiciona o diretório atual ao PATH do Python para que possa importar gerar_provas
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import gerar_provas # Importa seu script refatorado

app = Flask(__name__)

# Configuração do diretório de uploads/downloads
# Assegura que o diretório download_provas existe
DOWNLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'download_provas')
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gerar_provas', methods=['POST'])
def gerar_provas_web():
    professor_nome = request.form['professor_nome']
    data_prova = request.form['data_prova']
    turma_nome = request.form['turma_nome']
    num_questoes = int(request.form['num_questoes'])

    # Geração do conteúdo do entrada.txt
    entrada_content = []
    for i in range(1, num_questoes + 1):
        q_id = f"Q{i}"
        enunciado = request.form[f'enunciado_q{i}']
        peso_questao = request.form[f'peso_q{i}']

        entrada_content.append(f"{q_id}|{peso_questao}")
        entrada_content.append(enunciado)

        for alt_letra in gerar_provas.ALTERNATIVAS: # Usar a lista de alternativas do seu script
            alt_texto = request.form[f'alt_{alt_letra}_q{i}']
            alt_peso = request.form[f'peso_alt_{alt_letra}_q{i}']
            entrada_content.append(f"{alt_letra}|{alt_texto}|{alt_peso}")

    # Cria um nome de arquivo único para evitar colisões
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = f"prova_{professor_nome.replace(' ', '_')}_{turma_nome}_{timestamp}"

    entrada_txt_path = os.path.join(DOWNLOAD_FOLDER, f"{base_filename}_entrada.txt")
    provas_docx_path = os.path.join(DOWNLOAD_FOLDER, f"{base_filename}_Provas.docx")
    gabarito_txt_path = os.path.join(DOWNLOAD_FOLDER, f"{base_filename}_gabarito.txt")

    # Salva o conteúdo no entrada.txt temporário
    with open(entrada_txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(entrada_content))

    try:
        # Chama as funções do script gerar_provas.py
        gabarito_base = gerar_provas.ler_entrada_txt(entrada_txt_path)
        todas_provas = gerar_provas.gerar_provas(gabarito_base, num_tipos=4)
        gerar_provas.salvar_gabarito_arquivo(todas_provas, gabarito_txt_path)
        gerar_provas.gerar_word_unificado(todas_provas, provas_docx_path)

        return render_template('index.html',
                               message="Provas geradas com sucesso!",
                               docx_file=os.path.basename(provas_docx_path),
                               gabarito_file=os.path.basename(gabarito_txt_path))

    except Exception as e:
        return render_template('index.html', error=f"Erro ao gerar provas: {e}")

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "Arquivo não encontrado.", 404

if __name__ == '__main__':
    app.run(debug=True)