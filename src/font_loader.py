import os
import sys
import dearpygui.dearpygui as imgui

MAIN_FONT: int | str = ''
HEADLINE_FONT: int | str = ''

big_let_start = 0x00C0
big_let_end = 0x00DF
small_let_end = 0x00FF
remap_big_let = 0x0410

alph_len = big_let_end - big_let_start + 1
alph_shift = remap_big_let - big_let_start

def load(font_path: str):
    with imgui.font_registry():
        with imgui.font(os.path.join(font_path, 'JetBrainsMono-Medium.ttf'), 18) as main_font:
            imgui.add_font_range_hint(imgui.mvFontRangeHint_Default)
            imgui.add_font_range_hint(imgui.mvFontRangeHint_Cyrillic)

            imgui.add_font_range(0x0391, 0x03C9)
            imgui.add_font_range(0x2070, 0x209F)

            if sys.platform == 'win32':
                _remap_chars()

    return main_font


def _remap_chars():
    biglet = remap_big_let
    for i1 in range(big_let_start, big_let_end + 1):
        imgui.add_char_remap(i1, biglet)
        imgui.add_char_remap(i1 + alph_len, biglet + alph_len)
        biglet += 1
    imgui.add_char_remap(0x00A8, 0x0401)
    imgui.add_char_remap(0x00B8, 0x0451)