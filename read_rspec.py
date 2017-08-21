import sublime
import sublime_plugin
import itertools

class ReadRspecCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        lines = self.search_lines_with_rspec_history_pattern()
        text = self.get_text_from_lines(lines)
        self.create_new_tab(text)

    def search_lines_with_rspec_history_pattern(self):
        regions = self.view.find_all('\ +(describe|it|context|specify)\s')
        lines = itertools.groupby(regions, self.view.line)
        return [l for l, _ in lines]

    def get_text_from_lines(self, lines):
        return '\n'.join([self.format_line_output(l) for l in lines]);

    def format_line_output(self, line):
        line_number = self.view.rowcol(line.begin())[0]
        return '%5d: %s' % (line_number, self.view.substr(line))

    def create_new_tab(self, text):
        results_view = self.view.window().new_file()
        results_view.set_name('RSpec History')
        results_view.set_scratch(True)
        results_view.run_command('append', {'characters': text, 'force': True, 'scroll_to_end': False})
        results_view.set_syntax_file(self.view.settings().get('syntax'))
