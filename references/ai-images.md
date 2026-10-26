# Фото Маші, 3D-предмети й AI

## Бібліотека (`~/.claude/skills/styl-yaroslavy/assets/library/`)

**masha/** — фото Маші є лише в приватній версії. Поклади сюди свої: вирізані PNG і темні фото в червоному світлі.

**props/** (уже обрізані по межах, прозоре тло)
- `robot-scroll.png` — чорний робот із сувоєм переписок (AI-агент, автоматизація).
- `hourglass.png` — пісочний годинник (довго, час, чекання).
- `phone-chat.png` — телефон з чатом і календарем (переписки, запис).
- `bubble-typing.png` — червона бульбашка «друкує…» (тиша, відповідь).
- `calendar-check.png` — календар з галочкою (запис, результат).
- `claw-marble-bust-red-blazer.png` — чорно-червона клешня згори тримає мармурове античне погруддя в застебнутому червоному жакеті (кейс товарки plus-size, світлий арт-колаж, 26.10.2026).
- `claw-red-blazer-money.png` — та сама клешня тримає вішалку з червоним жакетом, з нагрудної кишені ледь видно долари. Запасна обкладинка того ж кейсу.
- Для кейсу товарки plus-size (26.10.2026) Маша зрештою поставила першим слайдом **статую** (`claw-marble-bust-red-blazer.png`): чисто біле тло #fff, як у закріпленому «Кейсі моєї трансформації», червоний мазок пензля під предметом.


## Нові 3D-предмети (Higgsfield)

Модель `gpt_image_2_5`, `background: "transparent"`, `aspect_ratio: "1:1"` (або `"2:3"` для високих предметів, ціна та сама). **Ціни на 26.10.2026: `quality: "low"` (і без параметра) — 0,25 кредиту, `"medium"` — 0,5.** Перед генерацією перевір `get_cost: true`. Відхилені фільтром (`nsfw`) не списуються.

Фільтр і смак: для статуй і людських фігур не пиши «voluptuous», «curvy», «Venus» — фільтр ріже, а пройдене виходить з глибоким вирізом. Пиши «fully buttoned blazer over a white high-neck top, nothing revealing, exactly one head» — інакше буває подвоєна голова. Кілька штук — одним `generate_image_batch`, далі `jobs_wait`, завантаж `result_url` через curl і обріж: `scripts/trim_alpha.sh *.png` (з'являться `t-*.png`).

Шаблон промпту (англійською, так модель тримає стиль стабільніше):
```
Glossy premium 3D <object>, black and red color scheme, soft plastic look, slight tilt,
studio product render, soft red rim light, isolated object, transparent background, no text, no letters, no numbers
```
Що вже добре вийшло: `cute premium 3D robot assistant reading a long unrolled scroll of chat message bubbles, black glossy body with red glowing accents and red eyes`; `glossy red 3D speech bubble with three white typing dots`; `premium 3D smartphone ... messenger chat with red and dark grey speech bubbles and a small calendar icon`.

Для сторіс у Ярослави трапляються смішні стікери-меми (кіт у темних окулярах з грошима). Їх можна генерувати тим самим способом, у реалістично-глянцевому 3D.

## Гроші

- **Вартість називай Маші до генерації**: «≈0,25 кредиту за предмет у стандартній якості (0,5 у medium), 4 предмети ≈ 1 кредит».
- Апскейл фото (`upscale_image`, bytedance): 2 кредити за фото, 2k і 4k коштують однаково.
- Баланс — `balance` у Higgsfield. У Creative Claw кредитів мало, для картинок бери Higgsfield.

## Обличчя й мітка AI

- Обличчя Маші через AI не генеруємо і не «покращуємо» генерацією. Справжні фото, вирізання (`cutout.swift`) і апскейл риси не змінюють, тому мітка не потрібна.
- Якщо все ж згенеровано реалістичну людину (зокрема «фото Маші» з референсу), на пості має стояти «Створено з AI» / AI info. Так вимагає закон ЄС про AI (Маша працює в ЄС). Згенеровані 3D-предмети й ілюстрації мітки не потребують.
- Якщо невідомо, звідки фото (Ярослава теж генерує фото), запитай Машу або попередь її про мітку.

## Маленьке фото

Якщо фото менше ніж ~1000 px по меншому боку, а потрібне на весь кадр:
1. Для фону на весь екран (обкладинка рілс) — апскейл у Higgsfield: `media_upload` → curl PUT → `media_confirm` → `upscale_image` з `width`/`height` оригіналу.
2. Для фото на пів слайда безкоштовно вистачає ffmpeg: `scale=iw*2.2:ih*2.2:flags=lanczos,unsharp=5:5:0.6`.
3. У будь-якому разі краще попросити в Маші оригінал.

## Вирізати фігуру

`swift ~/.claude/skills/styl-yaroslavy/scripts/cutout.swift in.jpg out.png` (macOS Vision). Добре працює на світлому чи кольоровому тлі. Чорне волосся на чорному тлі ріже погано: для таких фото бери `bleed`.
