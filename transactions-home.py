from dash import html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State

from app1 import app
from apps import dbconnect as db

layout = html.Div(
    [
        html.H2("Transaction"),
        html.Hr(),
        dbc.Card(
            [
                dbc.CardHeader(html.H4("Transaction Details", style={'fontweight':'bold'})),
                dbc.CardBody(
                    [
                        dbc.Button('+ Add Transaction', color="secondary", href='/transaction/transactions_profile?mode=add',
                        style={'background-color':'#5D5856','color':'#f5f8ef','border':'0px'}),
                        html.Hr(),
                        html.Div(
                            [
                                html.H6("Find Records", style={'fontWeight': 'bold'}),
                                dbc.Row(
                                    [
                                        dbc.Label("Search Transaction ID", width=2),
                                        dbc.Col(
                                            dbc.Input(
                                                type="text", id="tran_filter_tranid", placeholder="Enter filter"
                                            ),
                                            width=6,
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                                html.Div(
                                    "No records to show",
                                    id='tran_tranrecords',
                                    style={'text-align':'center'}
                                )
                            ]
                        )
                    ]
                ),
            ]
        )
    ]
)


@app.callback(
    [
        Output('tran_tranrecords', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('tran_filter_tranid', 'value'), # changing the text box value should update the table
    ]
)
def moviehome_loadpolist(pathname, searchterm):
    if pathname == '/transaction':
        
        sql = """ SELECT transac_id, to_char(transac_date, 'DD Mon YYYY'), transac_name
            FROM transactions
            WHERE NOT transac_delete_ind
        """
        values = [] 
        cols = ['Transaction ID', 'Date Created', 'Customer Name']
        
        
        # Filter
        if searchterm:
            sql += """AND (transac_name ILIKE %s) OR CAST(transac_id as VARCHAR(10)) ILIKE %s OR CAST(to_char(transac_date, 'DD Mon YYYY') as VARCHAR(20)) ILIKE %s"""

            values += [f"%{searchterm}%", searchterm, f"%{searchterm}%"]
        df = db.querydatafromdatabase(sql,values,cols)
        
        if df.shape: 
            
            # Create the buttons as a list based on the ID
            buttons = []
            for transac_id in df['Transaction ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Edit', href=f'transaction/transactions_profile?mode=edit&id={transac_id}',
                                   size='sm', style={'background-color':'#F9FAB9', 'color':'#5D5856', 'border':'0px'}),
                        style={'text-align': 'center'}
                    )
                ]
            
            df['Action'] = buttons
            
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                    hover=True, size='sm')
            return [table]
        else:
            return ["No records to show"]
        
    else:
        raise PreventUpdate
