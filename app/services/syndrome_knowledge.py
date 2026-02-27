"""
Base determinística de conhecimento clínico por síndrome.
Utilizada como fallback seguro quando a IA falha ou está indisponível.

REGRAS:
- Conteúdo educacional
- Não fecha diagnóstico
- Não prescreve doses
- Foco em segurança do paciente
- Pronto-Socorro adulto
"""

SYNDROME_KNOWLEDGE = {

    # =====================================================
    # DOR TORÁCICA
    # =====================================================
    "dor_toracica": {
        "questions_needed": [
            "Tempo de início e característica da dor (opressiva, em aperto, queimação).",
            "Irradiação para braço esquerdo, mandíbula ou dorso.",
            "Fatores de melhora ou piora (esforço, repouso, respiração).",
            "Sintomas associados como dispneia, náuseas, sudorese ou síncope.",
            "Histórico cardiovascular prévio e fatores de risco."
        ],
        "differentials": [
            {"name": "Síndrome Coronariana Aguda", "reasoning": "Dor opressiva, irradiação e fatores de risco cardiovasculares."},
            {"name": "Tromboembolismo Pulmonar", "reasoning": "Dor torácica associada à dispneia súbita e hipoxemia."},
            {"name": "Dissecção de Aorta", "reasoning": "Dor súbita, intensa, em rasgo, com possível irradiação para dorso."},
            {"name": "Pneumotórax", "reasoning": "Dor torácica súbita associada à dispneia."},
            {"name": "Pericardite Aguda", "reasoning": "Dor que piora ao deitar e melhora ao sentar-se."
            }
        ],
        "red_flags": [
            "Instabilidade hemodinâmica",
            "Alterações eletrocardiográficas sugestivas de isquemia",
            "Hipotensão ou choque",
            "Dor torácica súbita de alta intensidade"
        ],
        "recommended_tests": [
            "Eletrocardiograma de 12 derivações",
            "Dosagem seriada de marcadores de necrose miocárdica",
            "Radiografia de tórax",
            "Monitorização cardíaca contínua"
        ],
        "educational_management": [
            "Priorizar avaliação imediata e monitorização contínua.",
            "Seguir protocolos institucionais para dor torácica.",
            "Manter abordagem sindrômica até exclusão de causas graves."
        ]
    },

    # =====================================================
    # DISPNEIA
    # =====================================================
    "dispneia": {
        "questions_needed": [
            "Início súbito ou progressivo da dispneia.",
            "Presença de dor torácica associada.",
            "Histórico de doença pulmonar ou cardíaca prévia.",
            "Saturação de oxigênio e necessidade de suporte ventilatório.",
            "Sintomas associados como tosse, febre ou hemoptise."
        ],
        "differentials": [
            {"name": "Insuficiência Respiratória Aguda", "reasoning": "Hipoxemia e desconforto respiratório."},
            {"name": "Edema Agudo de Pulmão", "reasoning": "Dispneia súbita associada a congestão pulmonar."},
            {"name": "Tromboembolismo Pulmonar", "reasoning": "Dispneia súbita, hipoxemia e dor torácica."},
            {"name": "Pneumonia Grave", "reasoning": "Dispneia associada a febre e sinais infecciosos."},
            {"name": "Exacerbação de Asma ou DPOC", "reasoning": "Histórico respiratório prévio com piora aguda."
            }
        ],
        "red_flags": [
            "Saturação de oxigênio < 90%",
            "Uso de musculatura acessória",
            "Alteração do nível de consciência",
            "Instabilidade hemodinâmica"
        ],
        "recommended_tests": [
            "Oximetria contínua",
            "Gasometria arterial",
            "Radiografia de tórax",
            "Avaliação laboratorial conforme suspeita clínica"
        ],
        "educational_management": [
            "Garantir vias aéreas pérvias e oxigenação adequada.",
            "Avaliação rápida para causas potencialmente fatais.",
            "Seguir protocolos institucionais de insuficiência respiratória."
        ]
    },

    # =====================================================
    # SEPSE / FEBRE SEM FOCO
    # =====================================================
    "sepse": {
        "questions_needed": [
            "Tempo de início da febre e sintomas associados.",
            "Possível foco infeccioso identificado.",
            "Uso recente de antimicrobianos.",
            "Comorbidades e estado imunológico.",
            "Sinais de disfunção orgânica."
        ],
        "differentials": [
            {"name": "Sepse", "reasoning": "Infecção associada a sinais de disfunção orgânica."},
            {"name": "Choque Séptico", "reasoning": "Hipotensão persistente apesar de reposição volêmica."},
            {"name": "Infecção Comunitária Grave", "reasoning": "Febre e sinais sistêmicos importantes."}
        ],
        "red_flags": [
            "Hipotensão",
            "Taquicardia persistente",
            "Alteração do nível de consciência",
            "Oligúria"
        ],
        "recommended_tests": [
            "Lactato sérico",
            "Hemoculturas conforme protocolo",
            "Exames laboratoriais completos",
            "Avaliação do foco infeccioso"
        ],
        "educational_management": [
            "Reconhecimento precoce e abordagem protocolar.",
            "Monitorização rigorosa e suporte hemodinâmico.",
            "Seguir protocolo institucional de sepse."
        ]
    },

    # =====================================================
    # AVC
    # =====================================================
    "avc": {
        "questions_needed": [
            "Horário exato do início dos sintomas.",
            "Déficits neurológicos presentes.",
            "Uso de anticoagulantes ou antiagregantes.",
            "Histórico prévio de AVC ou AIT.",
            "Comorbidades relevantes."
        ],
        "differentials": [
            {"name": "AVC Isquêmico", "reasoning": "Déficit neurológico focal de início súbito."},
            {"name": "AVC Hemorrágico", "reasoning": "Déficit neurológico associado a cefaleia intensa."},
            {"name": "Hipoglicemia", "reasoning": "Alteração neurológica reversível com correção metabólica."}
        ],
        "red_flags": [
            "Déficit neurológico progressivo",
            "Alteração do nível de consciência",
            "Cefaleia súbita intensa"
        ],
        "recommended_tests": [
            "Glicemia capilar imediata",
            "Tomografia de crânio sem contraste",
            "Monitorização neurológica contínua"
        ],
        "educational_management": [
            "Avaliação imediata conforme protocolo de AVC.",
            "Determinar elegibilidade para terapias de reperfusão.",
            "Manter abordagem tempo-dependente."
        ]
    },

    # =====================================================
    # TRAUMA
    # =====================================================
    "trauma": {
        "questions_needed": [
            "Mecanismo do trauma.",
            "Tempo decorrido desde o evento.",
            "Perda de consciência associada.",
            "Dor ou déficit neurológico.",
            "Uso de anticoagulantes."
        ],
        "differentials": [
            {"name": "Traumatismo Cranioencefálico", "reasoning": "Queda ou impacto com possível alteração neurológica."},
            {"name": "Fraturas", "reasoning": "Dor localizada e limitação funcional."},
            {"name": "Lesões Internas", "reasoning": "Trauma com sinais sistêmicos ou instabilidade."}
        ],
        "red_flags": [
            "Instabilidade hemodinâmica",
            "Alteração do nível de consciência",
            "Dor intensa ou deformidade evidente"
        ],
        "recommended_tests": [
            "Avaliação primária conforme ATLS",
            "Exames de imagem conforme mecanismo",
            "Monitorização contínua"
        ],
        "educational_management": [
            "Priorizar abordagem ABCDE.",
            "Identificar rapidamente lesões ameaçadoras à vida.",
            "Seguir protocolos de trauma."
        ]
    }
}
