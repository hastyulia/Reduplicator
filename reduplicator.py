import re
import os
import sys
import requests
import webbrowser
import proxy_server


class Reduplicator:
    def __init__(self, prefix='ху') -> None:
        self.printable = False
        self.url_pattern = re.compile(
            r'^(https?://)([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*\S*)*')
        self.prefix = prefix
        self.result = ''
        self.consonant_pattern = re.compile(r'[бвгджзйклмнпрстфхцчшщъь]+')
        self.vowel_pattern = re.compile(r'[аеёиоуыэюя]')
        self.replace_dict = {
            'а': 'я',
            'е': 'е',
            'ё': 'ё',
            'и': 'и',
            'о': 'ё',
            'у': 'ю',
            'ы': 'и',
            'э': 'е',
            'ю': 'ю',
            'я': 'я'
        }

    def check_input(self) -> bool:
        match_prefix = re.search(r'[а-яА-ЯЁё]+', self.prefix)
        if not match_prefix:
            return False

        if re.search(self.vowel_pattern, self.prefix):
            while self.prefix[-1] in 'бвгджзйклмнпрстфхцчшщъь':
                self.prefix = self.prefix[:-1]

        return True

    def reduplicate(self, text: str) -> None:
        if not self.check_input():
            print('incorrect prefix')
            return

        match_url = re.search(self.url_pattern, text)
        if not match_url:
            self.reduplicate_text(text)

        else:
            self.reduplicate_website(text)

    def reduplicate_text(self, text: str) -> None:
        split_text = re.split(r'(\W+)', text)
        reduplicated_text = []
        for word in split_text:
            word = word.lower()
            vowel = re.search(self.vowel_pattern, word)
            if not vowel or len(word) <= 2:
                reduplicated_text.append('')
                continue

            word = re.sub(self.vowel_pattern,
                          self.replace_dict[vowel.group(0)], word, count=1)
            prefix = self.prefix
            if self.prefix[-1] == vowel.group(0):
                prefix = self.prefix[:-1]

            if word[0] in 'бвгджзйклмнпрстфхцчшщъь':
                reduplicated_text.append('--' + self.consonant_pattern.sub(
                    prefix, word, count=1))

            else:
                reduplicated_text.append('--' + prefix + word)

        for index in range(len(split_text)):
            self.result += (split_text[index]
                            + re.sub(r'^[бвгджзйклмнпрстфхцчшщъь]', '',
                                     reduplicated_text[index]))

        self.printable = True

    def reduplicate_website(self, address: str) -> None:
        response = requests.get(address)
        file = response.content.decode('UTF-8')
        self.reduplicate_text(file)
        with open('site.html', 'w') as html_file:
            html_file.write(self.result)

        self.printable = False


if __name__ == '__main__':
    reduplication_word = input()
    if sys.argv == 'proxy':
        proxy_server.listen()

    input_text = input()
    reduplicator = Reduplicator(reduplication_word)
    reduplicator.reduplicate(input_text)
    if reduplicator.printable:
        print(reduplicator.result)

    else:
        path = os.path.abspath('site.html')
        webbrowser.get('safari')
        webbrowser.open('file://' + path, new=2, autoraise=True)
