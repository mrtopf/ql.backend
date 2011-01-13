from quantumlounge.framework.decorators import json, html

def test_html_decorator():
    
    @html
    def fu():
        return "foobar"
        
    res = fu()
    assert res.headers['Content-Type'] == "text/html"
    assert res.data == """foobar"""


def test_json_decorator():
    
    @json()
    def fu(a,b):
        d={
            'a' : a,
            'b' : b
        }
        return d
        
    res = fu(3,4)
    assert res.headers['Content-Type'] == "application/json"
    assert res.data == """{"a": 3, "b": 4}"""
    
def test_json_method_decorator():
    
    class A:
        
        c=17
        
        @json()
        def get(self, a,b):
            return {'a': a, 'b': b, 'c': self.c}
            
    a = A()
    res = a.get(3,4)
    assert res.headers['Content-Type'] == "application/json"
    assert res.data == """{"a": 3, "c": 17, "b": 4}"""
    
