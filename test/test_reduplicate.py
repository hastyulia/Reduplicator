import unittest
from reduplicator import Reduplicator


class ReduplicatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fake_html = """
        <noscript>
            <div class="tag-home__item">
                Поисковая система.
                <span class="hide--screen-xs">
                <a class="tag-home__link">Узнайте больше<a>
            </div>
        </noscript>
        """
        self.fake_html_result = """
        <noscript>
            <div class="tag-home__item">
                Поисковая--хуёисковая система--хуистема.
                <span class="hide--screen-xs">
                <a class="tag-home__link">Узнайте--хюзнайте больше--хуёльше<a>
            </div>
        </noscript>
        """

    def test_init(self) -> None:
        reduplicator = Reduplicator()
        self.assertEqual(reduplicator.prefix, 'ху')

    def test_reduplicate_xy(self) -> None:
        reduplicator = Reduplicator()
        reduplicator.reduplicate('Мама мыла раму')
        self.assertEqual('Мама--хуяма мыла--хуила раму--хуяму',
                         reduplicator.result)

    def test_reduplicate_shm(self) -> None:
        reduplicator = Reduplicator('шм')
        reduplicator.reduplicate('Мама мыла раму')
        self.assertEqual('Мама--шмяма мыла--шмила раму--шмяму',
                         reduplicator.result)

    def test_reduplicate_long(self) -> None:
        reduplicator = Reduplicator('шмель')
        reduplicator.reduplicate('Телефон')
        self.assertEqual('Телефон--шмелефон',
                         reduplicator.result)

    def test_reduplicate_first_vowel(self) -> None:
        reduplicator = Reduplicator('шмель')
        reduplicator.reduplicate('яма')
        self.assertEqual('яма--шмеяма',
                         reduplicator.result)

    def test_reduplicate_incorrect_prefix(self) -> None:
        reduplicator = Reduplicator('01')
        self.assertEqual(None, reduplicator.reduplicate('мама мыла раму'))

    def test_reduplicate_no_vowel(self) -> None:
        reduplicator = Reduplicator()
        reduplicator.reduplicate('мм мл рм')
        self.assertEqual('мм мл рм', reduplicator.result)

    def test_reduplicate_en(self) -> None:
        reduplicator = Reduplicator()
        reduplicator.reduplicate('hello word')
        self.assertEqual('hello word', reduplicator.result)

    def test_reduplicate_url(self) -> None:
        reduplicator = Reduplicator()
        reduplicator.reduplicate('https://duckduckgo.com')
        self.assertFalse(reduplicator.printable)

    def test_reduplicate_html(self) -> None:
        reduplicator = Reduplicator()
        reduplicator.reduplicate(self.fake_html)
        self.assertEqual(self.fake_html_result, reduplicator.result)

    def test_reduplicate_en_ru(self) -> None:
        reduplicator = Reduplicator()
        reduplicator.reduplicate('hello word мама Мыла раму')
        self.assertEqual('hello word мама--хуяма Мыла--хуила раму--хуяму',
                         reduplicator.result)

    def test_check_input_correct(self) -> None:
        reduplicator = Reduplicator('мы')
        self.assertEqual(True, reduplicator.check_input())

    def test_check_input_incorrect_en(self) -> None:
        reduplicator = Reduplicator('vv')
        self.assertEqual(False, reduplicator.check_input())

    def test_check_input_incorrect_number(self) -> None:
        reduplicator = Reduplicator('11')
        self.assertEqual(False, reduplicator.check_input())
