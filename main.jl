using Pluto


UI_TYPE = "pluto"

if UI_TYPE == "dash"
    println("running dash")
    include("app.jl")
else
    println("running pluto")
    Pluto.run()
end
