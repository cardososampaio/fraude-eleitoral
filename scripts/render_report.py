"""Render the reviewed, self-contained HTML report from reviewed_snapshot.json."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "data" / "final_snapshot.json"
OUTPUT = ROOT / "report" / "index.html"
data = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
assert data["funnel"]["screened"] == 880
assert data["funnel"]["included"] == 727
assert data["scale"]["claimEntries"] == 1019
assert data["scale"]["allegationEntries"] == 874
assert data["scale"]["allegationPublications"] == 571
assert data["scale"]["pollClaims"] == 5
assert data["scale"]["pollPublications"] == 4

embedded = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
embedded = embedded.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")

document = r'''<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#f4f1e9">
  <meta name="description" content="Relatório interativo da cobertura noticiosa sobre fraude eleitoral no Brasil: acusações específicas, alvos, dinheiro e redes sociais em 727 textos tratados.">
  <title>A marca das 17h aparece em 119 enunciados codificados</title>
  <style>
    :root {
      color-scheme: light;
      --paper: #f4f1e9;
      --paper-deep: #e9e5db;
      --card: #fffdf8;
      --ink: #202620;
      --muted: #596258;
      --line: #d3cec1;
      --line-dark: #aaa596;
      --rust: #a6452b;
      --rust-pale: #f2e1d8;
      --teal: #286e65;
      --teal-pale: #dce9e3;
      --blue: #546a85;
      --gold: #8c7044;
      --serif: Georgia, "Iowan Old Style", "Palatino Linotype", "Book Antiqua", serif;
      --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
      --width: 1180px;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; background: var(--paper); }
    body { margin: 0; background: var(--paper); color: var(--ink); font: 16px/1.58 var(--sans); }
    a { color: var(--teal); text-decoration-thickness: 1px; text-underline-offset: .18em; }
    a:hover { color: var(--rust); }
    :focus-visible { outline: 3px solid var(--rust); outline-offset: 3px; border-radius: 3px; }
    .progress { position: fixed; z-index: 10; inset: 0 auto auto 0; height: 4px; width: 0; background: var(--rust); }
    .masthead { display:flex; justify-content:space-between; align-items:center; max-width:var(--width); margin:auto; padding:17px 28px; border-bottom:1px solid var(--line-dark); color:var(--muted); font-size:10px; font-weight:800; letter-spacing:.13em; text-transform:uppercase; }
    .masthead strong { color:var(--ink); font-size:12px; letter-spacing:.06em; }
    .hero { max-width:var(--width); margin:auto; padding:clamp(48px,8vw,96px) 28px 42px; }
    .eyebrow,.kicker { margin:0 0 10px; color:var(--rust); font-size:11px; font-weight:800; letter-spacing:.14em; text-transform:uppercase; }
    h1,h2,h3,p { margin-top:0; }
    h1 { max-width:1020px; margin-bottom:18px; font:500 clamp(42px,7.7vw,86px)/.98 var(--serif); letter-spacing:-.05em; text-wrap:balance; }
    .deck { max-width:830px; margin:0; color:var(--muted); font:400 clamp(19px,2.5vw,26px)/1.45 var(--serif); text-wrap:pretty; }
    .byline { display:flex; flex-wrap:wrap; gap:8px 20px; margin-top:24px; color:var(--muted); font-size:11px; font-weight:700; letter-spacing:.04em; }
    .byline span + span::before { content:"•"; margin-right:20px; color:var(--rust); }
    .summary { max-width:var(--width); margin:0 auto; padding:26px 28px 38px; border-top:1px solid var(--line-dark); border-bottom:1px solid var(--line-dark); }
    .summary h2 { margin:0 0 17px; font:500 30px/1.05 var(--serif); letter-spacing:-.025em; }
    .summary-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:12px 32px; }
    .summary-item { margin:0; color:var(--muted); font-size:14px; line-height:1.62; }
    .summary-item strong { color:var(--ink); }
    .nav { position:sticky; z-index:5; top:0; display:flex; justify-content:center; gap:3px; overflow-x:auto; padding:9px 12px; border-bottom:1px solid var(--line); background:rgb(244 241 233 / 95%); backdrop-filter:blur(10px); scrollbar-width:thin; }
    .nav a { flex:0 0 auto; padding:7px 10px; border-radius:999px; color:var(--muted); font-size:10px; font-weight:800; text-decoration:none; white-space:nowrap; }
    .nav a:hover,.nav a:focus-visible { background:var(--paper-deep); color:var(--ink); }
    main { max-width:var(--width); margin:0 auto; }
    .section { padding:clamp(44px,6vw,74px) 28px; border-bottom:1px solid var(--line); scroll-margin-top:58px; }
    .section.tinted { background:var(--paper-deep); }
    .section-head { display:grid; grid-template-columns:56px minmax(0,1fr); gap:16px; max-width:950px; margin-bottom:25px; }
    .section-number { color:var(--rust); font:500 30px/1 var(--serif); font-variant-numeric:tabular-nums; }
    .section h2 { max-width:860px; margin:0 0 12px; font:500 clamp(31px,4.7vw,50px)/1.04 var(--serif); letter-spacing:-.035em; text-wrap:balance; }
    .intro { max-width:850px; margin:0; color:var(--muted); font-size:15px; line-height:1.7; }
    .intro strong { color:var(--ink); }
    .chart-card { max-width:1050px; margin:24px 0 0; padding:22px 23px 18px; border:1px solid var(--line); background:var(--card); }
    .chart-head { display:flex; justify-content:space-between; align-items:baseline; flex-wrap:wrap; gap:10px 18px; margin-bottom:15px; }
    .chart-head h3 { margin:0; font-size:13px; font-weight:800; letter-spacing:-.01em; }
    .switch { display:inline-flex; gap:3px; padding:3px; border:1px solid var(--line); border-radius:999px; background:var(--paper); }
    .switch button { min-height:29px; padding:5px 11px; border:0; border-radius:999px; background:transparent; color:var(--muted); font:700 10px var(--sans); cursor:pointer; }
    .switch button[aria-pressed="true"] { background:var(--ink); color:#fff; }
    .bar-list { display:grid; gap:4px; }
    .bar-row { display:grid; width:100%; grid-template-columns:minmax(170px,300px) minmax(70px,1fr) 85px; align-items:center; gap:12px; padding:7px 8px; border:0; border-radius:4px; background:transparent; color:var(--ink); text-align:left; font:inherit; }
    button.bar-row { cursor:pointer; }
    .bar-row:hover,button.bar-row[aria-pressed="true"] { background:#f2eee5; }
    .bar-label { color:var(--muted); font-size:11px; line-height:1.25; overflow-wrap:anywhere; }
    .bar-track { height:11px; overflow:hidden; background:#e8e4da; }
    .bar-fill { display:block; height:100%; min-width:2px; width:var(--w); background:var(--teal); transition:width .4s ease; }
    .bar-row.accent .bar-fill { background:var(--rust); }
    .bar-value { color:var(--ink); font-size:11px; font-weight:800; text-align:right; font-variant-numeric:tabular-nums; white-space:nowrap; }
    .chart-note { max-width:900px; margin:15px 0 0; color:var(--muted); font-size:11px; line-height:1.55; }
    .two-col { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:16px; align-items:start; max-width:1050px; margin-top:20px; }
    .two-col .chart-card { margin:0; }
    .note { max-width:1050px; margin:20px 0 0; padding:17px 20px; border-left:3px solid var(--teal); background:var(--teal-pale); color:#294940; font-size:13px; line-height:1.65; }
    .note strong { color:#172d27; }
    .warning { border-left-color:var(--rust); background:var(--rust-pale); color:#593d32; }
    .cases-title { max-width:1050px; margin:27px 0 10px; font-size:13px; font-weight:800; }
    .case-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:12px; max-width:1050px; }
    .case { padding:16px 17px 18px; border:1px solid var(--line-dark); border-top:3px solid var(--rust); background:var(--card); }
    .case-meta { display:flex; flex-wrap:wrap; gap:5px 10px; margin-bottom:7px; color:var(--muted); font-size:9px; font-weight:800; letter-spacing:.07em; text-transform:uppercase; }
    .case h3 { margin:0 0 7px; font:500 20px/1.2 var(--serif); }
    .case h3 a { color:var(--ink); text-decoration-color:var(--rust); }
    .case p { margin:0 0 9px; font-size:12px; line-height:1.52; }
    .case .target { color:var(--muted); font-size:10px; }
    .case .treatment { color:var(--muted); font-size:10px; }
    .case.empty { grid-column:1/-1; border-top-color:var(--line-dark); color:var(--muted); }
    .target-table-wrap { overflow-x:auto; max-width:1050px; margin-top:19px; border:1px solid var(--line); background:var(--card); }
    table { width:100%; border-collapse:collapse; }
    th,td { padding:10px 12px; border-bottom:1px solid var(--line); text-align:left; vertical-align:top; font-size:11px; }
    th { color:var(--muted); background:#f7f4ec; font-size:9px; font-weight:800; letter-spacing:.08em; text-transform:uppercase; }
    td.num,th.num { text-align:right; font-variant-numeric:tabular-nums; white-space:nowrap; }
    .explorer { max-width:1120px; }
    .filters { display:grid; grid-template-columns:minmax(210px,1.5fr) minmax(165px,1fr) minmax(165px,1fr) minmax(150px,.8fr); gap:10px; align-items:end; margin:21px 0 12px; }
    .field { display:grid; gap:5px; }
    .field label { color:var(--muted); font-size:10px; font-weight:800; }
    .field input,.field select { width:100%; min-height:40px; padding:8px 10px; border:1px solid var(--line-dark); border-radius:3px; background:var(--card); color:var(--ink); font:12px var(--sans); }
    .explorer-actions { display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px; }
    .button { min-height:37px; padding:8px 13px; border:1px solid var(--ink); border-radius:3px; background:var(--ink); color:white; font:750 11px var(--sans); cursor:pointer; }
    .button.secondary { background:transparent; color:var(--ink); }
    .results-label { color:var(--muted); font-size:11px; }
    .table-wrap { overflow:auto; max-height:720px; border:1px solid var(--line-dark); background:var(--card); }
    .claim-table { min-width:1000px; }
    .claim-table th { position:sticky; top:0; z-index:1; }
    .claim-table td { font-size:11px; line-height:1.45; }
    .claim-table .proposition { min-width:340px; }
    .claim-table .source-col { min-width:190px; }
    .claim-table details { margin-top:6px; color:var(--muted); font-size:10px; }
    .claim-table summary { cursor:pointer; color:var(--teal); }
    .tag-pill { display:inline-block; margin:2px 2px 2px 0; padding:2px 6px; border-radius:999px; background:var(--teal-pale); color:#28594f; font-size:9px; white-space:nowrap; }
    .kind-pill { display:inline-block; padding:3px 6px; border-radius:3px; background:var(--rust-pale); color:#693c2d; font-size:9px; font-weight:800; }
    .kind-pill.other { background:#e8e7e0; color:#55584e; }
    .pagination { display:flex; justify-content:center; align-items:center; gap:12px; margin-top:12px; }
    .pagination button { min-height:34px; padding:6px 12px; border:1px solid var(--line-dark); border-radius:3px; background:var(--card); color:var(--ink); font:700 10px var(--sans); cursor:pointer; }
    .pagination button:disabled { opacity:.45; cursor:not-allowed; }
    .method { max-width:1000px; margin:0 auto; padding:clamp(42px,6vw,70px) 28px 34px; border-top:4px solid var(--ink); scroll-margin-top:58px; }
    .method h2 { margin:0 0 17px; font:500 clamp(32px,4.8vw,48px)/1.02 var(--serif); letter-spacing:-.035em; }
    .method h3 { margin:24px 0 7px; font-size:11px; font-weight:850; letter-spacing:.08em; text-transform:uppercase; }
    .method p,.method li { color:var(--muted); font-size:12px; line-height:1.7; }
    .method strong { color:var(--ink); }
    .method ul { padding-left:19px; }
    .sources { display:grid; gap:7px; margin-top:20px; padding-top:15px; border-top:1px solid var(--line); }
    .sources a { font-size:11px; }
    .footer { max-width:var(--width); margin:auto; padding:18px 28px 35px; color:var(--muted); font-size:10px; }
    .footer strong { color:var(--ink); }
    .progress[role="progressbar"] { pointer-events:none; }
    .no-js { padding:20px 28px; color:var(--rust); }
    @media (max-width:780px) {
      .summary-grid,.two-col,.case-grid { grid-template-columns:1fr; }
      .filters { grid-template-columns:repeat(2,minmax(0,1fr)); }
      .section-head { grid-template-columns:38px minmax(0,1fr); gap:11px; }
    }
    @media (max-width:560px) {
      .masthead,.hero,.summary,.section,.method,.footer { padding-left:17px; padding-right:17px; }
      .masthead span { display:none; }
      .hero { padding-top:45px; }
      .byline { display:grid; gap:5px; }
      .byline span + span::before { content:""; margin:0; }
      .summary h2 { font-size:26px; }
      .chart-card { padding:15px 10px; }
      .bar-row { grid-template-columns:minmax(105px,1.15fr) minmax(55px,1fr) 58px; gap:7px; padding:7px 3px; }
      .bar-label,.bar-value { font-size:10px; }
      .filters { grid-template-columns:1fr; }
      th,td { padding:8px; }
    }
    @media (prefers-reduced-motion:reduce) {
      html { scroll-behavior:auto; }
      *,*::before,*::after { scroll-behavior:auto!important; transition-duration:.01ms!important; animation-duration:.01ms!important; }
    }
  </style>
</head>
<body>
  <div class="progress" id="progress" role="progressbar" aria-label="Progresso da leitura" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"></div>
  <header class="masthead"><strong>Observatório da cobertura eleitoral</strong><span>Brasil · 2026 · análise de conteúdo</span></header>
  <header class="hero">
    <p class="eyebrow">Fraude eleitoral nas notícias</p>
    <h1>A marca das 17h aparece em 119 enunciados codificados</h1>
    <p class="deck">A leitura específica dos enunciados mostra o que os rótulos amplos escondiam: alegações e irregularidades sobre prorrogação, pausas no painel, mesários, modelos de urna, alvos institucionais, dinheiro e operações digitais.</p>
    <div class="byline"><span>Publicações: 15 ago–9 nov 2026</span><span>Base final: 727 textos tratados</span><span>Atualização do relatório: 15 nov 2026</span></div>
  </header>
  <section class="summary" aria-labelledby="summary-title">
    <h2 id="summary-title">Resumo executivo</h2>
    <div class="summary-grid">
      <p class="summary-item"><strong>A marca das 17h é a menção específica mais recorrente.</strong> São 119 entradas em 105 matérias, no conjunto codificado como suspeita, afirmação de fraude ou irregularidade. O marcador identifica enunciados que citam 17h, votos após o horário, prorrogação ou urnas já encerradas; não decide, sozinho, que houve fraude. Pausas e painéis aparecem em 42 entradas; mesários, biometria ou voto por terceiros, em 41.</p>
      <p class="summary-item"><strong>Alvos e acusadores são identificáveis.</strong> O papel de acusador foi atribuído a Flávio Bolsonaro em 179 matérias e a Donald Trump em 62. Entre os atores marcados como acusados, aparecem Podemos em 32 matérias, TSE e Cristiano Zanin em 31 cada, Lula em 24 e a chapa Lula–Alckmin em 14.</p>
      <p class="summary-item"><strong>“Financiamento” reúne mecanismos diferentes.</strong> O código amplo aparece em 109 entradas. Duas formulações sobre possível dinheiro estrangeiro para campanhas aparecem em três publicações; uma foi republicada. Nenhuma registra transferência concluída.</p>
      <p class="summary-item"><strong>Redes sociais aparecem explicitamente.</strong> 52 entradas em 45 matérias mencionam redes sociais de forma genérica; X/Twitter aparece em 22 entradas, WhatsApp em 19 e Instagram em 15. Menção a uma plataforma não significa que ela seja acusada de manipular a eleição.</p>
    </div>
  </section>
  <nav class="nav" aria-label="Navegação do relatório">
    <a href="#urnas">Urnas e apuração</a><a href="#instituicoes">TSE</a><a href="#atores">Quem acusa</a><a href="#dinheiro">Dinheiro</a><a href="#redes">Redes sociais</a><a href="#explorador">Todas as entradas</a><a href="#metodo">Método</a>
  </nav>
  <main>
    <section class="section" id="urnas" aria-labelledby="urnas-title">
      <div class="section-head"><span class="section-number">01</span><div><p class="kicker">Mecanismos alegados</p><h2 id="urnas-title">“Fraude nas urnas” reúne acusações sobre mecanismos distintos.</h2><p class="intro">As proposições mencionam ligação com a Smartmatic, modelos e códigos, invasões em testes, teclas ou lacres, voto por terceiros, pausas de divulgação e argumentos sobre padrões de votos. Cada barra conta entradas codificadas e matérias; os grupos se sobrepõem.</p></div></div>
      <div class="chart-card">
        <div class="chart-head"><h3>Entradas de alegação por mecanismo explícito</h3><div class="switch" role="group" aria-label="Unidade do gráfico de mecanismos"><button type="button" data-chart-metric="claims" aria-pressed="true">Entradas</button><button type="button" data-chart-metric="publications" aria-pressed="false">Matérias</button></div></div>
        <div class="bar-list" id="vote-tags" role="list" aria-label="Subtemas de urnas e apuração"></div>
        <p class="chart-note">Um clique filtra o explorador para as entradas da categoria. “Entradas” são unidades de alegação do protocolo; “matérias” são publicações distintas, não acontecimentos únicos. A mesma narrativa pode aparecer em vários veículos.</p>
      </div>
      <h3 class="cases-title" id="vote-cases-title">Casos que dão concretude às categorias</h3>
      <div class="case-grid" id="vote-cases" aria-live="polite"></div>
    </section>

    <section class="section tinted" id="instituicoes" aria-labelledby="tse-title">
      <div class="section-head"><span class="section-number">02</span><div><p class="kicker">O Tribunal Superior Eleitoral</p><h2 id="tse-title">O TSE aparece em 90 enunciados como alvo, mas o papel de “acusado” é mais restrito.</h2><p class="intro">O campo <em>alvo</em> nomeia o objeto da proposição; não equivale automaticamente a uma acusação endossada pelo veículo. Em 90 entradas de alegação, o campo alvo menciona TSE/Tribunal Superior Eleitoral; em 31 matérias, a tabela de atores registra o TSE explicitamente no papel de acusado.</p></div></div>
      <div class="chart-card">
        <div class="chart-head"><h3>O que se alega contra ou sobre o TSE</h3><div class="switch" role="group" aria-label="Unidade do gráfico do TSE"><button type="button" data-chart-metric="claims" aria-pressed="true">Entradas</button><button type="button" data-chart-metric="publications" aria-pressed="false">Matérias</button></div></div>
        <div class="bar-list" id="tse-tags" role="list" aria-label="Subtemas de acusações que citam o TSE"></div>
        <p class="chart-note">Os subtemas abaixo são multilabel e cobrem somente proposições com marcador textual explícito: manipular sistemas/resultados; retirar ou impedir fiscais; questionar decisões, horários ou isonomia. Não somar as barras.</p>
      </div>
      <div class="note"><strong>Exemplos que o rótulo “integridade eleitoral” não mostrava:</strong> matérias registram alegações de que servidores poderiam alterar sistemas e resultados; de que fiscais do PL foram retirados da sala-cofre; e de que a prorrogação do horário teria quebrado a isonomia. A listagem pesquisável permite abrir a formulação, o tratamento e a fonte de cada entrada.</div>
    </section>

    <section class="section" id="atores" aria-labelledby="actors-title">
      <div class="section-head"><span class="section-number">03</span><div><p class="kicker">Fontes e alvos nomeados</p><h2 id="actors-title">Flávio Bolsonaro aparece sobretudo como acusador; Lula, Podemos e o TSE como alvos.</h2><p class="intro">As contagens abaixo vêm dos papéis atribuídos a atores nas matérias. Um texto pode registrar vários acusadores e alvos, e os papéis não são sinônimo de culpa nem de validação jornalística.</p></div></div>
      <div class="two-col">
        <div class="chart-card"><div class="chart-head"><h3>Fontes classificadas como acusadoras</h3></div><div class="bar-list" id="accusers" role="list" aria-label="Atores no papel de acusador"></div><p class="chart-note">Número de matérias em que o ator recebeu o papel “acusador”. Siglas equivalentes foram agrupadas apenas em aliases documentados, como MPE/Ministério Público Eleitoral.</p></div>
        <div class="chart-card"><div class="chart-head"><h3>Atores classificados como acusados</h3></div><div class="bar-list" id="accused" role="list" aria-label="Atores no papel de acusado"></div><p class="chart-note">Número de matérias com o papel “acusado”. O agrupamento não é uma contagem de processos, decisões ou acontecimentos independentes.</p></div>
      </div>
      <div class="chart-card">
        <div class="chart-head"><h3>Alvos explícitos nas proposições de alegação</h3><div class="switch" role="group" aria-label="Unidade da tabela de alvos"><button type="button" data-target-metric="claims" aria-pressed="true">Entradas</button><button type="button" data-target-metric="publications" aria-pressed="false">Matérias</button></div></div>
        <div class="target-table-wrap"><table><thead><tr><th>Alvo nomeado no campo</th><th>Tipo</th><th class="num">Entradas</th><th class="num">Matérias</th></tr></thead><tbody id="target-rows"></tbody></table></div>
        <p class="chart-note">Os grupos se sobrepõem: uma proposição pode citar mais de um alvo. “Bolsonaro (sobrenome no alvo)” conta qualquer ocorrência do sobrenome e pode incluir Flávio ou Jair; não é uma pessoa adicional. O campo alvo pode nomear alguém sem que a tabela de atores registre esse ator no papel de “acusado”, por exemplo quando a matéria relata e contesta a proposição. Entre as entradas com alvo vazio, o protocolo preserva a ausência em vez de inferir um nome.</p>
      </div>
      <div class="chart-card"><div class="chart-head"><h3>O que se alegou sobre candidaturas e cotas</h3></div><div class="bar-list" id="candidate-tags" role="list" aria-label="Subtemas de candidaturas e cotas"></div><p class="chart-note">A regra identifica enunciados sobre candidaturas fictícias ou de fachada para cumprir a cota de gênero. Ela não atribui desvio de recursos quando a proposição não o menciona. Clique para abrir as entradas e as matérias correspondentes.</p></div>
    </section>

    <section class="section tinted" id="dinheiro" aria-labelledby="finance-title">
      <div class="section-head"><span class="section-number">04</span><div><p class="kicker">Financiamento, poder e campanhas</p><h2 id="finance-title">A categoria financeira mistura dinheiro, uso do Estado e propaganda.</h2><p class="intro">O código amplo <code>campanha_financiamento</code> foi aplicado a 109 entradas em 84 matérias. A recodificação distingue uso da máquina pública, abuso de poder político/econômico, compra de votos, prestação de contas, propaganda e possíveis recursos estrangeiros. Os subtemas se sobrepõem; o rótulo não confirma uma irregularidade.</p></div></div>
      <div class="chart-card">
        <div class="chart-head"><h3>Mecanismos específicos em alegações financeiras</h3><div class="switch" role="group" aria-label="Unidade do gráfico de dinheiro"><button type="button" data-chart-metric="claims" aria-pressed="true">Entradas</button><button type="button" data-chart-metric="publications" aria-pressed="false">Matérias</button></div></div>
        <div class="bar-list" id="finance-tags" role="list" aria-label="Subtemas financeiros"></div>
        <p class="chart-note" id="finance-coverage-note"></p>
      </div>
      <h3 class="cases-title">Outros mecanismos financeiros descritos nas matérias</h3>
      <div class="case-grid" id="finance-cases" aria-label="Exemplos de acusações financeiras"></div>
      <div class="note warning"><strong>Houve acusação de dinheiro vindo do exterior?</strong> Duas formulações aparecem em três publicações. Uma relata a possibilidade de interferência dos EUA, inclusive financiamento de campanha, em relatório da Abin; ela aparece em The Conversation e em uma republicação do R7. A outra pergunta se consultorias de Fernando Cerimedo poderiam ter sido pagas por um fundo nos EUA. As duas são hipóteses ou perguntas; nenhuma relata uma transferência concluída.</div>
      <div class="case-grid" id="foreign-cases" aria-label="Casos sobre possíveis recursos estrangeiros e projeto internacional"></div>
      <div class="note"><strong>Fluxos diferentes não devem ser confundidos:</strong> o projeto norte-americano citado em uma matéria previa recursos para grupos críticos ao STF, não doação direta a campanhas; outra reportagem relata R$ 600 mil pagos pela campanha de Flávio Bolsonaro a uma empresa norte-americana de serviços de segurança da informação. Esse último é um pagamento da campanha a um fornecedor estrangeiro, não dinheiro estrangeiro entrando na campanha. As matérias também registram a declaração de R$ 1 milhão na prestação parcial e respostas da campanha e da empresa. As referências a ajuda financeira para a Argentina e a operações em Honduras são comparações internacionais, não valores destinados a campanhas brasileiras.</div>
    </section>

    <section class="section" id="redes" aria-labelledby="social-title">
      <div class="section-head"><span class="section-number">05</span><div><p class="kicker">Plataformas e circulação</p><h2 id="social-title">As redes aparecem como canal de circulação, ferramenta de campanha e alvo de acusações.</h2><p class="intro">Os registros citam publicações virais e grupos, anúncios, influenciadores, bots e conteúdo de IA. Algumas proposições acusam plataformas de restringir conteúdo ou favorecer candidaturas; outras apenas informam onde a alegação circulou.</p></div></div>
      <div class="two-col">
        <div class="chart-card"><div class="chart-head"><h3>Funções digitais explicitamente descritas</h3><div class="switch" role="group" aria-label="Unidade do gráfico digital"><button type="button" data-chart-metric="claims" aria-pressed="true">Entradas</button><button type="button" data-chart-metric="publications" aria-pressed="false">Matérias</button></div></div><div class="bar-list" id="digital-tags" role="list" aria-label="Funções de redes e plataformas"></div></div>
        <div class="chart-card"><div class="chart-head"><h3>Plataformas nomeadas nas evidências codificadas</h3></div><div class="bar-list" id="platforms" role="list" aria-label="Menções a plataformas nas alegações"></div><p class="chart-note">Cada valor mostra entradas / matérias. Busca literal no enunciado, alvo e trecho de evidência de cada alegação; plataformas podem se sobrepor. A contagem não cobre toda menção no texto integral.</p></div>
      </div>
      <div class="note"><strong>O que isso sustenta:</strong> redes sociais são parte explícita das alegações e da cobertura. O material também descreve anúncios que simulavam comunicações do TSE, questionamentos sobre resultados de busca, restrições de conteúdo e contas coordenadas. A presença de “Meta”, “WhatsApp” ou “X” na matéria, isoladamente, não é evidência de fraude ou de responsabilidade da empresa.</div>
    </section>

    <section class="section tinted" id="explorador" aria-labelledby="explorer-title">
      <div class="section-head"><span class="section-number">06</span><div><p class="kicker">Consulta auditável</p><h2 id="explorer-title">Explore as 1.019 entradas, incluindo alvo, fonte e tratamento.</h2><p class="intro">A tabela preserva enunciados, objetos originais e subtemas específicos. Use o filtro de alvo para separar “Podemos” como partido de ocorrências da palavra em manchetes; pesquise expressões como “dinheiro estrangeiro”, “mesários” ou “WhatsApp” e abra a matéria de origem.</p></div></div>
      <div class="explorer">
        <div class="filters">
          <div class="field"><label for="search">Buscar na proposição, alvo, fonte ou matéria</label><input id="search" type="search" placeholder="Ex.: pausa no painel, compra de votos, TSE"></div>
          <div class="field"><label for="kind-filter">Tipo de enunciado</label><select id="kind-filter"><option value="all">Todas as 1.019 entradas</option><option value="allegation">Suspeita, fraude ou irregularidade</option><option value="other">Negação ou integridade preventiva</option></select></div>
          <div class="field"><label for="target-filter">Alvo nomeado (alegações)</label><select id="target-filter"><option value="all">Todos os alvos</option></select></div>
          <div class="field"><label for="object-filter">Objeto do protocolo original</label><select id="object-filter"><option value="all">Todos os objetos</option></select></div>
          <div class="field"><label for="tag-filter">Subtema específico</label><select id="tag-filter"><option value="all">Todos os subtemas</option></select></div>
        </div>
        <div class="explorer-actions"><span class="results-label" id="result-count" aria-live="polite"></span><button class="button" id="download-csv" type="button">Baixar CSV com todas as entradas</button></div>
        <div class="table-wrap"><table class="claim-table"><thead><tr><th>Data</th><th>Matéria</th><th>Enunciado e evidência</th><th>Fonte da alegação</th><th>Alvo</th><th>Modalidade / tratamento</th><th>Subtemas</th></tr></thead><tbody id="claim-rows"></tbody></table></div>
        <div class="pagination"><button id="previous-page" type="button">Anterior</button><span class="results-label" id="page-label"></span><button id="next-page" type="button">Próxima</button></div>
      </div>
    </section>
  </main>
  <section class="method" id="metodo" aria-labelledby="method-title">
    <p class="eyebrow">Como ler estes números</p><h2 id="method-title">Corpus final, unidades e limites da classificação</h2>
    <h3>Uma base final e uma etapa de filtragem</h3>
    <p>O inventário reuniu <strong>880 registros</strong>. Depois da conferência de texto integral, pertinência ao tema e duplicidade/versões, <strong>727 textos</strong> formam o corpus final apresentado aqui; 153 ficaram fora da análise de conteúdo. O relatório não separa resultados por blocos anteriores de coleta.</p>
    <h3>O que cada número conta</h3>
    <p>As tabelas registram <strong>1.019 entradas de proposições em 634 matérias</strong>. Destas, 874 entradas em 571 matérias são classificadas como suspeita, afirmação de fraude ou irregularidade. As outras 145 são negações de fraude ou afirmações preventivas de integridade. Em 73 entradas, o campo de alvo está vazio; o relatório não completa esse dado por inferência.</p>
    <h3>Recodificação específica e reprodução</h3>
    <p>Os códigos amplos do manual foram preservados. Para responder às perguntas sobre urnas, TSE, financiamento e redes, o script aplica uma recodificação textual adicional ao enunciado e ao alvo da alegação, com regras explícitas de busca descritas em <code>relatorio_interativo/gerar_snapshot.py</code>. Os subtemas são multilabel: uma entrada pode acionar mais de uma regra. As contagens medem formulações noticiadas e sua presença em matérias; não são acontecimentos independentes nem prova de que o fato ocorreu.</p>
    <p>O campo <em>tratamento</em> registra como o texto apresenta, contesta ou atribui a proposição. A tabela de atores registra papéis como acusador e acusado; os nomes foram agrupados somente em aliases evidentes (por exemplo, TSE/Tribunal Superior Eleitoral, PL/Partido Liberal e MPE/Ministério Público Eleitoral). Um mesmo ator pode aparecer em vários textos sobre a mesma narrativa.</p>
    <h3>Limites de confiabilidade</h3>
    <p>As classificações de conteúdo foram produzidas com assistência de IA e não tiveram validação humana independente, dupla codificação ou cálculo de concordância entre codificadores. A recodificação adicional é lexical e reprodutível, mas pode perder paráfrases ou sinalizar usos ambíguos; os enunciados e trechos ligados às fontes permitem revisar cada caso. O corpus não é amostra aleatória da imprensa brasileira e não estima prevalência nacional de cobertura. O rótulo não confirma a acusação nem mede seu alcance sobre o público.</p>
    <div class="sources" aria-label="Fontes e documentação">
      <a href="../classificacao/MANUAL.md">Manual de classificação do projeto</a>
      <a href="../classificacao/integral/alegacoes.csv">Tabela de alegações e evidências do corpus final</a>
      <a href="../classificacao/integral/atores.csv">Tabela de atores e papéis</a>
      <a href="../classificacao/ampliacao/alegacoes_639.csv">Registros de alegações tratados na etapa complementar</a>
      <a href="https://periodicos.fgv.br/cgpc/announcement/view/532" target="_blank" rel="noopener noreferrer">FGV — contexto do projeto sobre fraude eleitoral</a>
      <a href="https://osf.io/gqeh2/overview" target="_blank" rel="noopener noreferrer">OSF — projeto indicado pela equipe</a>
    </div>
  </section>
  <footer class="footer"><strong>Nota de leitura</strong> · As frequências descrevem alegações e tratamentos nas matérias recuperadas e classificadas até 9 de novembro de 2026; não representam a totalidade do noticiário nem comprovam as alegações.</footer>
  <noscript><p class="no-js">Este relatório interativo precisa de JavaScript habilitado. Todos os dados usados estão embutidos neste arquivo.</p></noscript>
  <script id="report-data" type="application/json">__DATA__</script>
  <script>
    (() => {
      const data = JSON.parse(document.getElementById("report-data").textContent);
      const nf = new Intl.NumberFormat("pt-BR");
      const esc = value => String(value ?? "").replace(/[&<>"']/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[char]));
      const safeUrl = value => /^https?:\/\//i.test(String(value || "")) ? String(value) : "#";
      const tagByCode = new Map(data.tagDefinitions.map(tag => [tag.code, tag]));
      const objectLabels = {
        votacao:"Votação", apuracao_totalizacao:"Apuração e totalização", divulgacao:"Divulgação de resultados",
        integridade_geral:"Integridade geral", campanha_financiamento:"Campanha e financiamento",
        candidaturas_filiacao_cotas:"Candidaturas, filiação e cotas", cadastro_identificacao:"Cadastro e identificação",
        pesquisas_eleitorais:"Pesquisas de opinião", outro:"Outro objeto"
      };
      const metricNames = {claims:"entradas",publications:"matérias"};
      const tagsFor = domain => data.tags.filter(tag => domain.includes(tag.domain));
      let metricMode = "claims";
      let selectedTag = "";

      function renderTagChart(id, rows) {
        const node = document.getElementById(id);
        const sorted = [...rows].sort((a,b) => (b[metricMode]-a[metricMode]) || a.label.localeCompare(b.label,"pt-BR"));
        const max = Math.max(1, ...sorted.map(row => row[metricMode]));
        node.innerHTML = sorted.map(row => {
          const value = row[metricMode];
          const percent = value ? Math.max(1, value / max * 100) : 0;
          const pressed = selectedTag === row.code;
          const title = `${row.label}: ${nf.format(value)} ${metricNames[metricMode]}. ${row.definition}`;
          return `<button class="bar-row ${row.domain === "Financiamento e poder econômico" ? "accent" : ""}" type="button" data-tag="${esc(row.code)}" aria-pressed="${pressed}" aria-label="${esc(title)}"><span class="bar-label">${esc(row.label)}</span><span class="bar-track" aria-hidden="true"><span class="bar-fill" style="--w:${percent.toFixed(2)}%"></span></span><span class="bar-value">${nf.format(value)}</span></button>`;
        }).join("") || `<p class="results-label">Não há entradas nesta categoria.</p>`;
        node.querySelectorAll("[data-tag]").forEach(button => button.addEventListener("click", () => {
          selectedTag = selectedTag === button.dataset.tag ? "" : button.dataset.tag;
          renderAllTagCharts();
          const select = document.getElementById("tag-filter");
          select.value = selectedTag || "all";
          renderExplorer();
        }));
      }
      function renderAllTagCharts() {
        renderTagChart("vote-tags", tagsFor(["Urnas e votação","Apuração e divulgação"]));
        renderTagChart("tse-tags", tagsFor(["TSE e instituições"]));
        renderTagChart("finance-tags", tagsFor(["Financiamento e poder econômico"]));
        renderTagChart("candidate-tags", tagsFor(["Candidaturas e cotas"]));
        renderTagChart("digital-tags", tagsFor(["Redes e operações digitais"]));
      }
      document.querySelectorAll("[data-chart-metric]").forEach(button => button.addEventListener("click", () => {
        metricMode = button.dataset.chartMetric;
        document.querySelectorAll("[data-chart-metric]").forEach(item => item.setAttribute("aria-pressed", String(item === button)));
        renderAllTagCharts();
      }));
      renderAllTagCharts();
      const financeAll=data.claims.filter(row=>row.objects.includes("campanha_financiamento"));
      const financeAllegations=financeAll.filter(row=>row.isAllegation);
      const financeCodes=new Set(data.tagDefinitions.filter(tag=>tag.domain==="Financiamento e poder econômico").map(tag=>tag.code));
      const financeTagged=financeAllegations.filter(row=>row.tags.some(code=>financeCodes.has(code)));
      document.getElementById("finance-coverage-note").textContent=`O objeto amplo reúne ${nf.format(financeAll.length)} entradas em ${nf.format(new Set(financeAll.map(row=>row.publicationId)).size)} matérias; ${nf.format(financeAllegations.length)} estão no conjunto de suspeitas, afirmações de fraude ou irregularidades. As regras específicas associam ${nf.format(financeTagged.length)} entradas distintas a pelo menos um subtema deste objeto; ${nf.format(financeAllegations.length-financeTagged.length)} não acionam nenhum desses marcadores. Os subtemas se sobrepõem e identificam palavras ou expressões das proposições, não comprovam gasto ilícito.`;

      function renderActorChart(id, rows) {
        const node = document.getElementById(id);
        const max = Math.max(1, ...rows.map(row => row.publications));
        node.innerHTML = rows.map(row => {
          const width = Math.max(1,row.publications/max*100);
          const label = `${row.name}: ${nf.format(row.publications)} matérias`;
          return `<div class="bar-row" role="listitem" aria-label="${esc(label)}"><span class="bar-label">${esc(row.name)}</span><span class="bar-track" aria-hidden="true"><span class="bar-fill" style="--w:${width.toFixed(2)}%"></span></span><span class="bar-value">${nf.format(row.publications)}</span></div>`;
        }).join("");
      }
      renderActorChart("accusers",data.accusers.slice(0,10));
      renderActorChart("accused",data.accused.slice(0,10));

      let targetMetric = "claims";
      function renderTargets() {
        const rows = [...data.targets].sort((a,b) => (b[targetMetric]-a[targetMetric]) || a.name.localeCompare(b.name,"pt-BR"));
        document.getElementById("target-rows").innerHTML = rows.map(row => `<tr><td>${esc(row.name)}</td><td>${esc(row.type)}</td><td class="num">${nf.format(row.claims)}</td><td class="num">${nf.format(row.publications)}</td></tr>`).join("");
        document.querySelectorAll("[data-target-metric]").forEach(button => button.setAttribute("aria-pressed",String(button.dataset.targetMetric===targetMetric)));
      }
      document.querySelectorAll("[data-target-metric]").forEach(button => button.addEventListener("click",()=>{targetMetric=button.dataset.targetMetric;renderTargets();}));
      renderTargets();

      const preferredExamples = new Set(["DOC-002-a01","DOC-065-a01","DOC-082-a01","DOC-091-a01","DOC-093-a02","DOC-011-a02","DOC-060-a01","DOC-084-a03","ADD-344-a01","ADD-365-a01","DOC-090-a04","DOC-136-a01","DOC-084-a09","DOC-084-a10","DOC-172-a01","DOC-188-a05","ADD-123-a01"]);
      function caseCard(row) {
        const tagNames = row.tags.map(code => tagByCode.get(code)?.label).filter(Boolean).slice(0,2);
        return `<article class="case"><div class="case-meta"><span>${esc(row.date)}</span><span>${esc(row.outlet)}</span><span>${esc(row.modality.replaceAll("_"," "))}</span></div><h3><a href="${esc(safeUrl(row.url))}" target="_blank" rel="noopener noreferrer">${esc(row.title)}</a></h3><p>${esc(row.proposition)}</p><p class="target"><strong>Fonte:</strong> ${esc(row.accuser || "não especificada")} · <strong>Alvo:</strong> ${esc(row.target || "não especificado")}</p><p class="treatment"><strong>Tratamento no corpo:</strong> ${esc(row.bodyTreatment.replaceAll("_"," ") || "não informado")}${tagNames.length ? ` · <strong>Subtema:</strong> ${esc(tagNames.join("; "))}` : ""}</p></article>`;
      }
      function renderExamples(nodeId, predicate, fallbackText, max=4) {
        let rows = data.claims.filter(row => row.isAllegation && predicate(row));
        rows = rows.filter(row => preferredExamples.has(row.id)).concat(rows.filter(row => !preferredExamples.has(row.id)));
        const unique = [];
        const usedPublications = new Set();
        for (const row of rows) {
          if (usedPublications.has(row.publicationId)) continue;
          usedPublications.add(row.publicationId);
          unique.push(row);
          if (unique.length >= max) break;
        }
        document.getElementById(nodeId).innerHTML = unique.length ? unique.map(caseCard).join("") : `<p class="case empty">${esc(fallbackText)}</p>`;
      }
      renderExamples("vote-cases", row => ["urnas_smartmatic_venezuela","urnas_modelo_codigo_chip","urnas_teste_hack_auditoria","urnas_interferencia_fisica","urna_identidade_mesarios","apuracao_painel_pausa","apuracao_horario_17h","apuracao_padrao_estatistico"].some(code => row.tags.includes(code)),"Nenhuma matéria exemplificativa disponível.",4);
      renderExamples("finance-cases", row => ["fin_uso_maquina_beneficios","fin_abuso_poder_politico_economico","fin_compra_votos","fin_contas_recursos_nao_declarados","fin_apoio_privado_servicos","fin_prop_meios_comunicacao"].some(code => row.tags.includes(code)),"Nenhuma matéria exemplificativa disponível.",4);
      renderExamples("foreign-cases", row => ["fin_possivel_dinheiro_estrangeiro_campanha","fin_projeto_estrangeiro_pressao"].some(code => row.tags.includes(code)),"Nenhuma matéria exemplificativa disponível.",5);

      const platformMax = Math.max(1,...data.platforms.map(row=>row.claims));
      document.getElementById("platforms").innerHTML = data.platforms.map(row => {
        const width=Math.max(1,row.claims/platformMax*100);
        const aria=`${row.platform}: ${nf.format(row.claims)} entradas em ${nf.format(row.publications)} matérias`;
        return `<div class="bar-row" role="listitem" aria-label="${esc(aria)}"><span class="bar-label">${esc(row.platform)}</span><span class="bar-track" aria-hidden="true"><span class="bar-fill" style="--w:${width.toFixed(2)}%"></span></span><span class="bar-value">${nf.format(row.claims)} / ${nf.format(row.publications)}</span></div>`;
      }).join("");

      const tagFilter=document.getElementById("tag-filter");
      for(const tag of data.tagDefinitions){const option=document.createElement("option");option.value=tag.code;option.textContent=`${tag.domain} · ${tag.label}`;tagFilter.append(option);}
      const targetFilter=document.getElementById("target-filter");
      for(const target of [...data.targets].sort((a,b)=>a.name.localeCompare(b.name,"pt-BR"))){const option=document.createElement("option");option.value=target.name;option.textContent=`${target.name} · ${nf.format(target.publications)} matérias`;targetFilter.append(option);}
      const objectFilter=document.getElementById("object-filter");
      const allObjects=[...new Set(data.claims.flatMap(row=>row.objects))].sort((a,b)=>(objectLabels[a]||a).localeCompare(objectLabels[b]||b,"pt-BR"));
      for(const object of allObjects){const option=document.createElement("option");option.value=object;option.textContent=objectLabels[object]||object;objectFilter.append(option);}
      const pageSize=20;let page=0;
      const foldText=value=>String(value||"").normalize("NFKD").replace(/[\u0300-\u036f]/g,"").toLowerCase();
      function filteredRows(){
        const query=document.getElementById("search").value.trim().toLocaleLowerCase("pt-BR");
        const kind=document.getElementById("kind-filter").value;
        const object=objectFilter.value;const tag=tagFilter.value;const target=data.targets.find(row=>row.name===targetFilter.value);
        return data.claims.filter(row=>{
          if(kind==="allegation"&&!row.isAllegation)return false;
          if(kind==="other"&&row.isAllegation)return false;
          if(object!=="all"&&!row.objects.includes(object))return false;
          if(tag!=="all"&&!row.tags.includes(tag))return false;
          if(target&&(!row.isAllegation||!new RegExp(target.pattern).test(foldText(row.target))))return false;
          if(query){const hay=[row.id,row.publicationId,row.proposition,row.target,row.accuser,row.outlet,row.title,...row.objects,...row.tags.map(code=>tagByCode.get(code)?.label||""),...row.platforms].join(" ").toLocaleLowerCase("pt-BR");if(!hay.includes(query))return false;}
          return true;
        });
      }
      function renderExplorer(){
        const rows=filteredRows();const maxPage=Math.max(0,Math.ceil(rows.length/pageSize)-1);page=Math.min(page,maxPage);
        const visible=rows.slice(page*pageSize,(page+1)*pageSize);
        document.getElementById("result-count").textContent=`${nf.format(rows.length)} entradas correspondem aos filtros · página ${nf.format(page+1)} de ${nf.format(maxPage+1)}`;
        document.getElementById("page-label").textContent=`${nf.format(page*pageSize+1)}–${nf.format(Math.min((page+1)*pageSize,rows.length))} de ${nf.format(rows.length)}`;
        document.getElementById("previous-page").disabled=page===0;
        document.getElementById("next-page").disabled=page>=maxPage;
        document.getElementById("claim-rows").innerHTML=visible.map(row=>{
          const kind=row.isAllegation?"Alegação":"Negação/prevenção";
          const kindClass=row.isAllegation?"":" other";
          const tags=row.tags.map(code=>tagByCode.get(code)?.label).filter(Boolean);
          const objectText=row.objects.map(code=>objectLabels[code]||code).join("; ");
          const evidence=row.evidence?`<details><summary>Trecho de evidência</summary><span>${esc(row.evidence)}</span></details>`:"";
          const tagPills=tags.length?tags.map(label=>`<span class="tag-pill">${esc(label)}</span>`).join(""):`<span class="results-label">Sem subtema lexical específico</span>`;
          return `<tr><td>${esc(row.date)}</td><td class="source-col"><a href="${esc(safeUrl(row.url))}" target="_blank" rel="noopener noreferrer">${esc(row.title)}</a><br><span class="results-label">${esc(row.outlet)} · ${esc(row.publicationId)}</span></td><td class="proposition"><span class="kind-pill${kindClass}">${kind}</span> ${esc(row.proposition)}${evidence}<br><span class="results-label">Objeto original: ${esc(objectText||"não informado")}</span></td><td>${esc(row.accuser||"não especificada")}</td><td>${esc(row.target||"não especificado")}</td><td>${esc(row.modality.replaceAll("_"," "))}<br><span class="results-label">Corpo: ${esc(row.bodyTreatment.replaceAll("_"," "))}</span></td><td>${tagPills}</td></tr>`;
        }).join("")||`<tr><td colspan="7">Nenhuma entrada corresponde aos filtros.</td></tr>`;
      }
      ["search","kind-filter","target-filter","object-filter","tag-filter"].forEach(id=>document.getElementById(id).addEventListener(id==="search"?"input":"change",()=>{page=0;selectedTag=tagFilter.value==="all"?"":tagFilter.value;renderExplorer();renderAllTagCharts();}));
      document.getElementById("previous-page").addEventListener("click",()=>{page=Math.max(0,page-1);renderExplorer();});
      document.getElementById("next-page").addEventListener("click",()=>{page+=1;renderExplorer();});
      document.getElementById("download-csv").addEventListener("click",()=>{
        const columns=["alegacao_local_id","publicacao_id","data","veiculo","url","proposicao","objetos","modalidade","alegador","alvo","alcance","tratamento_corpo","tratamento_titulo","situacao_relatada","subtemas_especificos","plataformas_mencionadas"];
        const quote=value=>`"${String(value??"").replace(/"/g,'""')}"`;
        const lines=[columns.map(quote).join(","),...data.claims.map(row=>[
          row.id,row.publicationId,row.date,row.outlet,row.url,row.proposition,row.objects.join("; "),row.modality,row.accuser,row.target,row.reach,row.bodyTreatment,row.titleTreatment,row.situation,
          row.tags.map(code=>tagByCode.get(code)?.label||code).join("; "),row.platforms.join("; ")
        ].map(quote).join(","))];
        const blob=new Blob(["\ufeff"+lines.join("\r\n")],{type:"text/csv;charset=utf-8"});
        const link=document.createElement("a");const objectUrl=URL.createObjectURL(blob);link.href=objectUrl;link.download="alegacoes_recodificadas_1019.csv";document.body.append(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(objectUrl),1000);
      });
      renderExplorer();

      const progress=document.getElementById("progress");let frame=0;
      function updateProgress(){cancelAnimationFrame(frame);frame=requestAnimationFrame(()=>{const max=document.documentElement.scrollHeight-innerHeight;const value=max>0?Math.max(0,Math.min(100,scrollY/max*100)):100;progress.style.width=`${value}%`;progress.setAttribute("aria-valuenow",String(Math.round(value)));});}
      addEventListener("scroll",updateProgress,{passive:true});addEventListener("resize",updateProgress,{passive:true});updateProgress();
    })();
  </script>
</body>
</html>'''

OUTPUT.write_text(document.replace("__DATA__", embedded), encoding="utf-8")
print(json.dumps({
    "html": str(OUTPUT), "bytes": OUTPUT.stat().st_size,
    "publications": data["scale"]["finalPublications"],
    "claimEntries": data["scale"]["claimEntries"],
    "allegationEntries": data["scale"]["allegationEntries"],
}, ensure_ascii=False))
