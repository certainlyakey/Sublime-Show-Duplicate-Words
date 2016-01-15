import sublime
import sublime_plugin
import collections, re, string

PLUGIN_NAME = "show_duplicate_words"
SETTINGS_FILE = PLUGIN_NAME + ".sublime-settings"

def filter_list(full_list, excludes):
    s = set(excludes)
    return (x for x in full_list if x not in s)

def show_words(text, view, edit):
    excludeshortwords = re.compile(r'\W*\b\w{1,3}\b|\d+')
    excludepunctuation = re.compile('[%s]' % re.escape(string.punctuation))
    text = excludeshortwords.sub('', text)
    text = excludepunctuation.sub('', text)
    words = text.split()
    words = map(lambda x:x.lower(),words)
    stopwords = sublime.Settings.get(sublime.load_settings(SETTINGS_FILE), 'ignored_words', {})
    cleanedwords = list(filter_list(words, stopwords))
    word_counts = collections.Counter(cleanedwords)
    for word, count in sorted(word_counts.items(), key=lambda times: times[1]):
        if count == 1:
            continue
        view.insert(edit, 0, '"%s" is repeated %d times.\n' % (word, count))

class ShowDuplicateWordsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selections = self.view.sel() 
        newview = sublime.active_window().new_file()
        isNotSelected = len(selections) == 1 and selections[0].size() == 0
        if isNotSelected:
            all = self.view.substr(sublime.Region(0, self.view.size()))
            show_words(all, newview, edit)
        else:
            for region in selections:
                show_words(self.view.substr(region), newview, edit)