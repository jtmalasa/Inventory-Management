import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from apps.products import products_home
from apps import home
from app1 import app

navlink_style = {
    'color': 'black',
    'padding-right':'5em',
    'font-weight':'bold',
}

#for editing of links:
navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col([
                        html.Img(src=app.get_asset_url('KMP.png'), height='45px'),
                        dbc.NavbarBrand("KMP Inventory Management System", className="ms-2", style={'padding-right':'6em'}),
                    ]),
                ],
                align="center",
                className='g-0',
            ),
            href="/home",
            style={'textDecoration': 'none', 'padding-left':'1em', 'padding-right':'2em', 'color':'#F5F8EF','font-style':'bold'},
        ),
        html.Br(),        
    ],
    dark=True,
    color='#BD904E',
)

navbar2 = dbc.Navbar(
    [
        dbc.NavLink("About Us", href="/home", style=navlink_style),
        dbc.NavLink("Products", href="/products", style=navlink_style),
        dbc.NavLink("Inventory", href="/inventory", style=navlink_style),
        dbc.NavLink("Transaction", href="/transaction", style=navlink_style),
        dbc.NavLink("Support", href="support", style=navlink_style),
        dbc.NavLink("Log-In", href="login", style=navlink_style),
    ],
    color = '#e59b93',
    className='d-flex justify-content-between',
    style={'flex': '1', 'padding-left':'4em'}
)

navbar3 = dbc.Navbar(
    [
        dbc.NavLink("About Us", href="/home", style=navlink_style),
        dbc.NavLink("Products", href="/products", style=navlink_style),
        dbc.NavLink("Inventory", href="/inventory", style=navlink_style),
        dbc.NavLink("Transaction", href="/transaction", style=navlink_style),
        dbc.NavLink("Support", href="support", style=navlink_style),
        dbc.NavLink("Log-Out", href="logout", style=navlink_style),
    ],
    color = '#e59b93',
    className='d-flex justify-content-between',
    style={'flex': '1', 'padding-left':'4em'}
)
