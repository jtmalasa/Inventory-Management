import dash_bootstrap_components as dbc
from dash import html, dash_table
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from app1 import app
from apps import dbconnect as db

layout = html.Div(
    [
        html.H2('Product List'),
        dbc.Card(
            [
                dbc.CardHeader(html.H4("View Products", style={'fontweight': 'bold'})),
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Label("Search Product", width=2),
                                        dbc.Col(
                                            dbc.Input(
                                                type="text",
                                                id="product_name_filter",
                                                placeholder="Enter filter",
                                            ),
                                            width=6,
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                                html.Div(
                                    "This will contain the product table",
                                    id = 'product_list',
                                    style = {'text-align': 'center'}
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)

@app.callback(
    [
        Output('product_list','children')
    ],
    [
        Input('url', 'pathname'),
        Input('product_name_filter', 'value'),
    ]
)
def prodhome_loadprodlist(pathname, searchterm):
    if pathname == '/products':
        sql = """ SELECT prod_id, prod_name, prod_brand, prod_compatibility, stock_onhand, stock_rop
            FROM inventory
            WHERE NOT prod_delete_ind
            ORDER BY prod_id ASC;
        """
        values = []
        cols = ['ID', 'Product Name', 'Brand', 'Compatibility','Stock Onhand', 'Stock ROP']
        if searchterm:
            sql +=  """ SELECT prod_id, prod_name, prod_brand, prod_compatibility, stock_onhand, stock_rop
            FROM inventory
            WHERE NOT prod_delete_ind
            AND prod_name ILIKE %s """
            values += [f"%{searchterm}%"]
        df = db.querydatafromdatabase(sql,values,cols)
        if df.shape:

            table = dash_table.DataTable(
                data=df.to_dict('records'),
                sort_action='native',
                columns=[
                    {'name': 'ID', 'id': 'ID', 'type': 'any', 'editable': False},
                    {'name': 'Product Name', 'id': 'Product Name', 'type': 'text'},
                    {'name': 'Brand', 'id': 'Brand', 'type': 'text'},
                    {'name': 'Compatibility', 'id': 'Compatibility', 'type': 'text'},
                    {'name': 'Stock Onhand', 'id': 'Stock Onhand', 'type': 'integer'},
                    {'name': 'Stock ROP', 'id': 'Stock ROP', 'type': 'integer'},
                ],
                editable=True,
                style_header={
                    'fontWeight': 'bold',
                    'font_size': '16px',
                },
                style_cell = {
                    'font_family': 'Sans-serif',
                    'font_size': '15px',
                    'text_align': 'center',
                    'striped':'True'
                },
                style_data_conditional=[
                    {
                        'if': {
                            'filter_query': '{Stock ROP} >= {Stock Onhand}',
                        },
                        'backgroundColor': 'red',
                        'color': 'white'
                    },
                ],
            )
            return[table]
        else:
            return ['No records to display']
    else:
        raise PreventUpdate
