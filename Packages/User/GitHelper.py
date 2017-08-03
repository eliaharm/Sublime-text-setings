# @author          Avtandil Kikabidze
# @copyright       Copyright (c) 2008-2016, Avtandil Kikabidze aka LONGMAN (akalongman@gmail.com)
# @link            http://longman.me
# @license         The MIT License (MIT)

import sublime
import sublime_plugin
import Git.git
import functools

class GitHelperAddCommand(Git.git.GitTextCommand):

    def __init__(self, view):
        self.view = view

    def run(self, edit):
        self.run_command(['git', 'add', '.'],
            functools.partial(self.add_done, "Committing whole repo"))

    def add_done(self, message, result):
        if result.strip():
            sublime.error_message("Error adding files: " + result)
            return

        self.view.window().show_input_panel('Commit msg', '', lambda s: self.on_done(s), None, None)


    def on_done(self, text):
        if text.strip() == "":
            sublime.error_message("Commit message is empty!")
            return

        self.run_command(['git', 'commit', '-m', text],
            callback=self.update_status)

    def update_status(self, output, **kwargs):
        if output.find('nothing to commit, working directory clean') != -1:
            sublime.status_message("Nothing to commit, working directory clean")
            return

        sublime.status_message("Commit success: "+output)