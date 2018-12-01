from django.test import TestCase, tag
from django.urls import reverse
from django.template import Context, Template

@tag('core')
class UrlReplace(TestCase):
    
    def setUp(self):
        self.resp = self.client.get(reverse('navigation_frontpage')) #Get a valid request object to mutate
        new_context = self.resp.context['request'].GET.copy() #Copy to disable the unmutable flag
        new_context['search'] = 'test' 
        self.resp.context['request'].GET = new_context #Change the GET dict to the new one
        context = Context({'request': self.resp.context['request']})     
        template_to_render = Template("{% load url_replace %} {% url_replace page='2' %}")
        self.rendered = template_to_render.render(context) 
        
    def test_url(self): 
        self.assertIn('search=test&amp;page=2', self.rendered)
