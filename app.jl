using Dash
using DashHtmlComponents
using DashCoreComponents
# using DashCytoscape

app = dash(external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"])

app.layout = html_div() do
    html_h1("Hello Dash"),
        dcc_tabs(id="stage-tabs", value="tab-model") do
            dcc_tab(value="tab-model", label="Model") do
                html_div("Model")
            end,
            dcc_tab(value="tab-identify", label="Identify ") do 
                
            end,
            dcc_tab(value="tab-estimate", label="Estimate") do 
                
            end,
            dcc_tab(value="tab-verify", label="Verify") do 
                
            end
        end,
        html_div(id="tab-content")
    #     cyto_cytoscape(
    #     id="cytoscape-elements-boolean",
    #     layout=(name="preset",),
    #     style=(width="100%",
    #            height="400px"),
    #     elements=[(
    #                 data=(id="one", label="Locked"),
    #                 position=(x=75, y=75),
    #                 locked=true
    #             ),
    #             (
    #                 data=(id="two", label="Selected"),
    #                 position=(x=75, y=200),
    #                 selected=true
    #             ),
    #             (
    #                 data=(id="three", label="Not Selectable"),
    #                 position=(x=200, y=75),
    #                 selectable=false
    #             ),
    #             (
    #                 data=(id="four", label="Not Grabbable"),
    #                 position=(x=200, y=200),
    #                 grabbable=false
    #             ),
    #             (
    #                 data=(source="one", target="two"),
    #             ),
    #             (
    #                 data=(source="two", target="three"),
    #             ),
    #             (
    #                 data=(source="three", target="four"),
    #             ),
    #             (
    #                 data=(source="two", target="four"),
    #             )                
    #     ]
    # )
    # dcc_graph(
    #     id = "example-graph",
    #     figure = (
    #         data = [
    #             (x = [1, 2, 3], y = [4, 1, 2], type = "bar", name = "SF"),
    #             (x = [1, 2, 3], y = [2, 4, 5], type = "bar", name = "Montréal"),
    #         ],
    #         layout = (title = "Dash Data Visualization",)
    #     )
    # )
end


callback!(app, Output("tab-content", "children"), Input("stage-tabs", "value")) do tab
    # extra = "-"
    if tab == "tab-model"
        return show_model_creation_content()
    else
        # return tab
        return html_h3("Tab $tab ... ")
    end
    # # isnothing() && throw(PreventUpdate())
end


function show_model_creation_content()
    extra = "uber model"
    return extra
end

run_server(app, "0.0.0.0", 8080, debug=true)
