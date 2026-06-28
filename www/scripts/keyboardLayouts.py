# Keyboard layouts for the visual keyboard visualization feature.
# Format: Each layout is a list of rows. Each row is a list of items:
#   - str: key label (implicit Key_<label> mapping)
#   - list: [label, 'Key_EDName'] explicit ED key name
#   - dict: special instructions for the NEXT key (x=offset, w=width, h=height, etc.)
#
# Label suffixes:
#   __L / __R / __N = trim to the left/right/numpad variant for display
#   \n = newline within the label (top/bottom of key shown)
#
# Ported from clockbrain/edrefcard2 PR #39 (branch: keyboard), bindingsData.py

keyboardLayouts = {
    'ANSI 104': [
        ['Esc', {'x': 1}, 'F1', 'F2', 'F3', 'F4', {'x': 0.5}, 'F5', 'F6', 'F7', 'F8', {'x': 0.5}, 'F9', 'F10', 'F11', 'F12', {'x': 0.25}, 'PrtSc', ['ScrLk', 'Key_ScrollLock'], ['Pause\nBreak', 'Key_Pause']],
        [{'y': 0.5}, ['~\n`', 'Key_Grave'], ['!\n1', 'Key_1'], ['@\n2', 'Key_2'], ['#\n3', 'Key_3'], ['$\n4', 'Key_4'], ['%\n5', 'Key_5'], ['^\\n6', 'Key_6'], ['&\n7', 'Key_7'], ['*\n8', 'Key_8'], ['(\n9', 'Key_9'], [')\n0', 'Key_0'], ['_\n-', 'Key_Minus'], ['+\n=', 'Key_Equals'], {'w': 2}, 'Backspace',
            {'x': 0.25}, 'Insert', 'Home', ['PgUp', 'Key_PageUp'], {'x': 0.25}, ['Num\nLock', 'Key_NumLock'], ['/__N', 'Key_Numpad_Divide'], ['*__N', 'Key_Numpad_Multiply'], ['-__N', 'Key_Numpad_Subtract']],
        [{'w': 1.5}, 'Tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', ['{\n[', 'Key_LeftBracket'], ['}\n]', 'Key_RightBracket'], {'w': 1.5}, ['|\n\\', 'Key_BackSlash'], {'x': 0.25},
            'Delete', 'End', ['PgDn', 'Key_PageDown'], {'x': 0.25}, ['7__N\nHome__N', 'Key_Numpad_7'], ['8__N\n↑', 'Key_Numpad_8'], ['9__N\nPgUp__N', 'Key_Numpad_9'], {'h': 2}, ['+__N', 'Key_Numpad_Add']],
        [{'w': 1.75}, ['Caps Lock', 'Key_CapsLock'], 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', [':\n;', 'Key_SemiColon'], ['"\n\'', 'Key_Apostrophe'], {'w': 2.25}, 'Enter',
            {'x': 3.5}, ['4__N\n←', 'Key_Numpad_4'], ['5__N', 'Key_Numpad_5'], ['6__N\n→', 'Key_Numpad_6']],
        [{'w': 2.25}, ['Shift__L', 'Key_LeftShift'], 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ['<\n,', 'Key_Comma'], ['>\n.', 'Key_Period'], ['?\n/', 'Key_Slash'], {'w': 2.75}, ['Shift__R', 'Key_RightShift'],
            {'x': 1.25}, ['↑', 'Key_UpArrow'], {'x': 1.25}, ['1__N\nEnd__N', 'Key_Numpad_1'], ['2__N\n↓', 'Key_Numpad_2'], ['3__N\nPgDn__N', 'Key_Numpad_3'], {'h': 2}, ['Enter__N', 'Key_Numpad_Enter']],
        [{'w': 1.25}, ['Ctrl__L', 'Key_LeftControl'], {'w': 1.25}, ['Win__L', 'Key_LeftWindows'], {'w': 1.25}, ['Alt__L', 'Key_LeftAlt'], {'a': 7, 'w': 6.25}, [' ', 'Key_Space'], {'a': 4, 'w': 1.25}, ['Alt__R', 'Key_RightAlt'], {'w': 1.25}, ['Win__R', 'Key_RightWindows'], {'w': 1.25}, 'Menu', {'w': 1.25}, ['Ctrl__R', 'Key_RightControl'],
            {'x': 0.25}, ['←', 'Key_LeftArrow'], ['↓', 'Key_DownArrow'], ['→', 'Key_RightArrow'], {'x': 0.25, 'w': 2}, ['0__N\nIns__N', 'Key_Numpad_0'], ['.__N\nDel__N', 'Key_Numpad_Decimal']],
    ],
    'ISO 105': [
        ['Esc', {'x': 1}, 'F1', 'F2', 'F3', 'F4', {'x': 0.5}, 'F5', 'F6', 'F7', 'F8', {'x': 0.5}, 'F9', 'F10', 'F11', 'F12', {'x': 0.25}, 'PrtSc', ['ScrLk', 'Key_ScrollLock'], ['Pause\nBreak', 'Key_Pause']],
        [{'y': 0.5}, ['¬\n`', 'Key_Grave'], ['!\n1', 'Key_1'], ['"\n2', 'Key_2'], ['£\n3', 'Key_3'], ['$\n4', 'Key_4'], ['%\n5', 'Key_5'], ['^\n6', 'Key_6'], ['&\n7', 'Key_7'], ['*\n8', 'Key_8'], ['(\n9', 'Key_9'], [')\n0', 'Key_0'], ['_\n-', 'Key_Minus'], ['+\n=', 'Key_Equals'], {'w': 2}, 'Backspace',
            {'x': 0.25}, 'Insert', 'Home', ['PgUp', 'Key_PageUp'], {'x': 0.25}, ['Num Lock', 'Key_NumLock'], ['/__N', 'Key_Numpad_Divide'], ['*__N', 'Key_Numpad_Multiply'], ['-__N', 'Key_Numpad_Subtract']],
        [{'w': 1.5}, 'Tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', ['{\n[', 'Key_LeftBracket'], ['}\n]', 'Key_RightBracket'], {'x': 0.25, 'w': 1.25, 'h': 2, 'w2': 1.5, 'h2': 1, 'x2': -0.25}, 'Enter',
            {'x': 0.25}, 'Delete', 'End', ['PgDn', 'Key_PageDown'], {'x': 0.25}, ['7__N\nHome__N', 'Key_Numpad_7'], ['8__N\n↑', 'Key_Numpad_8'], ['9__N\nPgUp__N', 'Key_Numpad_9'], {'h': 2}, ['+__N', 'Key_Numpad_Add']],
        [{'w': 1.75}, ['Caps Lock', 'Key_CapsLock'], 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', [':\n;', 'Key_SemiColon'], ["@\n'", 'Key_Apostrophe'], ['~\n#', 'Key_Hash'],
            {'x': 4.75}, ['4__N\n←', 'Key_Numpad_4'], ['5__N', 'Key_Numpad_5'], ['6__N\n→', 'Key_Numpad_6']],
        [{'w': 1.25}, ['Shift__L', 'Key_LeftShift'], ['|\n\\', 'Key_BackSlash'], 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ['<\n,', 'Key_Comma'], ['>\n.', 'Key_Period'], ['?\n/', 'Key_Slash'], {'w': 2.75}, ['Shift__R', 'Key_RightShift'],
            {'x': 1.25}, ['↑', 'Key_UpArrow'], {'x': 1.25}, ['1__N\nEnd__N', 'Key_Numpad_1'], ['2__N\n↓', 'Key_Numpad_2'], ['3__N\nPgDn__N', 'Key_Numpad_3'], {'h': 2}, ['Enter__N', 'Key_Numpad_Enter']],
        [{'w': 1.25}, ['Ctrl__L', 'Key_LeftControl'], {'w': 1.25}, ['Win__L', 'Key_LeftWindows'], {'w': 1.25}, ['Alt__L', 'Key_LeftAlt'], {'a': 7, 'w': 6.25}, [' ', 'Key_Space'], {'a': 4, 'w': 1.25}, 'AltGr', {'w': 1.25}, ['Win__R', 'Key_RightWindows'], {'w': 1.25}, 'Menu', {'w': 1.25}, ['Ctrl__R', 'Key_RightControl'],
            {'x': 0.25}, ['←', 'Key_LeftArrow'], ['↓', 'Key_DownArrow'], ['→', 'Key_RightArrow'], {'x': 0.25, 'w': 2}, ['0__N\nIns__N', 'Key_Numpad_0'], ['.__N\nDel__N', 'Key_Numpad_Decimal']],
    ],
    'ЙЦУКЕН': [
        ['Esc', {'x': 1}, 'F1', 'F2', 'F3', 'F4', {'x': 0.5}, 'F5', 'F6', 'F7', 'F8', {'x': 0.5}, 'F9', 'F10', 'F11', 'F12', {'x': 0.25}, 'PrtSc', ['ScrLk', 'Key_ScrollLock'], ['Pause\nBreak', 'Key_Pause']],
        [{'y': 0.5}, ['Ё\n`', 'Key_Grave'], ['!\n1', 'Key_1'], ['"\n2', 'Key_2'], ['№\n3', 'Key_3'], ['4', 'Key_4'], ['%\n5', 'Key_5'], [':\n6', 'Key_6'], ['?\n7', 'Key_7'], ['*\n8', 'Key_8'], ['(\n9', 'Key_9'], [')\n0', 'Key_0'], ['_\n-', 'Key_Minus'], ['+\n=', 'Key_Equals'], {'w': 2}, 'Backspace',
            {'x': 0.25}, 'Insert', 'Home', ['PgUp', 'Key_PageUp'], {'x': 0.25}, ['Num Lock', 'Key_NumLock'], ['/__N', 'Key_Numpad_Divide'], ['*__N', 'Key_Numpad_Multiply'], ['-__N', 'Key_Numpad_Subtract']],
        [{'w': 1.5}, 'Tab', 'Й', 'Ц', 'У', 'К', 'Е', 'Н', 'Г', 'Ш', 'Щ', 'З', ['Х\n[', 'Key_LeftBracket'], ['Ъ\n]', 'Key_RightBracket'], {'x': 0.25, 'w': 1.25, 'h': 2, 'w2': 1.5, 'h2': 1, 'x2': -0.25}, 'Enter',
            {'x': 0.25}, 'Delete', 'End', ['PgDn', 'Key_PageDown'], {'x': 0.25}, ['7__N\nHome__N', 'Key_Numpad_7'], ['8__N\n↑', 'Key_Numpad_8'], ['9__N\nPgUp__N', 'Key_Numpad_9'], {'h': 2}, ['+__N', 'Key_Numpad_Add']],
        [{'w': 1.75}, ['Caps Lock', 'Key_CapsLock'], 'Ф', 'Ы', 'В', 'А', 'П', 'Р', 'О', 'Л', 'Д', ['Ж\n;', 'Key_SemiColon'], ['Э\n\'', 'Key_Apostrophe'], ['\\\n|', 'Key_Slash'],
            {'x': 4.75}, ['4__N\n←', 'Key_Numpad_4'], ['5__N', 'Key_Numpad_5'], ['6__N\n→', 'Key_Numpad_6']],
        [{'w': 1.25}, ['Shift__L', 'Key_LeftShift'], ['\\\n/', 'Key_BackSlash'], 'Я', 'Ч', 'С', 'М', 'И', 'Т', 'Ь', ['Б\n,', 'Key_Comma'], ['Ю\n.', 'Key_Period'], ['.\n/', 'Key_Period'], {'w': 2.75}, ['Shift__R', 'Key_RightShift'],
            {'x': 1.25}, ['↑', 'Key_UpArrow'], {'x': 1.25}, ['1__N\nEnd__N', 'Key_Numpad_1'], ['2__N\n↓', 'Key_Numpad_2'], ['3__N\nPgDn__N', 'Key_Numpad_3'], {'h': 2}, ['Enter__N', 'Key_Numpad_Enter']],
        [{'w': 1.25}, ['Ctrl__L', 'Key_LeftControl'], {'w': 1.25}, ['Win__L', 'Key_LeftWindows'], {'w': 1.25}, ['Alt__L', 'Key_LeftAlt'], {'a': 7, 'w': 6.25}, [' ', 'Key_Space'], {'a': 4, 'w': 1.25}, 'AltGr', {'w': 1.25}, ['Win__R', 'Key_RightWindows'], {'w': 1.25}, 'Menu', {'w': 1.25}, ['Ctrl__R', 'Key_RightControl'],
            {'x': 0.25}, ['←', 'Key_LeftArrow'], ['↓', 'Key_DownArrow'], ['→', 'Key_RightArrow'], {'x': 0.25, 'w': 2}, ['0__N\nIns__N', 'Key_Numpad_0'], ['.__N\nDel__N', 'Key_Numpad_Decimal']],
    ],
}
