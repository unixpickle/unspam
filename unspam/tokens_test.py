from .tokens import tokens


def test_tokens_basic():
    assert tokens('hi  there') == ['hi', 'there']
    assert tokens('"hi"--there') == ['hi', 'there']
    assert tokens('“hi“--there') == ['hi', 'there']
    assert tokens('“hi“--therehttp://google.com hey') == ['hi', 'there', 'URL', 'hey']
