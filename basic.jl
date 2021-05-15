### A Pluto.jl notebook ###
# v0.14.5

using Markdown
using InteractiveUtils

# ╔═╡ 831a3d08-b4f3-11eb-101b-a19a95d2b62e
begin
	using LightGraphs
	using GraphPlot
	using ParserCombinator.Parsers.DOT: nodes, edges, parse_dot, StringID
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
    T -> M -> X -> Y;
    T -> Y;
}"

# ╔═╡ 8302c22b-816c-43cf-9d06-60a9daaa56fb
graph, nodelabels = loaddot(gio, "graphname")

# ╔═╡ 4ae575f1-a224-4b98-8142-207a1c9b0094
gplot(graph, layout=circular_layout, nodelabel=nodelabels)

# ╔═╡ ae162157-5768-4935-a1ee-b720fb2d1dc7


# ╔═╡ Cell order:
# ╠═831a3d08-b4f3-11eb-101b-a19a95d2b62e
# ╠═b1abedc3-647e-4f64-ad78-c4b0eeff8510
# ╠═48203bec-8156-489a-b04d-9a613526c85e
# ╠═7e9da9c2-ac34-4ec9-a6ad-f81d67435c5b
# ╠═8302c22b-816c-43cf-9d06-60a9daaa56fb
# ╠═4ae575f1-a224-4b98-8142-207a1c9b0094
# ╠═ae162157-5768-4935-a1ee-b720fb2d1dc7
