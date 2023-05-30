from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
from urllib.parse import urlparse, parse_qs
from dash.dash_table.Format import Group

from app1 import app
from apps import dbconnect as db

layout = html.Div(
    [
        html.Div( 
            [
            dcc.Store(id='invprof_toload', storage_type='memory', data=0),
            ]
        ),
        html.H2('Product Details'),
        html.Hr(),
        dbc.Row(
            [
                dbc.Label("Product or SKU Description", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", #change to number/bool for others !
                        id="invprof_name",
                        placeholder="Enter product name",
                    ),
                    width=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Brand", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text",
                        id="invprof_brand",
                        placeholder="Enter product brand",
                    ),
                    width=6,
                ),
            ],
            
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Compatibility", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text",
                        id="invprof_comp",
                        placeholder="Enter product compatibility",
                    ),
                    width=5,
                ),
            ],
            className="mb-3"
        ),
        dbc.Row(
            [
                dbc.Label("Stock on Hand", width=2),
                dbc.Col(
                    dbc.Input(
                        type="integer",
                        id="invprof_stockonhand",
                        placeholder="Enter amount of stock on hand",
                    ),
                    width=5,
                ),
            ],
            className="mb-3"
        ),
        dbc.Row(
            [
                dbc.Label("Stock ROP", width=2),
                dbc.Col(
                    dbc.Input(
                        type="integer",
                        id="invprof_stockrop",
                        placeholder="Enter amount of stock reorder point",
                    ),
                    width=5,
                ),
            ],
            className="mb-3"
        ),
        dbc.Row(
            [
                dbc.Label("Stock Backorder", width=2),
                dbc.Col(
                    dbc.Input(
                        type="integer",
                        id="invprof_stockbackorder",
                        placeholder="Enter amount of backorder stock",
                    ),
                    width=5,
                ),
            ],
            className="mb-3"
        ),
        dbc.Row(
            [
                dbc.Label("Cost", width=2),
                dbc.Col(
                    dbc.Input(
                        type="float",
                        id="invprof_cost",
                        placeholder="Enter cost per item",
                    ),
                    width=5,
                ),
            ],
            className="mb-3"
        ),
        dbc.Row(
            [
                dbc.Label("Selling Price", width=2),
                dbc.Col(
                    dbc.Input(
                        type="float",
                        id="invprof_sellingprice",
                        placeholder="Enter selling price per item",
                    ),
                    width=5,
                ),
            ],
            className="mb-3"
        ),
        html.Div(
                dbc.Row(
                [
                    dbc.Label("Wish to delete?", width=2),
                    dbc.Col(
                        dbc.Checklist(
                            id='invprof_removerecord',
                            options=[
                                {
                                    'label': "Mark for Deletion",
                                    'value': 1
                                }
                            ],
                            # I want the label to be bold
                            style={'fontWeight':'bold'},
                        ),
                        width=6,
                    ),
                ],
                className="mb-3",
            ),
            id='invprof_removerecord_div'
        ),
        dbc.Button('Submit', id = 'invprof_submit', 
                    style={'background-color':'#5D5856','color': '#f5f8ef', 'border':'0px'}),
        dbc.Modal(
            [
                dbc.ModalHeader("Saving Progress", id='invprof_feedback_header'),
                dbc.ModalBody("tempmessage", id ='invprof_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", id="invprof_closebutton", className="ms-auto", n_clicks=0,
                        style={'background-color':'#5D5856','color': '#f5f8ef', 'border':'0px'}
                    ),
                ),
            ],
            id = "invprof_successmodal",
            is_open=False,
        )
    ]
)

@app.callback(
    [
        Output('invprof_toload', 'data'),
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('url', 'search')
    ]
)

def to_load(pathname, search):
    if pathname == '/inventory/inventory_profile':

        parsed = urlparse(search)
        mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if mode == 'edit' else 0

    else:
        raise PreventUpdate

    return[to_load]


@app.callback(
    [
        Output('invprof_successmodal', 'is_open'),
        Output('invprof_feedback_header', 'children'),
        Output('invprof_feedback_message', 'children'),
        Output('invprof_closebutton', 'href'),
        #Output('invprof_toload', 'data'),
        
    ],
    [
        #Input('url', 'pathname'),
        Input('invprof_submit', 'n_clicks'),
        Input('invprof_closebutton', 'n_clicks'),
        #Input('invprof_toload', 'modified_timestamp')
    ],
    [
        State('invprof_name','value'),
        State('invprof_brand', 'value'),
        State('invprof_comp', 'value'),
        State('invprof_stockonhand', 'value'),
        State('invprof_stockrop','value'),
        State('invprof_stockbackorder','value'),
        State('invprof_cost','value'),
        State('invprof_sellingprice','value'),
        #State('invprof_status','value'),
        #State('invprofile_toload', 'data'),
        State('url', 'search'),
        State('invprof_removerecord', 'value')
    ]
)

def invprofile_saveprofile(submitbtn, closebutton, product, brand, compatibility, 
                            stockonhand, stockrop, stockbackorder, cost, sellingprice, 
                            search, removerecord):

    ctx=dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        modal_open = False
        header = ''
        feedbackmessage = ''
        okay_href = None
    else:
        raise PreventUpdate

    if eventid == 'invprof_submit' and submitbtn:
        modal_open = True

        # We need to check inputs
        inputs = [
            product,
            brand,
            compatibility,
            stockonhand, 
            stockrop, 
            stockbackorder, 
            cost, 
            sellingprice, 
        ]

                #if erroneous inputs, raise prompt
        if not all(inputs):
            header = 'Incomplete data'
            feedbackmessage = 'Please supply all inputs.'
        elif len(product)>256:
            feedbackmessage = "Product name is too long (length>256)."

        else: # all inputs are valid
        # Add the data into the db
            #removed stock_on_hand:
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]

            if mode == 'add':
                sql = """
                    INSERT INTO inventory (
                        prod_name, 
                        prod_brand, 
                        prod_compatibility,
                        stock_onhand,
                        stock_rop,
                        stock_backorder,
                        cost,
                        sell_price,
                        prod_delete_ind
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """

                values = [product, brand, compatibility, stockonhand, stockrop, stockbackorder, cost, sellingprice, False]
                db.modifydatabase(sql, values)
                header = 'Save Success'
                feedbackmessage = "Product has been saved!"
                okay_href = "/inventory"
            
            elif mode =='edit':
                parsed = urlparse(search)
                invid = parse_qs(parsed.query)['id'][0]
                sqlcode = """ UPDATE inventory
                SET
                    prod_name = %s,
                    prod_brand = %s, 
                    prod_compatibility = %s,
                    stock_onhand = %s,
                    stock_rop = %s,
                    stock_backorder = %s,
                    cost = %s,
                    sell_price = %s,
                    prod_delete_ind = %s
                WHERE
                    prod_id = %s
                """
                to_delete = bool(removerecord)

                values = [product, brand, compatibility, stockonhand, stockrop, stockbackorder, cost, sellingprice,
                            to_delete, invid]
                
                db.modifydatabase(sqlcode, values)
                header = 'Update Success'
                feedbackmessage = "Product list has been updated."
                okay_href = '/inventory'

            else:
                raise PreventUpdate
    
    elif eventid == "invprof_closebutton" and closebutton:
        pass
 
    else: # Callback was not triggered by desired triggers
        raise PreventUpdate

    return[modal_open, header, feedbackmessage, okay_href]

@app.callback(
    [
        Output('invprof_name', 'value'),
        Output('invprof_brand', 'value'),
        Output('invprof_comp', 'value'),
        Output('invprof_stockonhand', 'value'),
        Output('invprof_stockrop', 'value'),
        Output('invprof_stockbackorder', 'value'),
        Output('invprof_cost', 'value'),
        Output('invprof_sellingprice', 'value'),
    ],
    [
        Input('invprof_toload', 'modified_timestamp'),
    ],
    [
        State('invprof_toload', 'data'),
        State('url', 'search'),
    ]
)

def loaddetails(timestamp, to_load, search):
    if to_load:
        sqlcode = """SELECT 
                        prod_name, 
                        prod_brand, 
                        prod_compatibility,
                        stock_onhand,
                        stock_rop,
                        stock_backorder,
                        cost,
                        sell_price
                FROM inventory
                WHERE prod_id = %s"""

        parsed = urlparse(search)
        invid = parse_qs(parsed.query)['id'][0]

        val = [invid]
        colnames = ['name', 'brand', 'compatibility', 'onhand', 'rop', 'backorder', 'cost', 'price']

        df = db.querydatafromdatabase(sqlcode, val, colnames)

        name = df['name'][0]
        brand = df['brand'][0]
        compatibility = df['compatibility'][0]
        onhand = df['onhand'][0]
        rop = df['rop'][0]
        backorder = df['backorder'][0]
        cost = df['cost'][0]
        price = df['price'][0]

        return [name, brand, compatibility, onhand, rop, backorder, cost, price]

    else:
        raise PreventUpdate
