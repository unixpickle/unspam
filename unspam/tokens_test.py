from .tokens import tokens


def test_tokens_basic():
    assert tokens('hi  there') == ['hi', 'there']
    assert tokens('"hi"--there') == ['hi', 'there']
    assert tokens('“hi“--there') == ['hi', 'there']
    assert tokens('“hi“--therehttp://google.com hey') == ['hi', 'there', 'URL', 'hey']
    assert tokens('meet me on 3/5/2018') == ['meet', 'me', 'on', 'NUM', 'NUM', 'NUM']
