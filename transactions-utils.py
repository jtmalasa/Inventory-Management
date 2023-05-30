from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State, ALL
import pandas as pd
from urllib.parse import urlparse, parse_qs
from datetime import date
import json

from app1 import app
from apps import dbconnect as db
from apps.transaction import transactions_utils as util

layout = html.Div(
    [
        html.Div( # This div shall contain all dcc.Store objects
            [
                # if edit mode, this gets a value of 1, else 0
                dcc.Store(id='tranprof_toload', storage_type='memory', data=0),
                
                # this gets the po_id 
                dcc.Store(id='tranprof_tranid', storage_type='memory', data=0),
                
                # this gets the po_item_id to edit
                dcc.Store(id='tranprof_linetoedit', storage_type='memory', data=0),
            ]
        ),

        html.H2("Transaction Details"),
        html.Hr(),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Label("Transaction Date", width=2),
                        dbc.Col(
                            dcc.DatePickerSingle(
                                id='tranprof_transactiondate',
                                date=date.today()
                            ),
                            width=6,
                        ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("Customer Name", width=2),
                        dbc.Col(
                            dbc.Input(
                                type="text",
                                className="mb-3",
                                placeholder="Add Customer Name",
                                id='tranprof_name'
                            ),
                            width=6,
                        ),
                    ],
                    className="mb-3",
                ),
            ]    
        ),
        
        html.Hr(),
        
        # We don't need a div here but I like using one
        # to signify a new section
        html.Div(
            [
                dbc.Alert("Please fill out the information above before proceeding", id='tranprof_alertmissingdata',
                          color='danger', is_open=False),
                dbc.Button("Add Line Item", id="tranprof_addlinebtn", 
                            className="ms-auto", n_clicks=0,
                           style={'background-color':'#5D5856','color': '#f5f8ef', 'display':'inline-block','border-radius':'5px', 'border':'0px'}
                ),  
                html.Br(),
                html.Br(),
                html.Div(
                    # This will contain the table of line items
                    id='tranprof_lineitems',
                    style = {'text-align': 'center'}
                )
            ]    
        ),
        
        dbc.Modal(
            [
                dbc.ModalHeader("Add Line Item", id='tranprof_linemodalhead'),
                dbc.ModalBody(
                    [
                        dbc.Alert(id='tranprof_linealert', color='warning', is_open=False),
                        dbc.Row(
                            [
                                dbc.Label("Item", width=4, id='itemhead'),
                                dbc.Col(
                                    html.Div(
                                        dcc.Dropdown(
                                            id='tranprof_lineitem',
                                            clearable=True,
                                            searchable=True,
                                            options=[]
                                        ), 
                                        className="dash-bootstrap"
                                    ),
                                    width=6,
                                    id='itemcol'
                                ),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Label("Qty", width=4, id='qtyhead'),
                                dbc.Col(
                                    dbc.Input(
                                        type="number", id="tranprof_lineqty", placeholder="Enter qty"
                                    ),
                                    width=6,
                                    id='qtycol'
                                ),
                            ],
                            className="mb-3",
                        ),
                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Label("Are you sure you want to Delete?", width=4),
                                    dbc.Col(
                                        dbc.Checklist(
                                            id='tranprof_lineremove',
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
                                        style={'margin': 'auto 0'}
                                    ),
                                ],
                                className="mb-3",
                            ),
                            id='tranprof_lineremove_div'
                        ),
                    ]
                ),
                dbc.ModalFooter(
                    [
                        html.Div(
                            [
                                dbc.Button('Cancel', id='tranprof_cancellinebtn',
                                           style={'background-color':'#E59B93','color': '#f5f8ef', 'border':'0px'}),
                                dbc.Button('Save Line Item', id='tranprof_savelinebtn',className="ms-auto",
                                           style={'background-color':'#5d5856','color': '#f5f8ef', 'border':'0px'}),
                            ],
                            # these are to separate the buttons to opposite ends
                            className='d-flex justify-content-between',
                            style={'flex': '1'}
                        )
                    ]
                )
            ],
            id='tranprof_modal',
            backdrop='static',
            centered=True
        ),
        
        # enclosing the checklist in a Div so we can
        # hide it in Add Mode
        html.Div(
            dbc.Row(
                [
                    dbc.Label("", width=2),
                    dbc.Col(
                        dbc.Checklist(
                            id='tranprof_removerecord',
                            options=[
                                {
                                    'label': "Mark for Deletion",
                                    'value': 1
                                }
                            ],
                            # I want the label to be bold
                            style={'display':'none'}, 
                        ),
                        width=6,
                        style={'margin': 'auto 0'}
                    ),
                ],
                className="mb-3",
            ),
            id='tranprof_removerecord_div'
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Saving Progress")),
                dbc.ModalBody("tempmessage", id='tranprof_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", id="tranprof_closebtn", className="ms-auto", n_clicks=0,
                        style={'background-color':'#5D5856','color': '#f5f8ef', 'border':'0px'}
                    )
                ),
            ],
            id="tranprof_modalsubmitted",
            is_open=False,
        ),
        html.Hr(),
        
        html.Div(
            [
                dbc.Button('Cancel', id='tranprof_cancelbtn',
                          style={'background-color':'#E59B93','color': '#f5f8ef', 'border':'0px'}),
                dbc.Button('Submit', color="primary", id='tranprof_savebtn',
                          style={'background-color':'#5D5856','color': '#f5f8ef', 'border':'0px'}),
            ],
            # these are to separate the buttons to opposite ends
            className='d-flex justify-content-between',
            style={'flex': '1'}
        )
    ]
)

@app.callback(
    [
        Output('tranprof_toload', 'data'),
        # we want to update the style of this element
        #Output('tranprof_removerecord_div', 'style'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search') 
    ]
)
def pageLoadOperations(pathname, search):
    
    if pathname == '/transaction/transactions_profile':
                
        # are we on add or edit mode?
        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0
        
        # to show the remove option?

       # removediv_style = {'display': 'none'} if not to_load else None
        # if to_load = 0, then not to_load -> not 0 -> not False -> True
    
    else:
        raise PreventUpdate

    return [to_load]


@app.callback(
    [
        Output('tranprof_transactiondate', 'date'),
        Output('tranprof_name', 'value'),
    ],
    [
        Input('tranprof_toload', 'modified_timestamp'),
        # toload is a dcc.store element. To use them in Input(), 
        # property should be 'modified_timestamp'
    ],
    [
        State('tranprof_toload', 'data'),
        State('url', 'search') 
    ]
)
def populatePOData(timestamp, toload, search):
    if toload == 1:
        
        parsed = urlparse(search)
        transac_id = int(parse_qs(parsed.query)['id'][0])
        
        sql = """SELECT transac_date, transac_name
        FROM transactions
        WHERE transac_id = %s"""
        val = [transac_id]
        col = ['date', 'remarks']
        
        df = db.querydatafromdatabase(sql, val, col)
        
        transactiondate, remarks = [df[i][0] for i in col]
        
    else:
        raise PreventUpdate
    
    return [transactiondate, remarks]


@app.callback(
    [
        Output('tranprof_modal', 'is_open'),
        Output('tranprof_alertmissingdata', 'is_open'),
        Output('tranprof_lineremove_div', 'className'),
        Output('tranprof_tranid', 'data'),
        
        Output('tranprof_lineitem', 'options'),
        Output('tranprof_linealert', 'children'),
        Output('tranprof_linealert', 'is_open'),
        Output('tranprof_linetoedit', 'data'),
        
        Output('tranprof_lineitems', 'children'),
        Output('tranprof_linemodalhead', 'children'),
        Output('tranprof_savelinebtn', 'children'),

        Output('itemcol', 'style'),
        Output('qtycol', 'style'),
        Output('itemhead', 'style'),
        Output('qtyhead', 'style'),
    ],
    [
        Input('tranprof_addlinebtn', 'n_clicks'),
        Input('tranprof_savelinebtn', 'n_clicks'),
        Input('tranprof_cancellinebtn', 'n_clicks'),
        Input({'index': ALL, 'type': 'tranprof_editlinebtn'}, 'n_clicks'),
        
        Input('tranprof_toload', 'modified_timestamp'),
        
    ],
    [
        State('url', 'search'),
        State('tranprof_transactiondate', 'date'),
        State('tranprof_name', 'value'),
        State('tranprof_tranid', 'data'),
        
        State('tranprof_lineitem', 'options'),
        State('tranprof_lineitem', 'value'),
        State('tranprof_lineqty', 'value'),
        State('tranprof_linetoedit', 'data'),
        
        State('tranprof_lineremove', 'value'),
        State('tranprof_lineitems', 'children'),
        State('tranprof_toload', 'data'),
        State('tranprof_linemodalhead', 'children'),
        
        State('tranprof_savelinebtn', 'children'),
    ]
)
def toggleModal(addlinebtn, savebtn, cancelbtn, editlinebtn,
                toload_timestamp,
                
                search, transactiondate, remarks, transac_id,
                item_options, itemid, itemqty, linetoedit,
                removeitem, linetable, toload, linemodalhead,
                addlinebtntxt):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        parsed = urlparse(search)
        
        # some default values
        openmodal = False
        openalert_missingdata = False
        lineremove_class = 'd-none' # hide the remove tickbox
        
        linealert_message = ''
        updatetable = False # for updating table of line items
        itemcol = {'display':'unset'}
        qtycol = {'display':'unset'}
        itemhead = {'display':'unset'}
        qtyhead = {'display':'unset'}
    else:
        raise PreventUpdate
    
    PO_requireddata = [
        transactiondate, 
        remarks
    ]
    
    if eventid == 'tranprof_addlinebtn' and addlinebtn and all(PO_requireddata):
        openmodal = True
        item_options = util.getItemDropdown('add', transac_id)
        linetoedit = 0
        
        # Edit modal text (buttons, headers)
        linemodalhead = 'Add Line Item'
        addlinebtntxt = 'Save Line Item'
    
    elif eventid == 'tranprof_addlinebtn' and addlinebtn and not all(PO_requireddata):
        openalert_missingdata = True
        
    elif eventid == 'tranprof_cancellinebtn' and cancelbtn:
        pass
    
    elif 'tranprof_editlinebtn' in eventid and any(editlinebtn):
        # if any of the buttons for editing si clicked
        itemcol = {'display':'none'}
        qtycol = {'display':'none'}
        itemhead = {'display':'none'}
        qtyhead = {'display':'none'}
        openmodal = True
        lineremove_class = '' # show line remove option
        linetoedit = int(json.loads(eventid)['index'])
        item_options = util.getItemDropdown('edit', transac_id)
        
        # Edit modal text (buttons, headers)
        linemodalhead = 'Edit Line Item'
        addlinebtntxt = 'Update Line Item'
        
        
    elif eventid == 'tranprof_toload' and toload == 1:
        updatetable = True
        transac_id = int(parse_qs(parsed.query)['id'][0])
    
        
    elif eventid == 'tranprof_savelinebtn' and savebtn:
        # validate inputs
        inputs = [
            itemid, 
            util.converttoint(itemqty)>0
        ]
        
        if not all(inputs):
            linealert_message = "Please ensure that fields are filled in and inputs are correct."
        
        else:
            # proceed to saving the line item
            
            newline = {
                'itemid': itemid,
                'itemqty': int(itemqty),
            }
            
            # if add mode:
            if linetoedit == 0:
                # if PO record not yet in db, save PO first
                if not transac_id:
                    transac_id = util.createPOrecord(transactiondate, remarks)
                
                util.managePOLineItem(transac_id, newline)
            
            else:
                if removeitem:
                    util.removeLineItem(linetoedit, transac_id, itemid)
                else:
                    util.managePOLineItem(transac_id, newline)
            
            updatetable = True
    
    else:
        raise PreventUpdate
    
    
    if updatetable:
        df = util.queryPOLineItems(transac_id)
        
        if df.shape[0]:
            linetable = util.formatPOtable(df)
        else:
            linetable = html.Div('No records to display', style={'color':'#777', 'padding-left': '2em'})

    # if we have an error prompt, linealert should open
    openalert_linealert = bool(linealert_message)
    
    return [
        openmodal, 
        openalert_missingdata, 
        lineremove_class,
        transac_id,
        
        item_options,
        linealert_message,
        openalert_linealert,
        linetoedit,
        
        linetable,
        linemodalhead,
        addlinebtntxt,

        itemcol,
        qtycol,
        itemhead,
        qtyhead
    ]


@app.callback(
    [
        Output('tranprof_lineitem', 'value'),
        Output('tranprof_lineqty', 'value'),
        Output('tranprof_lineremove', 'value'),
    ],
    [
        Input('tranprof_addlinebtn', 'n_clicks'),
        Input('tranprof_linetoedit', 'modified_timestamp'),
    ],
    [
        State('tranprof_linetoedit', 'data'),
        State('tranprof_lineitem', 'value'),
        State('tranprof_lineqty', 'value'),
        State('tranprof_lineremove', 'value'),
    ]
)
def clearFields(addlinebtn, line_timestamp, 
                
                linetoedit, itemid, itemqty, removeitem):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    else:
        raise PreventUpdate
    
    
    if eventid == 'tranprof_addlinebtn' and addlinebtn:
        itemid, itemqty = None, None
        removeitem = []
        
    elif eventid == 'tranprof_linetoedit' and linetoedit:
        itemid, itemqty = util.getPOLineData(linetoedit)
        removeitem = []
        
    else:
        raise PreventUpdate
    
    return [itemid, itemqty, removeitem]


@app.callback(
    [
        Output('tranprof_modalsubmitted', 'is_open'),
        Output('tranprof_feedback_message', 'children'),
        Output('tranprof_closebtn', 'href'),
    ],
    [
        Input('tranprof_savebtn', 'n_clicks'),
        Input('tranprof_cancelbtn', 'n_clicks'),
        Input('tranprof_closebtn', 'n_clicks'),
    ],
    [
        State('tranprof_tranid', 'data'),
        State('tranprof_removerecord', 'value'),
        State('tranprof_toload', 'data') 
    ]
)
def finishTransaction(submitbtn, cancelbtn, closebtn,                      
                      transac_id, removerecord, iseditmode):
    ctx = dash.callback_context
    if ctx.triggered:
        # eventid = name of the element that caused the trigger
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False
        feedbackmessage = ''
        okay_href = None
    else:
        raise PreventUpdate
    
    if eventid == 'tranprof_savebtn' and submitbtn:
        openmodal = True
        
        # check if we have line items
        if not transac_id:
            feedbackmessage = "You have not filled out the form."
            okay_href = '/transaction'
            
        elif not util.checkPOLineItems(transac_id):
            feedbackmessage = "Please add line items. If you want to exit press Okay"
            okay_href = '/transaction'

        # elif removerecord:
        #     util.deletePO(transac_id)
        #     feedbackmessage = "Record has been deleted. Click Okay to go back to Transaction Home."
        #     okay_href = '/transaction'
            
        else:
            feedbackmessage = "Transaction is saved. Click Okay to go back to Transaction Home."
            okay_href = '/transaction'
            
    elif eventid == 'tranprof_cancelbtn' and cancelbtn:
        openmodal = True
        
        if not transac_id:
            feedbackmessage = "Click Okay to go back to Transaction Home."
            okay_href = '/transaction'
        elif iseditmode and transac_id:
            feedbackmessage = "Changes have been discarded. Click Okay to go back to Transaction Home."
            okay_href = '/transaction'
        else:
            feedbackmessage = "Click Okay to go back to Transaction Home."
            okay_href = '/transaction'
            
    
    elif eventid == 'tranprof_closebtn' and closebtn:
        pass
    
    else:
        raise PreventUpdate
    
    return [openmodal, feedbackmessage, okay_href]
