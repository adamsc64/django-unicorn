import pytest
from bs4 import BeautifulSoup

from django_unicorn.components.unicorn_template_response import (
    UnicornTemplateResponse,
    get_root_element,
)


def test_get_root_element():
    expected = "<div>test</div>"

    component_html = "<div>test</div>"
    soup = BeautifulSoup(component_html, features="html.parser")
    actual = get_root_element(soup)

    assert str(actual) == expected


def test_get_root_element_with_comment():
    expected = "<div>test</div>"

    component_html = "<!-- some comment --><div>test</div>"
    soup = BeautifulSoup(component_html, features="html.parser")
    actual = get_root_element(soup)

    assert str(actual) == expected


def test_get_root_element_with_blank_string():
    expected = "<div>test</div>"

    component_html = "\n<div>test</div>"
    soup = BeautifulSoup(component_html, features="html.parser")
    actual = get_root_element(soup)

    assert str(actual) == expected


def test_get_root_element_no_element():
    expected = "<div>test</div>"

    component_html = "\n"
    soup = BeautifulSoup(component_html, features="html.parser")

    with pytest.raises(Exception):
        actual = get_root_element(soup)

        assert str(actual) == expected


def test_desoupify():
    html = "<div>&lt;a&gt;&lt;style&gt;@keyframes x{}&lt;/style&gt;&lt;a style=&quot;animation-name:x&quot; onanimationend=&quot;alert(1)&quot;&gt;&lt;/a&gt;!\n</div>\n\n<script type=\"application/javascript\">\n  window.addEventListener('DOMContentLoaded', (event) => {\n    Unicorn.addEventListener('updated', (component) => console.log('got updated', component));\n  });\n</script>"
    expected = "<div>&lt;a&gt;&lt;style&gt;@keyframes x{}&lt;/style&gt;&lt;a style=\"animation-name:x\" onanimationend=\"alert(1)\"&gt;&lt;/a&gt;!\n</div>\n<script type=\"application/javascript\">\n  window.addEventListener('DOMContentLoaded', (event) => {\n    Unicorn.addEventListener('updated', (component) => console.log('got updated', component));\n  });\n</script>"

    soup = BeautifulSoup(html, "html.parser")

    actual = UnicornTemplateResponse._desoupify(soup)

    assert expected == actual