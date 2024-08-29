#import dash and selenium libraries
import time
import dash
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from dash import Dash, dcc, html, Input, Output, ctx, ClientsideFunction, callback, State
from dash.exceptions import PreventUpdate
#instantiate and configure the driver options


#start driver and wait
driver = webdriver.Chrome()
time.sleep(5)

# uncomment to activate options
options = Options()
options.add_argument("--headless")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.78 Safari/537.36")
# options.add_argument("--window-size=1980x1020")
# options.add_argument("--log-level=3")

#instantiate the app
app = Dash(external_stylesheets=[
    "https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css",
    "https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css"],
    external_scripts=[
    "https://cdnjs.cloudflare.com/ajax/libs/dash-renderer/1.17.1/dash_renderer.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/dash-renderer/1.17.1/dash_renderer.dev.js"
    ],
    prevent_initial_callbacks=True,
    title='Domain extractor'
)

#UI
app.layout = html.Main(children=[
    html.Div(children=[
        html.H2(children="Domain Name Search"),
        html.H4(children="Use our domain checker tool to find the perfect name for your online project."),
        html.Div(
            className="search",
            children=[
                dcc.Input(
                    id="query",
                    type="text",
                    className="searchTerm",
                    placeholder="What domain are you looking for?",
                ),
            ]),
        html.H4(children="Choose from any of the registrars below"),
        html.Div(
            className="domainButtons",
            children=[
            html.Button('HOSTINGER', id='hostinger-button', n_clicks=0),
            html.Button('NAMECHEAP', id='namecheap-button', n_clicks=0),
            html.Button('WHOIS', id='whois-button', n_clicks=0)
    ], style={'textAlign': 'center', 'padding': '20px'}),
    html.Div(id='domains-table', children=[]),
    html.Button('X', id='quit-button', n_clicks=0, style={'position': 'fixed', 'bottom': '10px', 'right': '10px'})
    ], style={'textAlign':'center', 'padding':'20px'}),
], id='program')

        
@callback(Output('domains-table', 'children', allow_duplicate=True),
    Input('hostinger-button', 'n_clicks'),
    State('query', 'value'), prevent_initial_call=True
)
def search_hostinger(n_clicks, value):
    if n_clicks is None:
        raise PreventUpdate

    # open the hostinger url and wait
    driver.get('https://www.hostinger.com/domain-name-search')
    time.sleep(5)

    #enter the search query and wait
    search_input = driver.find_element(By.ID, 'h-domain-finder-header-input')
    search_input.send_keys(value)
    search_input.send_keys(Keys.RETURN)
    time.sleep(17)

    #extract the domain names and output the result
    domain_result = driver.find_elements(By.CLASS_NAME, 'h-found-domain-cards__domain-result')
    domain_names = [result.find_element(By.CSS_SELECTOR, 'h4 > b').text for result in domain_result]
    return html.Ul([html.Li(name) for name in domain_names], className='domain-list')

    #price_result = driver.find_elements(By.CSS_SELECTOR, "span.h-price__number.t-body-strikethrough")
    #prices = [result.text for result in price_result]


@callback(Output('domains-table', 'children', allow_duplicate=True),
    Input('namecheap-button', 'n_clicks'),
    State('query', 'value'), prevent_initial_call=True
)
def search_namecheap(n_clicks, value):
    if n_clicks is None:
        raise PreventUpdate
    
    #open the namecheap url and wait
    driver.get("https://www.namecheap.com/domains/domain-name-search/")
    time.sleep(5)

    #enter the query and wait
    search_input = driver.find_element(By.CLASS_NAME, "gb-search__field")
    search_input.send_keys(value)
    search_input.send_keys(Keys.RETURN)
    time.sleep(17)

    #extract the domain names and output the results
    domain_results = driver.find_elements(By.CSS_SELECTOR, "div.name > h2")
    domain_names = [result.text for result in domain_results]
    return html.Ul([html.Li(name) for name in domain_names], className='domain-list')


@callback(Output('domains-table', 'children', allow_duplicate=True),
    Input('whois-button', 'n_clicks'),
    State('query', 'value'), prevent_initial_call=True
)
def search_whois(n_clicks, value):
    if n_clicks is None:
        raise PreventUpdate
    
    #open the whois url and wait
    driver.get("https://shop.whois.com/domain-registration/index.php")
    time.sleep(5)
    
    #open the dropdown and untick the .com checkbox 
    com_checkbox = driver.find_element(By.CSS_SELECTOR, "span.tld-select")
    com_checkbox.click()
    com_tick = driver.find_element(By.CSS_SELECTOR, "input#tld_chk_com")
    com_tick.click()

    #enter the query
    search_input = driver.find_element(By.CLASS_NAME, "dom-input")
    search_input.send_keys(value)
    search_input.send_keys(Keys.RETURN)
    time.sleep(17)

    #extract the domain names and output the results
    domain_results = driver.find_elements(By.CSS_SELECTOR, "div.inline-block.dca-domain-name > span")
    domain_names = [result.text for result in domain_results]
    return html.Ul([html.Li(name) for name in domain_names], className='domain-list')

@callback(Output('program', 'children'),
    Input('quit-button', 'n_clicks'),
    prevent_initial_call=True
)
def quit_program(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        driver.quit()
        

# @callback(Output('domains-table', 'children'),
#     Input('hostinger-button', 'n_clicks'),
#     Input('namecheap-button', 'n_clicks'),
#     Input('whois-button', 'n_clicks'),
#     State('query', 'value'), prevent_initial_call=True
# )
# def update_output(hos, nam, who):
#     if ctx.triggered == 'hostinger-button':
#         return search_hostinger()
    
#     elif ctx.triggered == 'namecheap-button':
#         return search_namecheap()
    
#     elif ctx.triggered == 'whois-button':
#         return search_whois()    

if __name__ == "__main__":
    app.run(debug=True)

