from dash import html
import dash_bootstrap_components as dbc
from app1 import app

facebook = dbc.Card(
    [
        dbc.CardImg(src=app.get_asset_url('fb.png'), top=True, style={'padding-top':'4em', 'padding-left':'4em', 'padding-right':'4em'}),
        dbc.CardBody(
            [
                dbc.Button(
                    "Facebook",
                    href="https://www.facebook.com/officialkmpph",
                ),
            ]
        ),
    ],
    style={"width": "15rem"}, 
)

shopee = dbc.Card(
    [
        dbc.CardImg(src=app.get_asset_url('shopee.png'), top=True, style={'padding-top':'4em', 'padding-left':'4em', 'padding-right':'4em'}),
        dbc.CardBody(
            [
                dbc.Button(
                    "Shopee",
                    href="Shopee.ph/officialkmpversion2.0",
                ),
            ]
        ),
    ],
    style={"width": "15rem"}, 
)

layout = html.Div(
    [
        html.Br(),
        html.H2('About the Company'),
        html.Hr(),
        html.Div(
            [
                html.Span(
                    "KMP Motorcycle Parts is a micro-retail and wholesale trade enterprise based in Marilao, Bulacan, which sells various motorcycle and scooter parts and accessories in both retail and wholesale. Ms. Aleli Garcia, the shop owner, shared that she ventured into this business because she had to assist her husband. However, when they got separated, her husband left the business for her to manage on her own. Right now, she handles almost all of the admin work while her 3 employees — 1 Manager, and 2 regular employees — help her with the whole business.",
                ),
                html.Br(),
                html.Br(),
                html.Span(
                    "Contact the owner if you need assistance!",
                    style={'font-style':'italic'}
                ),
            ]
        ),
        html.Br(),
        html.Br(),
        html.H4('Brands'),
        html.Hr(),
        html.Div(
            dbc.ListGroup(
                [
                    dbc.ListGroupItem("100% AKRAPOVIC"),
                    dbc.ListGroupItem("BATTERY TENDER"),
                    dbc.ListGroupItem("DAINESE"),
                    dbc.ListGroupItem("GIVI"),
                    dbc.ListGroupItem("INTUITIVE CUBE"),
                    dbc.ListGroupItem("KAPPA"),
                    dbc.ListGroupItem("KOMINE"),
                    dbc.ListGroupItem("NOCO"),
                    dbc.ListGroupItem("OXFORD"),
                    dbc.ListGroupItem("POLISPORT"),
                    dbc.ListGroupItem("RIZOMA"),
                    dbc.ListGroupItem("SENA"),
                ],
                flush=True,
            )
        ),
        html.Br(),
        html.Br(),
        html.H4('Also Available In'),
        html.Hr(),
        html.Div(
            [
                dbc.Navbar(
                    [
                        html.A(
                            dbc.Row(
                                [
                                    dbc.Col([
                                        html.Img(src=app.get_asset_url('Facebook.png'), height='45px'),
                                    ]),
                                ],
                                align="center",
                                className='g-0',
                            ),
                            href="https://www.facebook.com/officialkmpph",
                            style={'textDecoration': 'none', 'padding-left':'1em', 'padding-right':'2em', 'color':'#F5F8EF','font-style':'bold'},
                        ),
                        html.A(
                            dbc.Row(
                                [
                                    dbc.Col([
                                        html.Img(src=app.get_asset_url('shopee.png'), height='45px'),
                                    ]),
                                ],
                                align="center",
                                className='g-0',
                            ),
                            href="https://shopee.ph/officialkmpversion2.0?fbclid=IwAR1jRaY3hHoq4IHbo90KRR2q6VYRCB0eUSY6N3zUAF-Xvx156hnbN-N1wc0",
                            style={'textDecoration': 'none', 'padding-left':'1em', 'padding-right':'2em', 'color':'#F5F8EF','font-style':'bold'},
                        ),
                    ]
                ),
            ]
        ),
    ]
)
