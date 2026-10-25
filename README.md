# styl-yaroslavy

Скіл для Claude: фірмовий візуальний і текстовий стиль, у якому живе Instagram [@mari.ivanuk](https://www.instagram.com/mari.ivanuk/) (дизайн SMM Ярослави). Каруселі, пости, кейси, сторіс, обкладинки рілс, підписи, 3D-предмети, моушн.

Це публічна версія: без фото, особистих фактів і оригінальних робіт Ярослави. Правила, набір блоків, шрифти й 3D-предмети на місці.

## Встановити (Claude Code)

```bash
git clone https://github.com/ivanukmaska696-design/styl-yaroslavy.git ~/.claude/skills/styl-yaroslavy
```

Перевірити, що все малюється:
```bash
python3 ~/.claude/skills/styl-yaroslavy/scripts/yar_kit.py --demo /tmp/yar-demo
```
Потрібні Python 3 і Chrome (або headless Chrome), для 3D-предметів і вирізання — ffmpeg і macOS.

## Що всередині

- `SKILL.md` — правила стилю, блоки, композиція, тексти, чеклист.
- `scripts/yar_kit.py` — готові блоки (пігулки, картки, списки, плитки з цифрами, фото, 3D-предмети) і рендер у PNG.
- `scripts/trim_alpha.sh` — обрізає прозорі поля 3D-предметів; `scripts/cutout.swift` — вирізає людину з фото (macOS Vision).
- `assets/fonts` — Montserrat (змінний шрифт, SIL Open Font License). `assets/library/props` — 3D-предмети.
- `references/` — формати, блоки, підписи, AI-картинки, відео, приклади.

Посилання на приклади Ярослави (`yar-*.jpg`) і файл фактів ведуть на файли, яких тут немає: вони лише в приватній версії.
