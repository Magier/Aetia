### A Pluto.jl notebook ###
# v0.14.5

using Markdown
using InteractiveUtils

# ╔═╡ 831a3d08-b4f3-11eb-101b-a19a95d2b62e
begin
	using CSV
	using DataFrames
	using LightGraphs
	using GLM
	using GraphPlot
	using ParserCombinator.Parsers.DOT: nodes, edges, parse_dot, StringID
    using Statistics
end

# ╔═╡ 1d7b6d76-8974-4480-942d-35e895ac0c69


# ╔═╡ cb7406e4-ae75-4c99-b7d5-842055b52aee
df = CSV.read("./data/sodium.csv", DataFrame)
df = select!(df, Not(:Column1))   # drop index column

# ╔═╡ 3c9d639a-dea3-40f5-bec0-be46ecf332e3
begin
    ols = lm(@formula(sbp ~ sodium + age + proteinuria), df)

    xt = copy(df[:,Not(:sbp)])
    xt₁ = copy(xt)
    xt₁.sodium .= 1
    xt₂ = copy(xt)
    xt₂.sodium .= 0

    ate_est = mean(predict(ols, xt₁) - predict(ols, xt₂))
    println("ATE estimate: $ate_est")
end


begin
    ols_causal = lm(@formula(sbp ~ sodium + age), df)

    xt = copy(df[:,Not([:sbp, :proteinuria])])
    xt₁ = copy(xt)
    xt₁.sodium .= 1
    xt₂ = copy(xt)
    xt₂.sodium .= 0

    causal_ate_est = mean(predict(ols_causal, xt₁) - predict(ols_causal, xt₂))
    println("causal ATE estimate: $causal_ate_est")
end


# ╔═╡ 48203bec-8156-489a-b04d-9a613526c85e
function _dot_read_one_graph(pg)
    isdir = pg.directed
    nvg = length(nodes(pg))
    nodedict = Dict(zip(collect(nodes(pg)), 1:nvg))
    if isdir
        g = LightGraphs.DiGraph(nvg)
    else
        g = LightGraphs.Graph(nvg)
    end
    for es in edges(pg)
        s = nodedict[es[1]]
        d = nodedict[es[2]]
        add_edge!(g, s, d)
    end
    return g, collect(nodes(pg))
end

# ╔═╡ b1abedc3-647e-4f64-ad78-c4b0eeff8510
function loaddot(gdot::String, gname::String)
    p = parse_dot(gdot)
    for pg in p
        isdir = pg.directed
        possname = isdir ? StringID("digraph") : StringID("graph")
        name = get(pg.id, possname).id
        name == gname && return _dot_read_one_graph(pg)
    end
    error("Graph $gname not found")
end



# ╔═╡ 7e9da9c2-ac34-4ec9-a6ad-f81d67435c5b
gio = "digraph graphname {
    age -> sodium;
	age -> sbp;
	sodium -> proteinuria;
	sodium -> sbp;
    sbp -> proteinuria;
}"

# ╔═╡ abb14b1e-75fb-4a3f-9973-c6ec4fdb2722


# ╔═╡ 8302c22b-816c-43cf-9d06-60a9daaa56fb
graph, nodelabels = loaddot(gio, "graphname")

# ╔═╡ 4ae575f1-a224-4b98-8142-207a1c9b0094
gplot(graph, layout=circular_layout, nodelabel=nodelabels)

# ╔═╡ ae162157-5768-4935-a1ee-b720fb2d1dc7
begin
	Xt = df[:, ["sodium", "age", "proteinuria"]]
	y = df[!, "sbp"]
end

# ╔═╡ 2aa55dbe-4776-46df-9107-8bd64a545ee4


# ╔═╡ f7a19ddb-391e-49e0-9912-990edc76e92b


# ╔═╡ 41ed3b5e-cdb5-4478-86ce-138f08c09784


# ╔═╡ Cell order:
# ╠═831a3d08-b4f3-11eb-101b-a19a95d2b62e
# ╠═1d7b6d76-8974-4480-942d-35e895ac0c69
# ╠═cb7406e4-ae75-4c99-b7d5-842055b52aee
# ╠═3c9d639a-dea3-40f5-bec0-be46ecf332e3
# ╠═b1abedc3-647e-4f64-ad78-c4b0eeff8510
# ╠═48203bec-8156-489a-b04d-9a613526c85e
# ╠═7e9da9c2-ac34-4ec9-a6ad-f81d67435c5b
# ╠═abb14b1e-75fb-4a3f-9973-c6ec4fdb2722
# ╠═8302c22b-816c-43cf-9d06-60a9daaa56fb
# ╠═4ae575f1-a224-4b98-8142-207a1c9b0094
# ╠═ae162157-5768-4935-a1ee-b720fb2d1dc7
# ╠═2aa55dbe-4776-46df-9107-8bd64a545ee4
# ╠═f7a19ddb-391e-49e0-9912-990edc76e92b
# ╠═41ed3b5e-cdb5-4478-86ce-138f08c09784
