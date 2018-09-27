from django.test import TestCase, tag
from django.template import Context, Template
from seed.factories import ThreadFactory, UserPostFactory, ModeratorFactory

class ThreadFormat(TestCase):

    def setUp(self):
        embed_link = 'http://www.youtube.com/watch?v=dQw4w9WgXcQ'
        self.embed_code = 'dQw4w9WgXcQ' #The embed_video template tag will transform the url so the unique part must be used to check if the embed is displayed
        self.thread = ThreadFactory(embed=embed_link)
        context = Context({'thread': self.thread, 
            'moderation_view': False})
        template_to_render = Template('{% load imageboard_objects %} {% thread_format thread %}')
        self.rendered = template_to_render.render(context)
            

    def test_subject(self):
        self.assertIn(self.thread.subject, self.rendered)

    def test_name(self):
        self.assertIn(self.thread.name, self.rendered)

    def test_report(self):
        self.assertIn(self.thread.get_report_url(), self.rendered)
  
    def test_embed(self):
        self.assertIn(self.embed_code, self.rendered)

    def test_post(self):
        self.assertIn(self.thread.post, self.rendered)



class ThreadIDFormat(TestCase): 

    def setUp(self):
        self.thread = ThreadFactory(id_enabled=True)
        context = Context({'thread': self.thread, 'moderation_view': False})
        template_to_render = Template('{% load imageboard_objects %} {% thread_format thread %}')
        self.rendered = template_to_render.render(context)

    def test_id(self):
        self.assertIn(self.thread.poster_id, self.rendered)


class ThreadFormatMod(TestCase):

    def setUp(self):
        self.thread = ThreadFactory(reported=True)
        mod = ModeratorFactory.create_mod()
        self.client.force_login(mod)
        perm_resp = self.client.get(self.thread.get_absolute_url())
        perms = perm_resp.context['perms'] #Get the permission context for a user
        context = Context({'thread': self.thread,
            'moderation_view': True,
            'perms': perms
        })
        template_to_render = Template('{% load imageboard_objects %} {% thread_format thread %}')
        self.mod_rendered = template_to_render.render(context) #Test the permission context


    def test_delete(self):
        self.assertIn(self.thread.get_delete_url(), self.mod_rendered)

    def test_ban(self):
        self.assertIn(self.thread.get_ban_url(), self.mod_rendered)
 
    def test_report_dismiss(self):
        self.assertIn(self.thread.get_report_dismiss_url(), self.mod_rendered)


class UserPostFormat(TestCase):

    def setUp(self):
        embed_link = 'http://www.youtube.com/watch?v=dQw4w9WgXcQ'
        self.embed_code = 'dQw4w9WgXcQ' 
        self.post = UserPostFactory(embed=embed_link)
        context = Context({'post': self.post, 
            'moderation_view': False})
        template_to_render = Template('{% load imageboard_objects %} {% post_format post %}')
        self.rendered = template_to_render.render(context)
            

    def test_name(self):
        self.assertIn(self.post.name, self.rendered)

    def test_report(self):
        self.assertIn(self.post.get_report_url(), self.rendered)

    def test_embed(self):
        self.assertIn(self.embed_code, self.rendered)

    def test_post(self):
        self.assertIn(self.post.post, self.rendered)


class UserPostIDFormat(TestCase):
  
    def setUp(self):
        self.post = UserPostFactory(thread__id_enabled=True) 
        context = Context({'post': self.post, 
            'moderation_view': False})
        template_to_render = Template('{% load imageboard_objects %} {% post_format post %}')
        self.rendered = template_to_render.render(context)

    def test_id(self):
        self.assertIn(self.post.poster_id, self.rendered)

class UserPostFormatMod(TestCase):

    def setUp(self):
        self.post = UserPostFactory(reported=True)
        mod = ModeratorFactory.create_mod()
        self.client.force_login(mod)
        perm_resp = self.client.get(self.post.get_absolute_url())
        perms = perm_resp.context['perms'] #Get the permission context for a user
        context = Context({'post': self.post,
            'moderation_view': True,
            'perms': perms
        })
        template_to_render = Template('{% load imageboard_objects %} {% post_format post %}')
        self.mod_rendered = template_to_render.render(context) #Test the permission context


    def test_delete(self):
        self.assertIn(self.post.get_delete_url(), self.mod_rendered)

    def test_ban(self):
        self.assertIn(self.post.get_ban_url(), self.mod_rendered)
 
    def test_report_dismiss(self):
        self.assertIn(self.post.get_report_dismiss_url(), self.mod_rendered)

