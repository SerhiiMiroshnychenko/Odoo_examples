# pip install googletrans==4.0.0-rc1
from googletrans import Translator


translator = Translator()

src_text = 'Привіт! Як твої справи?'
src_lang = 'uk'
dest_lang = 'en'

result = translator.translate(src_text, src=src_lang, dest=dest_lang)

print(result.text)
