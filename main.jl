using Pluto


# phases
# 1) create/discover/load causal model  (causal estimand)
# 2) identify statistical model from causal model (statistical estimand)
# 3) estimate effects given data with the statistical model (estimate)
# 4) post-estimate sanity checks (i.e. refute as MS calls it )


# similar projects/sites
# 1) Colliders in Epidemiology: https://watzilei.com/shiny/collider/
# 2) Dagitty: http://www.dagitty.net/dags.html


UI_TYPE = "dash"

if UI_TYPE == "dash"
    println("running dash")
    include("app.jl")
else
    println("running pluto")
    Pluto.run()
end
