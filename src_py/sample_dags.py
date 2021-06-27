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
        "sbp[outcome] -> proteinuria",
    ],
    "Collider": [
        "Z -> X[treatment]",
        "X -> Y[outcome]",
        "Z -> Y"
    ],
    "M-bias": [
        "U₁[unobserved] -> Z",
        "U₁[unobserved] -> Y[outcome]",
        "U₂[unobserved] -> X[treatment]",
        "U₂[unobserved] -> Z",
        "X -> Y"
    ],
    "canonical_frontdoor": [
        "X[T] -> M",
        "M -> Y[O]",
        "U[U] -> X",
        "U -> Y"
    ],
    "canonical_instrument": [
        "Z -> X[T]",
        "X[T] -> Y[O]",
        "U[U] -> X",
        "U[U] -> Y",
    ],
    "Shrier&Platt, 2008": SHRIER_PLATT_2008,
    "big-M": [
        "Z₅ -> Y[outcome]",
        "Z₆ -> Y",
        "Z₁ -> Y",
        "X[treatment] -> Z₆",
        "Z₄ -> Z₅",
        "Z₃ -> Z₂",
        "Z₄ -> Z₁",
        "Z₃ -> Z₁",
        "Z₂ -> X",
        "Z₁ -> X"
    ]
}
# add more complex Shrier & Platt 2008: https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/1471-2288-8-70



# Frontdoor example
#  X --> Z --> Y
#  U --> X; U --> Y
# e_x <- rnorm(1000)
# e_x <- rnorm(1000)
# e_y <- rnorm(1000)
# e_z <- rnorm(1000)
# u <- rnorm(1000)

# x <- 1*(e_x + u > 0)
# z <- 1*(x + e_z > 0.5)
# y <- 1*(z + e_y + u > 0.5)

# z_dox <- 1*(1 + e_Z > .5)
# y_dox <- 1*(z_dox + e_y  + u > .5)

