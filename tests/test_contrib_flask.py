"""Tests related to the Flask contrib."""
import pytest


pytest.importorskip("flask")
views = pytest.importorskip("flask.views")
contrib = pytest.importorskip("dependencies.contrib.flask")
http_methods = views.http_method_funcs
http_methods_no_head = http_methods - {"head"}


@pytest.fixture()
def app():
    """Create flask application."""
    from flask_project.app import _create_app

    app = _create_app()
    app.config["TESTING"] = True
    return app


@pytest.mark.parametrize("method", http_methods_no_head)
def test_dispatch_request(client, method):
    """Dispatch request to the `Injector` subclass attributes."""
    response = getattr(client, method)("/test_dispatch_request/1/test/")
    assert response.status_code == 200
    assert response.data == b"<h1>OK</h1>"
