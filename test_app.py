from dash.testing.application_runners import import_app


def test_header_is_present(dash_duo):
    app = import_app("app")
    dash_duo.start_server(app)

    # Wait for the header to appear, then check its text
    dash_duo.wait_for_element("#header", timeout=10)
    header = dash_duo.find_element("#header")
    assert header.text == "Soul Foods — Pink Morsel Sales Visualiser"


def test_visualisation_is_present(dash_duo):
    app = import_app("app")
    dash_duo.start_server(app)

    # The line chart should render
    dash_duo.wait_for_element("#sales-line-chart", timeout=10)
    assert dash_duo.find_element("#sales-line-chart") is not None


def test_region_picker_is_present(dash_duo):
    app = import_app("app")
    dash_duo.start_server(app)

    # The radio buttons should render
    dash_duo.wait_for_element("#region-filter", timeout=10)
    assert dash_duo.find_element("#region-filter") is not None