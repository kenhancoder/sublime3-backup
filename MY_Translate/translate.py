# -*- coding: utf-8 -*-
import sublime
import sublime_plugin

import requests
import json

SETTINGS = {}

api_url = {
    'google': 'https://translate.googleapis.com/translate_a/single',
}


def handle_data(api, data):
    if api == 'google':
        return ''.join([item[0] for item in data[0]])


def search(self, text, target_lang):
    """
        languge
        auto
        zh-CN
        en
    """
    params = {}

    source_lang = 'auto'

    api = SETTINGS.get('api')

    if SETTINGS.get('source_lang'):
        source_lang = SETTINGS.get('source_lang')

    if api == 'google':
        params['client'] = "gtx"
        params['sl'] = source_lang
        params['tl'] = target_lang
        params['dt'] = "t"
        params['q'] = text

    url = api_url.get(api, 'google')
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = json.loads(response.text)
        popup_data = handle_data(api, data)
        self.view.show_popup(popup_data, max_width=888, max_height=888)


class TranslateCommand(sublime_plugin.TextCommand):
    def run(self, edit, **kw):
        text_ls = []
        for selection in self.view.sel():
            if selection.empty():
                text = self.view.word(selection)
            else:
                text = self.view.substr(selection)
            text_ls.append(text)
        search(self, ''.join(text_ls), kw['target_lang'])


class TranslateSelectionCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        langs = SETTINGS.get('langs')
        print(langs)

        def on_done(index):
            if index >= 0:
                self.view.run_command("translate", {"target_lang": langs[index]})
        self.view.window().show_quick_panel(langs, on_done)


def get_settings():
    settings = sublime.load_settings('translate.sublime-settings')
    SETTINGS['api'] = settings.get('api', 'google').lower()
    SETTINGS['source_lang'] = settings.get('source_lang', 'auto')
    SETTINGS['langs'] = settings.get('langs', ["zh-CN", "en"])


def init_settings():
    get_settings()
    sublime.load_settings('translate.sublime-settings').add_on_change('get_settings', get_settings)


def plugin_loaded():
    init_settings()
