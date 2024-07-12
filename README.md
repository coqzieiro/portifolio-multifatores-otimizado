# Portfólio Multifatores
Alocação de ações em modelos de portfólios que seguem os índices de referência. O objetivo é obter um modelo que maximizar o retorno e outro que visa maximizar a relação entre retorno/volatilidade.

## Instalação das dependências

<i>pip install Riskfolio-Lib</i>

## Execução

<i>python3 plotGraph.py</i>

## Método Experimental

<ol>
  <li><strong>Importação e Preparação dos Dados:</strong>
      <ul>
          <li>Foram importados dados de composição do índice IBX, preços de fechamento dos ativos, índices de referência (Ibovespa, IBX, SELIC), e os fatores ROIC, Momentum, Valor de Mercado, P/V Patrimonial e Volatilidade.</li>
      </ul>
  </li>
  <li><strong>Definição dos Períodos e Parâmetros:</strong>
      <ul>
          <li>O período de análise foi definido entre janeiro de 2005 e dezembro de 2021.</li>
          <li>Parâmetros para rebalanceamento e avaliação foram estabelecidos (1 mês para ambos).</li>
      </ul>
  </li>
  <li><strong>Seleção de Ações para o Portfólio:</strong>
      <ul>
          <li>Portfólio com um Fator: A função <code>SelPort1</code> é utilizada para selecionar ações baseadas em um único fator dentro de um intervalo de rankings.</li>
          <li>Portfólio com Dois Fatores: A função <code>SelPort2Par</code> é utilizada para selecionar ações que atendem aos critérios de dois fatores simultaneamente.</li>
      </ul>
  </li>
  <li><strong>Avaliação de Portfólios e Índices de Referência:</strong>
      <ul>
          <li>A função <code>EvalPort</code> avalia um portfólio calculando o retorno acumulado, o retorno periódico, o drawdown, o retorno anualizado e a volatilidade anualizada.</li>
          <li>A função <code>EvalRef</code> faz o mesmo para os índices de referência (Ibovespa, IBX, SELIC).</li>
      </ul>
  </li>
  <li><strong>Otimização de Portfólio usando Riskfolio-Lib:</strong>
      <ul>
          <li>Risk Parity (RP): Busca equilibrar os riscos dos ativos no portfólio.</li>
          <li>Global Minimum Variance (GMV): Minimiza a variância total do portfólio.</li>
          <li>Maximum Decorrelation Portfolio (MDP): Maximiza a descorrelação entre os ativos do portfólio.</li>
          <li>A função <code>calc_riskfolio_opt</code> implementa estas otimizações, calculando os pesos ótimos dos ativos usando dados históricos de retornos.</li>
      </ul>
  </li>
  <li><strong>Análise e Comparação:</strong>
      <ul>
          <li>Vários portfólios são avaliados e comparados, incluindo aqueles baseados em <code>volatilidade</code>, <code>ROIC</code>, <code>Momentum</code> e <code>PVP</code>, e combinações de ambos os fatores.</li>
          <li>São calculados e comparados indicadores como <i>retorno acumulado, retorno anualizado, volatilidade anualizada, drawdown, e a relação retorno/volatilidade</i>.</li>
          <li>A performance dos portfólios é visualizada ao longo do tempo, comparando-se também com índices de referência como o <code>IBX</code>.</li>
      </ul>
  </li>
  <li><strong>Visualização de Resultados:</strong>
      <ul>
          <li>A evolução das quotas dos portfólios e índices de referência são plotadas para análise visual.</li>
      </ul>
  </li>
</ol>

## Análise Modelo 1: Maior Retorno

<ol>
    <li><strong>Ranked_PVP (Preço sobre Valor Patrimonial):</strong>
        <ul>
            <li>O P/VPA é um indicador financeiro que compara o preço de mercado de uma ação ao seu valor contábil por ação. A utilização do <code>ranked_pvp</code> significa que estamos selecionando ações com base em suas classificações de P/VPA.</li>
            <li>Em geral, ações com baixo <code>P/VPA</code> são consideradas subvalorizadas, e a seleção das melhores ações segundo este critério pode identificar empresas que estão sendo negociadas a um preço inferior ao seu valor contábil, oferecendo potencial de valorização.</li>
        </ul>
    </li>
    <li><strong>Ranked_Momentum:</strong>
        <ul>
            <li>Momentum se refere à tendência de continuação do desempenho passado das ações. Ações que têm mostrado um bom desempenho recente tendem a continuar a ter um bom desempenho no curto prazo.</li>
            <li>Utilizar <code>ranked_momentum</code> significa que estamos selecionando ações que tiveram um forte desempenho nos últimos períodos, o que pode indicar uma tendência de continuidade desse desempenho positivo.</li>
        </ul>
    </li>
    <li><strong>Máxima Descorrelação:</strong>
        <ul>
            <li>Descorrelação refere-se à seleção de ativos cujos retornos não são fortemente correlacionados entre si. Isso é importante porque a diversificação reduz o risco específico de cada ativo no portfólio.</li>
            <li>Ao maximizar a descorrelação, estamos criando um portfólio que é mais robusto às variações de mercado, reduzindo o risco total e potencialmente aumentando o retorno ajustado ao risco.</li>
        </ul>
    </li>
    <li><strong>Por que isso funciona?</strong>
        <ul>
            <li>Diversificação Efetiva: Com a máxima descorrelação, o portfólio é bem diversificado. Diversificação eficaz reduz o risco total sem necessariamente reduzir o retorno esperado. Portanto, o portfólio se torna mais estável e menos volátil.</li>
            <li>Aproveitamento de Anomalias de Mercado: Os fatores <code>P/VPA</code> e <code>momentum</code> são bem documentados na literatura financeira como anomalias que oferecem retornos superiores ao mercado. Investir com base nesses fatores permite capturar esses retornos adicionais.</li>
            <li>Seleção de Ações de Alta Qualidade e Potencial: As ações selecionadas com base no <code>ranked_pvp</code> são geralmente subvalorizadas e têm um bom potencial de crescimento, enquanto as ações com bom <code>ranked_momentum</code> indicam uma tendência positiva que pode continuar. Combinando esses fatores, você seleciona ações com bons fundamentos e um histórico recente positivo.</li>
        </ul>
    </li>
</ol>

## Análise Modelo 2: Maior Retorno/Volatilidade

<ol>
    <li><strong>ROIC (Return on Invested Capital):</strong>
        <ul>
            <li>Eficiência na Alocação de Capital: Empresas com altos ROICs tendem a ser mais eficientes na utilização de seus capitais para gerar lucros. Isso pode indicar que a empresa tem um modelo de negócios robusto, vantagens competitivas sustentáveis e boas práticas de gestão.</li>
            <li>Menor Probabilidade de Perda: Empresas com altos ROICs geralmente têm menor probabilidade de enfrentar dificuldades financeiras, o que pode reduzir a volatilidade de suas ações.</li>
        </ul>
    </li>
    <li><strong>Volatilidade:</strong>
        <ul>
            <li>Gestão de Risco: Selecionar ações com baixa volatilidade pode ajudar a minimizar os movimentos bruscos nos preços das ações, resultando em um portfólio mais estável. Isso é especialmente importante quando se busca um bom retorno ajustado ao risco.</li>
            <li>Previsibilidade: Ações com baixa volatilidade tendem a ser mais previsíveis, o que facilita a gestão do portfólio e pode levar a um desempenho mais consistente ao longo do tempo.</li>
        </ul>
    </li>
    <li><strong>Combinação de Fatores:</strong>
        <ul>
            <li>Sinergia: A combinação de fatores de alto ROIC e baixa volatilidade pode criar um portfólio de alta qualidade, onde você tem empresas eficientes que também apresentam estabilidade nos preços de suas ações.</li>
            <li>Mitigação de Riscos Específicos: Ao selecionar empresas com base em múltiplos critérios (ROIC e volatilidade), você está mitigando riscos específicos que podem estar presentes se você usar apenas um critério de seleção.</li>
            <li>Balanceamento de Risco: Ao equilibrar o risco entre os ativos, você está evitando a concentração de risco em uma única ação ou setor, o que pode ajudar a suavizar os retornos e reduzir a volatilidade.</li>
        </ul>
    </li>
</ol>
