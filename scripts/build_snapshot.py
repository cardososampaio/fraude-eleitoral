"""Build an auditable, fine-grained snapshot from the final classified corpus.

The supplemental tags below are transparent lexical recodes of the existing
claim propositions and targets. A tag marks an explicit textual signal; it is
not an independent judgment that the alleged event occurred.
"""

from __future__ import annotations

import csv
import json
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "final_snapshot.json"
ALLEGATION_MODALITIES = {
    "suspeita", "afirmacao_fraude", "irregularidade_sem_fraude_afirmada"
}
FINAL_EXTENSION_DECISIONS = {
    "incluir_nucleo", "incluir_contexto", "separar_institucional", "versao_mesma_url"
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def fold(value: str | None) -> str:
    decomposed = unicodedata.normalize("NFKD", value or "")
    return "".join(char for char in decomposed if not unicodedata.combining(char)).lower()


def parse_json_list(value: str | None) -> list:
    try:
        parsed = json.loads(value or "[]")
    except (TypeError, json.JSONDecodeError):
        return []
    return parsed if isinstance(parsed, list) else []


def unique_nonempty(values: list[str]) -> list[str]:
    return list(dict.fromkeys(value.strip() for value in values if value and value.strip()))


def article_meta(row: dict[str, str], source: str) -> dict:
    if source == "original":
        return {
            "id": row["id"], "date": row["data_cadastrada"],
            "outlet": row["veiculo"], "title": row["titulo_cadastrado"],
            "url": row["url_cadastrada"], "genre": row.get("genero", ""),
        }
    return {
        "id": row["id"], "date": row["data"], "outlet": row["veiculo"],
        "title": row["titulo"], "url": row["url"], "genre": row.get("genero", ""),
    }


# A proposition can receive multiple mechanism tags when the text explicitly names them; preserving overlap prevents distinct signals in one allegation from being collapsed.
TAGS = [
    {
        "code": "urnas_smartmatic_venezuela", "domain": "Urnas e votação",
        "label": "Vínculo Smartmatic/Venezuela",
        "definition": "A proposição liga urnas brasileiras à Smartmatic ou a alegações de fraude venezuelana.",
        "pattern": r"smartmatic|venezuela",
        "objects": {"votacao"},
    },
    {
        "code": "urnas_modelo_codigo_chip", "domain": "Urnas e votação",
        "label": "Modelo, código, chip ou algoritmo da urna",
        "definition": "A proposição nomeia modelo, código, chip, software ou algoritmo como mecanismo relevante.",
        "pattern": r"ue2013|ue2015|modelos? de urnas?|codigo das urnas?|software das urnas?|chip[s]? (?:taiwan|das urnas?)|algoritmos? das urnas?",
        "objects": {"votacao"},
    },
    {
        "code": "urnas_teste_hack_auditoria", "domain": "Urnas e votação",
        "label": "Teste, auditoria, invasão ou vulnerabilidade",
        "definition": "A proposição cita teste de segurança/auditoria, invasão, hackers, plano de ataque, auditabilidade ou vulnerabilidade.",
        "pattern": r"hackers?|invad(?:iu|iram|ir)|invasao|testes? (?:publicos? de )?(?:seguranca|auditoria)|planos? de ataque|inauditavel|vulnerabilidade",
        "objects": {"votacao"},
    },
    {
        "code": "urnas_interferencia_fisica", "domain": "Urnas e votação",
        "label": "Interferência física ou defeito localizado",
        "definition": "A proposição descreve tecla colada/danificada, lacre violado, voto já inserido ou registro de votos sem ação do eleitor.",
        "pattern": r"teclas? (?:[a-z ]{0,22})?colad[ao]s?|teclas? danificad[ao]s?|lacres? (?:eletronicos? )?violad[ao]s?|votos? (?:ja )?inseridos?|votava sozinho|registrou votos sozinha|urna[s]? (?:teriam? sido )?fraudad[ao]s? no (?:df|distrito federal)",
        "objects": {"votacao"},
    },
    {
        "code": "urna_identidade_mesarios", "domain": "Urnas e votação",
        "label": "Identidade, biometria ou ação de mesários",
        "definition": "A proposição cita voto por terceiro/ausente, biometria, título de pessoa falecida ou mesário como mecanismo.",
        "pattern": r"mesari|biometria|voto em nome|eleitores? ausentes?|titulos? de falecidos|votarem por eleitores",
        "objects": {"votacao"},
    },
    {
        "code": "apuracao_painel_pausa", "domain": "Apuração e divulgação",
        "label": "Pausa, painel ou atualização dos resultados",
        "definition": "A proposição menciona pausa, painel, interrupção ou atualização dos resultados; a entrada também pertence ao conjunto de suspeitas, afirmações de fraude ou irregularidades.",
        "pattern": r"pausa|parada|interrupcao|painel|horarios? (?:divergentes?|de atualizacao)|atualizacao dos resultados|divulgacao dos resultados",
        "objects": {"apuracao_totalizacao", "divulgacao"},
    },
    {
        "code": "apuracao_horario_17h", "domain": "Apuração e divulgação",
        "label": "Menção a votos após 17h ou prorrogação",
        "definition": "A proposição menciona 17h, votos após o horário, prorrogação ou urnas já encerradas; a entrada também pertence ao conjunto de suspeitas, afirmações de fraude ou irregularidades. A marca lexical não decide, por si só, que houve fraude.",
        "pattern": r"17h|17 horas|prorrogacao|apos as 17|depois das 17|votos apos o horario|urnas ja encerradas",
        "objects": {"votacao", "apuracao_totalizacao", "divulgacao"},
    },
    {
        "code": "apuracao_padrao_estatistico", "domain": "Apuração e divulgação",
        "label": "Padrão de votos ou argumento matemático",
        "definition": "A proposição usa votação unânime, ausência de votos, proporções improváveis ou impossibilidade matemática como indício.",
        "pattern": r"unanim|nao recebeu votos|votos? so para|matematicamente impossivel|mais eleitores que habitantes|percentual.{0,30}(?:impossivel|fraude)|subida dos votos",
        "objects": {"votacao", "apuracao_totalizacao"},
    },
    {
        "code": "tse_manipulacao_tecnica", "domain": "TSE e instituições",
        "label": "Acusação de manipular sistemas ou resultados",
        "definition": "Com TSE/Tribunal Superior Eleitoral no campo alvo, a proposição atribui roubo, manipulação, alteração técnica ou desaparecimento de votos.",
        "pattern": r"roubou|manipul|alterar sistemas|alterar software|votos? desaparecer|invadiu|invadiram|faria votos sumirem|fraudou eleicao|algoritm",
        "target_pattern": r"\btse\b|tribunal superior eleitoral",
        "objects": None,
    },
    {
        "code": "tse_fiscais_acesso", "domain": "TSE e instituições",
        "label": "Retirada de fiscais ou bloqueio de fiscalização",
        "definition": "Com TSE/Tribunal Superior Eleitoral no campo alvo, a proposição cita fiscais, sala-cofre, retirada, expulsão ou falta de fiscalização.",
        "pattern": r"fiscais?|sala.co|retirad[oa]s?|expuls|acesso|nao sao fiscalizados|fiscalizacao",
        "target_pattern": r"\btse\b|tribunal superior eleitoral",
        "objects": None,
    },
    {
        "code": "tse_decisao_isonomia", "domain": "TSE e instituições",
        "label": "Decisão, horário ou tratamento desigual",
        "definition": "Com TSE/Tribunal Superior Eleitoral no campo alvo, a proposição questiona prorrogação, isonomia, local de votação, suspensão ou outra decisão procedimental.",
        "pattern": r"prorrogacao|quebra de isonomia|tratamento desigual|decisao.{0,25}irregular|mudou locais|impedir comparecimento|suspensa ilegalmente|nao cruza",
        "target_pattern": r"\btse\b|tribunal superior eleitoral",
        "objects": None,
    },
    {
        "code": "fin_uso_maquina_beneficios", "domain": "Financiamento e poder econômico",
        "label": "Máquina pública, recursos ou benefícios",
        "definition": "A proposição cita máquina pública, recursos ou benefícios públicos, gasto oficial ou uso eleitoral de ato estatal; o rótulo não comprova desvio.",
        "pattern": r"maquina publica|recursos publicos|beneficios sociais|gastos e beneficios|uso eleitoral do bicentenario|publicidade oficial|isencao de ipva|nomeacoes.{0,35}periodo eleitoral|atos normativos.{0,35}beneficios?|uso (?:eleitoral )?de beneficios?",
        "objects": {"campanha_financiamento"},
    },
    {
        "code": "fin_abuso_poder_politico_economico", "domain": "Financiamento e poder econômico",
        "label": "Abuso de poder político ou econômico",
        "definition": "A proposição nomeia abuso de poder político/econômico ou uso do poder econômico para favorecer candidatura; não presume que tenha havido gasto ou transferência de recursos.",
        "pattern": r"abusos? de poder (?:economico|politico)|abuso (?:economico|politico)|poder economico.{0,45}(?:favore|campanha|elei[cç])|poder politico.{0,45}(?:favore|campanha|elei[cç])|usou poder economico",
        "objects": {"campanha_financiamento"},
    },
    {
        "code": "fin_compra_votos", "domain": "Financiamento e poder econômico",
        "label": "Compra de votos ou incentivo material ao eleitor",
        "definition": "A proposição afirma ou suspeita compra de votos, pagamento por apoio/voto ou incentivo material eleitoral.",
        "pattern": r"compra.{0,28}voto|comprou votos?|comprar votos?|por pedidos de voto|criptomoedas.{0,55}voto|pagamentos comprariam apoio|dinheiro.{0,30}voto",
        "objects": {"campanha_financiamento"},
    },
    {
        "code": "fin_contas_recursos_nao_declarados", "domain": "Financiamento e poder econômico",
        "label": "Contas, recursos não declarados ou desvio",
        "definition": "A proposição cita prestação/contas de campanha, recursos não declarados, desvio ou falsidade ideológica eleitoral.",
        "pattern": r"prestacao de contas|contas? de campanha|recursos? nao declarad|desvio de r\$|desviar recursos|falsidade ideologica eleitoral|notas? ativas|pagamentos e notas|dados? financeiros? (?:de|do|da|em)",
        "objects": {"campanha_financiamento"},
    },
    {
        "code": "fin_possivel_dinheiro_estrangeiro_campanha", "domain": "Financiamento e poder econômico",
        "label": "Possível financiamento estrangeiro de campanhas",
        "definition": "A proposição menciona explicitamente fundo nos EUA ou possibilidade de financiamento estrangeiro/de campanhas.",
        "pattern": r"financiamento de campanhas|financiamento.{0,35}campanha|fundo nos eua|poderiam ter sido pagas.{0,35}eua",
        "objects": {"campanha_financiamento"},
    },
    {
        "code": "fin_projeto_estrangeiro_pressao", "domain": "Financiamento e poder econômico",
        "label": "Projeto estrangeiro ou pressão econômica",
        "definition": "A proposição cita projeto estrangeiro para financiar grupos não eleitorais, interferência estrangeira ou coerção/pressão econômica; não presume doação a campanha.",
        "pattern": r"projeto dos eua|recursos para grupos de oposicao|coercao economica|interferencia estrangeira|pressao economica",
        "objects": {"campanha_financiamento"},
    },
    {
        "code": "fin_apoio_privado_servicos", "domain": "Financiamento e poder econômico",
        "label": "Serviços, empresas ou apoio privado indireto",
        "definition": "A proposição cita serviços, recursos empresariais, estrutura privada ou financiamento empresarial indireto; o rótulo não determina por si só se o gasto foi irregular.",
        "pattern": r"recursos empresariais|financiamento empresarial|servicos da elytron|consultorias.{0,35}bolsonaro|campanha.{0,40}servicos|estrutura sindical|pagamentos? e notas",
        "objects": {"campanha_financiamento"},
    },
    {
        "code": "fin_prop_meios_comunicacao", "domain": "Financiamento e poder econômico",
        "label": "Propaganda irregular ou abuso dos meios de comunicação",
        "definition": "A proposição cita propaganda eleitoral irregular/antecipada, comunicação usada contra candidatura ou montagem com finalidade eleitoral. O código não presume que houve financiamento.",
        "pattern": r"abuso.{0,25}meios? de comunicacao|uso indevido.{0,25}meios? de comunicacao|propaganda (?:eleitoral )?(?:antecipada|irregular|enganosa)|publicidade eleitoral irregular|videos? manipulados?.{0,60}propaganda|montagens?.{0,60}(?:desgastar|campanha)|uso indevido da comunicacao|uso de comunicacao contra|desfile.{0,50}abuso de poder",
        "objects": {"campanha_financiamento"},
    },
    {
        "code": "cand_cotas_candidaturas_ficticias", "domain": "Candidaturas e cotas",
        "label": "Candidaturas fictícias para cumprir cota de gênero",
        "definition": "A proposição menciona candidaturas fictícias/de fachada ou sem campanha relacionadas à cota de gênero; não presume desvio de recursos quando isso não é dito.",
        "pattern": r"candidatura[s]? feminina.{0,60}desviar|candidaturas? (?:femininas? )?(?:de fachada|ficticias?)|candidaturas? feminin.{0,45}fictici|candidatas?.{0,60}(?:cota|ficticia|fachada)|cota.{0,50}(?:fictici|fraude)|cotas.{0,40}recursos|sem campanha, recursos|desviar recursos",
        "objects": {"campanha_financiamento", "candidaturas_filiacao_cotas"},
    },
    {
        "code": "digital_anuncios_influenciadores", "domain": "Redes e operações digitais",
        "label": "Anúncios, impulsionamento ou influenciadores",
        "definition": "A proposição cita anúncio, publicidade paga, impulsionamento ou influenciadores; o rótulo não presume pagamento quando ele não é explicitado.",
        "pattern": r"anuncios?|impulsionamento|influenciadores?|publicidade paga|contratacao de quase.{0,20}influenciadores?",
        "objects": None,
    },
    {
        "code": "digital_bots_contas_coordenadas_ia", "domain": "Redes e operações digitais",
        "label": "Bots, contas coordenadas ou conteúdo sintético",
        "definition": "A proposição cita bots/automação, contas falsas, coordenação em rede, IA, deepfake ou conteúdo sintético.",
        "pattern": r"bots?|contas automatizadas|contas falsas|rede[s]? coordenad[ao]s?|conteudos? sinteticos?|inteligencia artificial|deepfakes?|operacoes de influencia",
        "objects": None,
    },
    {
        "code": "digital_algoritmo_moderacao_alcance", "domain": "Redes e operações digitais",
        "label": "Algoritmo, moderação ou alcance de plataforma",
        "definition": "A proposição acusa ou discute restrição/remoção de conteúdo, manipulação de busca/alcance ou favorecimento por plataforma.",
        "pattern": r"plataforma[s]?.{0,45}(?:restring|remov|bloque|favorec|censur|manipul)|meta.{0,45}(?:restring|remov|bloque|favorec|censur|manipul)|buscas? no google.{0,30}manipul|algoritmos? (?:das plataformas|de redes)",
        "objects": None,
    },
    {
        "code": "pesquisas_eleitorais", "domain": "Pesquisas de opinião",
        "label": "Pesquisas de opinião eleitoral",
        "definition": "A alegação recebeu o objeto original pesquisas_eleitorais.",
        "pattern": r".",
        "objects": {"pesquisas_eleitorais"},
    },
]


PLATFORM_PATTERNS = [
    ("X/Twitter", r"twitter|x\.com|rede social x|rede x|plataforma x|no x|na x"),
    ("WhatsApp", r"whatsapp"), ("Instagram", r"instagram"),
    ("Facebook", r"facebook"), ("Telegram", r"telegram"),
    ("TikTok", r"tiktok"), ("YouTube", r"youtube"),
    ("Meta", r"\bmeta\b"), ("Google", r"google"), ("Kwai", r"kwai"),
    ("Redes sociais (genérico)", r"redes? sociais?"),
]


def normalize_actor(name: str) -> str:
    key = re.sub(r"[^a-z0-9]+", " ", fold(name)).strip()
    if key in {"tse", "tribunal superior eleitoral"}:
        return "TSE"
    if key in {"mpe", "ministerio publico eleitoral"}:
        return "Ministério Público Eleitoral"
    if key in {"pl", "partido liberal"}:
        return "PL"
    if key in {"missao", "partido missao"}:
        return "Partido Missão"
    if key in {"lula", "luiz inacio lula da silva", "luiz inacio lula"}:
        return "Lula"
    if key in {"flavio bolsonaro"}:
        return "Flávio Bolsonaro"
    if key in {"jair bolsonaro"}:
        return "Jair Bolsonaro"
    if key == "cristiano zanin":
        return "Cristiano Zanin"
    if key in {"mesarios", "mesario"}:
        return "Mesários"
    return name.strip()


publication_rows = read_csv(ROOT / "data" / "triagem_880.csv")
articles: dict[str, dict] = {}
for row in publication_rows:
    if row["incluir_no_corpus_final"] != "sim":
        continue
    articles[row["id"]] = {
        "id": row["id"], "date": row["data"], "outlet": row["veiculo"],
        "title": row["titulo"], "url": row["url"], "genre": row["genero"],
    }
raw_claims = read_csv(ROOT / "data" / "alegacoes_1025.csv")
claims = []
for row in raw_claims:
    meta = articles.get(row["publicacao_id"])
    if not meta:
        continue
    objects = parse_json_list(row.get("objetos"))
    source_evidence = [
        item.get("trecho", "")
        for item in parse_json_list(row.get("evidencias"))
        if isinstance(item, dict)
    ]
    evidence = unique_nonempty(source_evidence)
    is_allegation = row.get("modalidade") in ALLEGATION_MODALITIES
    proposition_target = fold(f"{row.get('proposicao', '')} {row.get('alvo', '')}")
    tags = []
    if is_allegation:
        for spec in TAGS:
            if spec["objects"] is not None and not set(objects).intersection(spec["objects"]):
                continue
            if spec.get("target_pattern") and not re.search(spec["target_pattern"], fold(row.get("alvo", ""))):
                continue
            if re.search(spec["pattern"], proposition_target):
                tags.append(spec["code"])
    platform_text = fold(" ".join([row.get("proposicao", ""), row.get("alvo", ""), *evidence]))
    platforms = [label for label, pattern in PLATFORM_PATTERNS if re.search(pattern, platform_text)]
    claims.append({
        "id": row["alegacao_local_id"], "publicationId": row["publicacao_id"],
        "date": meta["date"], "outlet": meta["outlet"], "title": meta["title"], "url": meta["url"],
        "proposition": row.get("proposicao", ""), "objects": objects,
        "modality": row.get("modalidade", ""), "accuser": row.get("alegador", ""),
        "target": row.get("alvo", ""), "reach": row.get("alcance", ""),
        "bodyTreatment": row.get("tratamento_corpo", ""), "titleTreatment": row.get("tratamento_titulo", ""),
        "situation": row.get("situacao_relatada", ""), "isAllegation": is_allegation,
        "tags": tags, "platforms": platforms,
        "evidence": evidence[0][:420] if evidence else "",
    })

allegations = [row for row in claims if row["isAllegation"]]
claim_publications = {row["publicationId"] for row in claims}
allegation_publications = {row["publicationId"] for row in allegations}
tag_rows = []
for spec in TAGS:
    matched = [row for row in allegations if spec["code"] in row["tags"]]
    tag_rows.append({
        "code": spec["code"], "domain": spec["domain"], "label": spec["label"],
        "definition": spec["definition"], "claims": len(matched),
        "publications": len({row["publicationId"] for row in matched}),
        "formulations": len({re.sub(r"\s+", " ", fold(row["proposition"])).strip() for row in matched}),
    })

modality_counts = Counter(row["modality"] for row in claims)
object_counts: dict[str, dict] = defaultdict(lambda: {"claims": 0, "publications": set()})
for row in allegations:
    for code in set(row["objects"]):
        object_counts[code]["claims"] += 1
        object_counts[code]["publications"].add(row["publicationId"])
object_rows = [
    {"code": code, "claims": data["claims"], "publications": len(data["publications"])}
    for code, data in object_counts.items()
]
object_rows.sort(key=lambda row: (-row["claims"], row["code"]))

platform_rows = []
for label, _ in PLATFORM_PATTERNS:
    matched = [row for row in allegations if label in row["platforms"]]
    if matched:
        platform_rows.append({
            "platform": label, "claims": len(matched),
            "publications": len({row["publicationId"] for row in matched}),
        })
platform_rows.sort(key=lambda row: (-row["claims"], row["platform"]))

TARGET_GROUPS = [
    ("TSE / Tribunal Superior Eleitoral", "Instituição", r"\btse\b|tribunal superior eleitoral"),
    ("STF / Supremo Tribunal Federal", "Instituição", r"\bstf\b|supremo tribunal federal"),
    ("Cristiano Zanin", "Autoridade judicial", r"cristiano zanin|\bzanin\b"),
    ("Lula", "Candidato/político", r"\blula\b|luiz inacio lula"),
    ("Flávio Bolsonaro", "Candidato/político", r"flavio bolsonaro"),
    ("Jair Bolsonaro", "Candidato/político", r"jair bolsonaro"),
    ("Bolsonaro (sobrenome no alvo)", "Referência política", r"\bbolsonaro\b"),
    ("Geraldo Alckmin", "Candidato/político", r"alckmin"),
    ("Douglas Ruas", "Candidato/político", r"douglas ruas"),
    ("Alan Rick", "Candidato/político", r"alan rick"),
    ("Augusto Cury", "Candidato/político", r"augusto cury"),
    ("Mesários", "Agentes eleitorais", r"mesarios?"),
    ("Meta", "Plataforma", r"\bmeta\b"),
    ("Podemos", "Partido", r"\bpodemos\b"),
    ("PL / Partido Liberal", "Partido", r"\bpl\b|partido liberal"),
    ("Partido Missão", "Partido", r"partido missao|\bmissao\b"),
    ("PT / Partido dos Trabalhadores", "Partido", r"\bpt\b|partido dos trabalhadores"),
]
target_rows = []
for label, entity_type, pattern in TARGET_GROUPS:
    matched = [row for row in allegations if re.search(pattern, fold(row["target"]))]
    if matched:
        target_rows.append({
            "name": label, "type": entity_type, "claims": len(matched),
            "publications": len({row["publicationId"] for row in matched}),
            "pattern": pattern,
        })

actor_files = [read_csv(ROOT / "data" / "atores_2146.csv")]
actor_counts: dict[tuple[str, str], set[str]] = defaultdict(set)
for actor_rows in actor_files:
    for row in actor_rows:
        if row["publicacao_id"] not in articles:
            continue
        normalized_name = normalize_actor(row.get("nome", ""))
        for role in parse_json_list(row.get("papeis")):
            actor_counts[(role, normalized_name)].add(row["publicacao_id"])

def actor_role_rows(role: str, limit: int = 12) -> list[dict]:
    result = [
        {"name": name, "publications": len(pub_ids)}
        for (actor_role, name), pub_ids in actor_counts.items()
        if actor_role == role
    ]
    result.sort(key=lambda row: (-row["publications"], row["name"].casefold()))
    return result[:limit]


funnel = {
    "screened": len(publication_rows),
    "included": len(articles), "outside": len(publication_rows) - len(articles),
    "criteria": [
        "Texto integral conferido",
        "Pertinência central, contextual ou institucional pertinente",
        "Duplicatas e registros fora do objeto não acrescentam novo conteúdo",
    ],
}
scale = {
    "finalPublications": len(articles), "claimEntries": len(claims),
    "claimPublications": len(claim_publications), "allegationEntries": len(allegations),
    "allegationPublications": len(allegation_publications),
    "otherEntries": len(claims) - len(allegations),
    "missingTargets": sum(not row["target"].strip() for row in claims),
    "pollClaims": sum("pesquisas_eleitorais" in row["objects"] for row in allegations),
    "pollPublications": len({row["publicationId"] for row in allegations if "pesquisas_eleitorais" in row["objects"]}),
    "modalities": dict(modality_counts),
}

# Examples use fixed publication IDs so readers can trace each chart label to the same coded passage after every rebuild.
preferred_example_ids = [
    "DOC-002-a01", "DOC-065-a01", "DOC-082-a01", "DOC-091-a01",
    "DOC-093-a02", "DOC-011-a02", "DOC-060-a01", "ADD-344-a01",
    "DOC-090-a04", "DOC-136-a01", "DOC-084-a09", "DOC-084-a10",
    "DOC-172-a01", "DOC-188-a05", "ADD-123-a01",
]
claim_by_id = {row["id"]: row for row in claims}
examples = [claim_by_id[item] for item in preferred_example_ids if item in claim_by_id]

base_paths = [
    "data/triagem_880.csv", "data/alegacoes_1025.csv",
    "data/atores_2146.csv", "docs/MANUAL_CODIFICACAO.md",
    "docs/protocolo_aplicacao.md", "docs/adendo_triagem.md",
]

snapshot = {
    "surface": "report", "title": "Fraude eleitoral nas notícias: quem acusa, contra quem e por quais mecanismos",
    "asOf": "2026-11-09", "generatedAt": datetime.now(timezone.utc).isoformat(),
    "status": "reviewed", "filters": [],
    "sourcePaths": base_paths,
    "funnel": funnel,
    "scale": scale,
    "objects": object_rows,
    "tagDefinitions": [
        {key: spec[key] for key in ("code", "domain", "label", "definition")}
        for spec in TAGS
    ],
    "tags": tag_rows,
    "accusers": actor_role_rows("acusador"),
    "accused": actor_role_rows("acusado"),
    "targets": target_rows,
    "platforms": platform_rows,
    "examples": examples,
    "claims": claims,
}
OUT.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")

def write_rows(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json.dumps(value, ensure_ascii=False) if isinstance(value, (list, dict)) else value for key, value in row.items()})

write_rows(ROOT / "data" / "publicacoes_corpus_final.csv", [row for row in publication_rows if row["incluir_no_corpus_final"] == "sim"])
write_rows(ROOT / "data" / "alegacoes_corpus_final.csv", claims)
write_rows(ROOT / "data" / "atores_corpus_final.csv", [row for row in actor_files[0] if row["publicacao_id"] in articles])
for source_name, output_name in [("episodios_723.csv", "episodios_corpus_final.csv"), ("enquadramentos_705.csv", "enquadramentos_corpus_final.csv"), ("evidencias_24683.csv", "evidencias_corpus_final.csv")]:
    source_rows = read_csv(ROOT / "data" / source_name)
    write_rows(ROOT / "data" / output_name, [row for row in source_rows if row["publicacao_id"] in articles])
summary = {
    "snapshot": str(OUT), "filterFunnel": funnel, "scale": scale,
    "tagCounts": [{"code": row["code"], "claims": row["claims"], "publications": row["publications"]} for row in tag_rows],
    "accusersTop": snapshot["accusers"][:6], "accusedTop": snapshot["accused"][:6],
    "platforms": platform_rows,
}
print(json.dumps(summary, ensure_ascii=False))
