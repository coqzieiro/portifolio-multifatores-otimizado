# Portfólio Multifatores
Alocação de ações em modelos de portfólios que seguem os índices de referência. O objetivo é obter um modelo que maximizar o retorno e outro que visa maximizar a relação entre retorno/volatilidade.

## Instalação das dependências

<code><i>pip install Riskfolio-Lib</i></code>

## Execução

<code><i>python3 plotGraph.py</i></code>

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
   <li><strong>Ranked_ROIC (Retorno sobre o Capital Investido):</strong>
      <ul>
          <li>O ROIC é uma medida de eficiência que indica quanto uma empresa é capaz de gerar de retorno para cada unidade de capital investido. A utilização do <code>ranked_ROIC</code> significa que estamos selecionando empresas com base em sua capacidade de gerar valor a partir de seus investimentos.</li>
          <li>Empresas com um alto <code>ROIC</code> são frequentemente consideradas mais eficientes e capazes de gerar valor sustentável para os acionistas, o que pode representar uma vantagem competitiva no longo prazo.</li>
      </ul>
  </li>
  <li><strong>Ranked_Volatilidade:</strong>
      <ul>
          <li>Volatilidade refere-se à variação do preço de uma ação em um dado período. A utilização do <code>ranked_Vol</code> significa que estamos selecionando ações com base na estabilidade de seus preços no mercado.</li>
          <li>Ações com baixa volatilidade são geralmente consideradas menos arriscadas, enquanto ações com alta volatilidade podem oferecer maiores oportunidades de ganho (e risco) em curto prazo.</li>
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
          <li>Diversificação Efetiva: Com base na volatilidade, a seleção visa a estabilidade do portfólio. Ações com baixa volatilidade contribuem para uma diversificação que mitiga riscos sem comprometer o potencial de retorno, levando a um portfólio globalmente mais estável.</li>
          <li>Otimização de Retornos Ajustados ao Risco: O ROIC é uma métrica crucial para identificar empresas que geram retornos eficientes sobre o capital investido. Investir em empresas com alto ROIC pode oferecer uma vantagem, pois elas são capazes de gerar valor acima da média de forma sustentável.</li>
          <li>Seleção de Ações de Alta Eficiência e Estabilidade: As ações selecionadas com base em <code>ranked_ROIC</code> são eficientes em termos de geração de valor, enquanto aquelas com baixa <code>ranked_Vol</code> oferecem menos riscos de grandes flutuações. Esta combinação promove um equilíbrio entre eficiência na geração de valor e estabilidade de preço, aumentando o potencial de um desempenho favorável sustentado.</li>
      </ul>
  </li>
</ol>

## Análise Modelo 2: Maior Retorno/Volatilidade

<ol>
    <li><strong>Standard Risk Parity:</strong>
        <ul>
            <li>Equilíbrio de Risco: O modelo de Paridade de Risco Padrão distribui igualmente o risco entre todos os ativos no portfólio, o que ajuda a maximizar a diversificação e minimizar a dependência de qualquer único ativo ou fator.</li>
            <li>Sustentabilidade do Retorno: Portfólios construídos com base na paridade de risco tendem a ser mais resilientes durante períodos de volatilidade do mercado, mantendo uma performance estável ao longo do tempo.</li>
        </ul>
    </li>
    <li><strong>Minimum Variance:</strong>
        <ul>
            <li>Minimização de Volatilidade: O modelo de Mínima Variância foca em selecionar ativos que juntos formam o portfólio com a menor volatilidade possível, ideal para investidores que buscam um retorno estável com menor risco.</li>
            <li>Consistência de Retorno: Portfólios de mínima variância podem oferecer um retorno mais consistente e previsível, atraindo investidores que preferem evitar grandes flutuações nos valores de seus investimentos.</li>
        </ul>
    </li>
</ol>
