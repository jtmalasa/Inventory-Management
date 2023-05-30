import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from app1 import app
from apps import dbconnect as db


layout = html.Div(
    [
        html.H2('Inventory List'),
        html.Hr(),
        dbc.Card(
            [
                dbc.CardHeader(html.H4("Manage Inventory")),
                dbc.CardBody(
                    [
                        dbc.Button('Add Product', color='secondary', href='/inventory/inventory_profile?mode=add',
                                    style={'background-color':'#5D5856','color': '#f5f8ef', 'border':'0px'}
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                html.H6('View Products', style={'fontweight': 'bold'}),
                                dbc.Row(
                                    [
                                        dbc.Label("Search Product", width=2),
                                        dbc.Col(
                                            dbc.Input(
                                                type="text",
                                                id="inv_name_filter",
                                                placeholder="Enter filter",
                                            ),
                                            width=6,
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                                html.Div(
                                    "This will contain the inventory table",
                                    id = 'inv_list',
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
        Output('inv_list','children')
    ],
    [
        Input('url', 'pathname'),
        Input('inv_name_filter', 'value'),
    ]
)
def invhome_loadinvlist(pathname, searchterm):
    if pathname == '/inventory':
        sql = """ SELECT prod_id, prod_name, stock_onhand, stock_rop, stock_backorder, CONCAT('₱', TO_CHAR(cost, 'fm999G999D00')), CONCAT('₱', TO_CHAR(sell_price, 'fm999G999D00'))
            FROM inventory 
            WHERE NOT prod_delete_ind
            ORDER BY prod_id ASC;
        """
        values = []
        cols = ['ID', 'Product Name', 'Stock Onhand', 'Stock ROP', 'Stock backorder', 'Cost', 'Selling Price']
        
        if searchterm:
            sql += """ SELECT prod_id, prod_name, stock_onhand, stock_rop, stock_backorder, CONCAT('₱', TO_CHAR(cost, 'fm999G999D99')), CONCAT('₱', TO_CHAR(sell_price, 'fm999G999D99'))
                FROM inventory 
                WHERE NOT prod_delete_ind
                AND prod_name ILIKE %s """
            values += [f"%{searchterm}%"]
        df = db.querydatafromdatabase(sql,values,cols)
        
        if df.shape:
            buttons=[]
            for product_id in df['ID']:
                buttons+=[
                    html.Div(
                        dbc.Button('Edit/Delete', href=f'inventory/inventory_profile?mode=edit&id={product_id}', size='sm',
                                    style={'background-color':'#F9FAB9', 'color':'#5D5856', 'border':'0px'}),
                        style={'text-align':'center'}
                    )
                ]
            df['Action']=buttons
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return[table]
        else:
            return ['No records to display']
    else:
        raise PreventUpdate
