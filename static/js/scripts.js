document.addEventListener('DOMContentLoaded', function() {
    const numQuestoesInput = document.getElementById('num_questoes');
    const questoesContainer = document.getElementById('questoes-container');
    const alternativas = ['A', 'B', 'C', 'D', 'E'];

    function renderQuestoes() {
        const numQuestoes = parseInt(numQuestoesInput.value);
        questoesContainer.innerHTML = ''; // Limpa o container antes de adicionar novas questões

        for (let i = 1; i <= numQuestoes; i++) {
            const questaoDiv = document.createElement('div');
            questaoDiv.classList.add('questao-item');
            questaoDiv.innerHTML = `
                <h3>Questão ${i}</h3>
                <div class="form-group">
                    <label for="enunciado_q${i}">Enunciado da Questão ${i}:</label>
                    <textarea id="enunciado_q${i}" name="enunciado_q${i}" rows="3" required></textarea>
                </div>
                <div class="form-group">
                    <label>Alternativas:</label>
                    ${alternativas.map(alt => `
                        <div class="alternativa-group">
                            <label for="alt_${alt}_q${i}">(${alt}) Texto:</label>
                            <input type="text" id="alt_${alt}_q${i}" name="alt_${alt}_q${i}" required>
                            <label for="peso_alt_${alt}_q${i}">Peso:</label>
                            <input type="number" id="peso_alt_${alt}_q${i}" name="peso_alt_${alt}_q${i}" step="0.1" value="0.0" required>
                        </div>
                    `).join('')}
                </div>
                <div class="form-group">
                    <label for="peso_q${i}">Peso da Questão ${i}:</label>
                    <input type="number" id="peso_q${i}" name="peso_q${i}" step="0.1" value="1.0" required>
                </div>
                <hr>
            `;
            questoesContainer.appendChild(questaoDiv);
        }
    }

    // Renderiza as questões iniciais
    renderQuestoes();

    // Adiciona listener para renderizar questões quando o número muda
    numQuestoesInput.addEventListener('change', renderQuestoes);
    numQuestoesInput.addEventListener('keyup', renderQuestoes); // Para quando o usuário digita
});