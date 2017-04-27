# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import general.models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='language',
            field=general.models.VarCharField(default=b'en', max_length=8, verbose_name='Language', choices=[(b'af', 'Afrikaans'), (b'ar', '\u0627\u0644\u0639\u0631\u0628\u064a\u0651\u0629'), (b'ast', 'asturianu'), (b'az', 'Az\u0259rbaycanca'), (b'bg', '\u0431\u044a\u043b\u0433\u0430\u0440\u0441\u043a\u0438'), (b'be', '\u0431\u0435\u043b\u0430\u0440\u0443\u0441\u043a\u0430\u044f'), (b'bn', '\u09ac\u09be\u0982\u09b2\u09be'), (b'br', 'brezhoneg'), (b'bs', 'bosanski'), (b'ca', 'catal\xe0'), (b'cs', '\u010desky'), (b'cy', 'Cymraeg'), (b'da', 'dansk'), (b'de', 'Deutsch'), (b'el', '\u0395\u03bb\u03bb\u03b7\u03bd\u03b9\u03ba\u03ac'), (b'en', 'English'), (b'en-au', 'Australian English'), (b'en-gb', 'British English'), (b'eo', 'Esperanto'), (b'es', 'espa\xf1ol'), (b'es-ar', 'espa\xf1ol de Argentina'), (b'es-mx', 'espa\xf1ol de Mexico'), (b'es-ni', 'espa\xf1ol de Nicaragua'), (b'es-ve', 'espa\xf1ol de Venezuela'), (b'et', 'eesti'), (b'eu', 'Basque'), (b'fa', '\u0641\u0627\u0631\u0633\u06cc'), (b'fi', 'suomi'), (b'fr', 'fran\xe7ais'), (b'fy', 'frysk'), (b'ga', 'Gaeilge'), (b'gl', 'galego'), (b'he', '\u05e2\u05d1\u05e8\u05d9\u05ea'), (b'hi', 'Hindi'), (b'hr', 'Hrvatski'), (b'hu', 'Magyar'), (b'ia', 'Interlingua'), (b'id', 'Bahasa Indonesia'), (b'io', 'ido'), (b'is', '\xcdslenska'), (b'it', 'italiano'), (b'ja', '\u65e5\u672c\u8a9e'), (b'ka', '\u10e5\u10d0\u10e0\u10d7\u10e3\u10da\u10d8'), (b'kk', '\u049a\u0430\u0437\u0430\u049b'), (b'km', 'Khmer'), (b'kn', 'Kannada'), (b'ko', '\ud55c\uad6d\uc5b4'), (b'lb', 'L\xebtzebuergesch'), (b'lt', 'Lietuvi\u0161kai'), (b'lv', 'latvie\u0161u'), (b'mk', '\u041c\u0430\u043a\u0435\u0434\u043e\u043d\u0441\u043a\u0438'), (b'ml', 'Malayalam'), (b'mn', 'Mongolian'), (b'mr', '\u092e\u0930\u093e\u0920\u0940'), (b'my', '\u1019\u103c\u1014\u103a\u1019\u102c\u1018\u102c\u101e\u102c'), (b'nb', 'norsk (bokm\xe5l)'), (b'ne', '\u0928\u0947\u092a\u093e\u0932\u0940'), (b'nl', 'Nederlands'), (b'nn', 'norsk (nynorsk)'), (b'os', '\u0418\u0440\u043e\u043d'), (b'pa', 'Punjabi'), (b'pl', 'polski'), (b'pt', 'Portugu\xeas'), (b'pt-br', 'Portugu\xeas Brasileiro'), (b'ro', 'Rom\xe2n\u0103'), (b'ru', '\u0420\u0443\u0441\u0441\u043a\u0438\u0439'), (b'sk', 'slovensk\xfd'), (b'sl', 'Sloven\u0161\u010dina'), (b'sq', 'shqip'), (b'sr', '\u0441\u0440\u043f\u0441\u043a\u0438'), (b'sr-latn', 'srpski (latinica)'), (b'sv', 'svenska'), (b'sw', 'Kiswahili'), (b'ta', '\u0ba4\u0bae\u0bbf\u0bb4\u0bcd'), (b'te', '\u0c24\u0c46\u0c32\u0c41\u0c17\u0c41'), (b'th', '\u0e20\u0e32\u0e29\u0e32\u0e44\u0e17\u0e22'), (b'tr', 'T\xfcrk\xe7e'), (b'tt', '\u0422\u0430\u0442\u0430\u0440\u0447\u0430'), (b'udm', '\u0423\u0434\u043c\u0443\u0440\u0442'), (b'uk', '\u0423\u043a\u0440\u0430\u0457\u043d\u0441\u044c\u043a\u0430'), (b'ur', '\u0627\u0631\u062f\u0648'), (b'vi', 'Ti\xea\u0301ng Vi\xea\u0323t'), (b'zh-cn', '\u7b80\u4f53\u4e2d\u6587'), (b'zh-hans', '\u7b80\u4f53\u4e2d\u6587'), (b'zh-hant', '\u7e41\u9ad4\u4e2d\u6587'), (b'zh-tw', '\u7e41\u9ad4\u4e2d\u6587')]),
        ),
    ]
