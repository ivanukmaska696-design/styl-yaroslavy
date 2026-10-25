# Відео: сторіс, рілс, анімовані слайди в стилі Ярослави

Інструменти лежать у `~/Projects/Інструменти/hyperframes-motion/` (HyperFrames 0.8.x, телеметрію вимкнено; завжди запускай з `HYPERFRAMES_NO_TELEMETRY=1`). Команду `npx hyperframes add` не запускай: вона пише в буфер обміну.

## Сторіс із Машею в кадрі

1. Нарізка й підготовка: `python3 prep_story.py <name> <input.mov> <job ai-video-editor | -> "a-b,c-d"`. Буде `shared/<name>.mp4`, слова з таймінгами й трек обличчя.
2. Конфіг `shared/<name>-yar.json`: заголовки (`headlines` з `text`, `accent`, `start`, `end`), `keywords` (червоні слова), `emoji`, `slam` (великий удар словом), `punches` (наїзди камери), `"head_style": "yar"`. Зразки: `shared/story03-yar.json`, `story05-yar.json`, `story07-yar.json`.
3. Збірка: `python3 build_story.py <проєкт> blood shared/<name>-yar.json`. Заголовок буде червоною пігулкою Montserrat зі світінням, субтитри «Кривава крапля»: ключові слова червоні, з них стікають краплі.
4. Перевірка: `npx hyperframes check --json` (помилок має бути 0), кадри через `snapshot --at …`.
5. Рендер: `npx hyperframes render --output ../out/<name>.mp4`, потім гучність: `ffmpeg -i in.mp4 -af loudnorm=I=-16:TP=-1.5:LRA=11 -ar 48000 -c:v copy -c:a aac -b:a 192k out-final.mp4`. Без `-ar 48000` loudnorm віддає 96 кГц.

Текст і субтитри автоматично ставляться поза обличчям.

## Рілс зі шматків кількох сторіс

`python3 make_reels.py shared/<name>-spec.json`. У spec: `pieces` (`[config, від, до]`) і `headlines` у часі готового відео. Слова, обличчя й наїзди переносяться самі; на склейках є стрибок зуму, при зміні кліпу — спалах. Далі `build_story.py … blood shared/<name>-yar.json` і рендер, як вище. Зразок: `shared/reels01-spec.json`.

Правила рілс:
- Гачок у першу секунду: заголовок-пігулка одразу з 0,1 с.
- 35–50 с.
- У кінці пігулка «підпишись: покажу …», щоб дати причину лишитися.
- У відео немає закликів писати в коментарі.
- Обкладинка окремим PNG (див. `formats.md`, розділ 4). При викладанні вмикай «Пробний ролик».

## Анімовані слайди (між розмовними сторіс)

`python3 build_slide_yar.py <slide04-yar|slide06-yar|slide08-yar>`. Новий слайд — додай запис у словник `SLIDES` на початку файлу (eyebrow, head з акцентом, facts / bad / good, card_title + ticks, cta, vote). Слайд має червоне сяйво з кута, пігулки, перекреслення неправильного, білу картку з галочками й контурну кнопку.

## Статичний слайд для сторіс без анімації

Простіше зібрати через `yar_kit` з `Deck("story")` (див. `formats.md`, розділ 3).
