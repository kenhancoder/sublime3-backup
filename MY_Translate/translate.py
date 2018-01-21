

import sublime
import sublime_plugin

import requests
import json

api_url = {
    'google': 'https://translate.googleapis.com/translate_a/single',
}


def handle_data(api, data):
    if api == 'google':
        return ''.join([item[0] for item in data[0]])


def search(self, text):
    """
        languge
        auto
        zh-CN
        en
    """
    params = {}

    source_language = 'auto'

    target_language = 'zh-CN'

    settings = sublime.load_settings('translate.sublime-settings')
    api = settings.get('api').lower()

    if settings.get('source_language'):
        source_language = settings.get('source_language')
    if settings.get('target_language'):
        target_language = settings.get('target_language')

    if api == 'google':
        params['client'] = "gtx"
        params['sl'] = source_language
        params['tl'] = target_language
        params['dt'] = "t"
        params['q'] = text

    url = api_url.get(api, 'google')
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = json.loads(response.text)
        popup_data = handle_data(api, data)
        self.view.show_popup(popup_data, max_width=888, max_height=888)


class TranslateSelectionCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self.input()
        for selection in self.view.sel():
            if selection.empty():
                text = self.view.word(selection)
            text = self.view.substr(selection)
            search(self, text)

print(dir(sublime_plugin.WindowCommand))
# print(dir(sublime))
# class InstallHandler(sublime_plugin.ListInputHandler):
#     pass
# class TranslateTargetInputHandler(sublime_plugin.ListInputHandler):
#     def name(self):
#         return "name"

#     def placeholder(self):
#         return "Name"

#     def list_items(self):
#         return ['zh-CN', 'en']
