import pytest
from dash import Dash
from dash.testing.application_runners import import_app
import dash.testing as dt

# test dash app
@pytest.fixture
def app():
    app = import_app("app")
    return app

def test_custom_html_template(app):
    # test that custom HTML template and meta tags are rendered correctly
    
    app.layout = app.layout
    
    with app.server.test_client() as client:
        response = client.get('/')
        
        # Check for the presence of custom HTML links or metadata
        assert b'<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css">' in response.data
        assert b'<link rel="icon" href="/assets/logos/favicon.svg" type="image/x-icon">' in response.data
        assert b'@import url(\'https://fonts.googleapis.com/css2?family=Inter:wght@100;400;700&display=swap\');' in response.data
