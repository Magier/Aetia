SHRIER_PLATT_2008 = [
        "Warm-up Exercises[treatment] -> Intra-game Proprioception",
        "Intra-game Proprioception -> Injury[outcome]",
        "Coach -> Team motivation, aggression",
        "Coach -> Fitness Level",
        "Genetics -> Fitness Level",
        "Genetics -> Neuromuscular Fatigue",
        "Genetics -> Connective Tissue Disorder",
        "Team motivation, aggression -> Warm-up Exercises",
        "Team motivation, aggression -> Previous Injury",
        "Fitness Level -> Pre-game Proprioception",
        "Fitness Level -> Neuromuscular Fatigue",
        "Connective Tissue Disorder -> Neuromuscular Fatigue",
        "Connective Tissue Disorder -> Tissue Weakness",
        "Pre-game Proprioception -> Warm-up Exercises",
        "Neuromuscular Fatigue -> Intra-game Proprioception",
        "Neuromuscular Fatigue -> Injury",
        "Contact Sport -> Previous Injury",
        "Contact Sport -> Intra-game Proprioception",
        "Tissue Weakness -> Injury",
    ]


SAMPLE_DAGS = {
    "default": [
        "age -> sodium",
        "age -> sbp",
        "w[unobserved] -> age",
        "sodium[treatment] -> proteinuria",
        "sodium -> mediator",
        "mediator -> sbp",
        "sbp[outcome] -> proteinuria"
    ],
    "Collider": [
        "L -> A[treatment]",
        "A -> Y[outcome]",
        "L -> Y"
    ],
    "M-bias": [
        "U₁[unobserved] -> Z",
        "U₁[unobserved] -> Y[outcome]",
        "U₂[unobserved] -> A[treatment]",
        "U₂[unobserved] -> Z",
        "A -> Y"
    ],
    "frontdoor": [
        "A[treatment] -> M",
        "M -> Y[outcome]",
        "U[unobserved] -> A",
        "U -> Y"
    ],
    "Shrier&Platt, 2008": SHRIER_PLATT_2008
}
# add more complex Shrier & Platt 2008: https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/1471-2288-8-70
