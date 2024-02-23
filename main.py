import os

import dearpygui.dearpygui as imgui
import xdialog

from loguru import logger
from PIL import Image

import src.font_loader as fl
import src.bytes_data as bd

RESOURCES = os.path.abspath('resources')
LOGS = os.path.abspath('logs')

logger_format = '[{time} | {level:10}]: {message}'
logger.add(os.path.join(LOGS, 'debug.log'), format=logger_format, rotation='1 MB', compression='zip')


if __name__ == '__main__':
    if not os.path.exists(RESOURCES):
        os.makedirs(RESOURCES)

    font_path = os.path.join(RESOURCES, 'JetBrainsMono-Medium.ttf')
    if not os.path.exists(font_path):
        with open(font_path, 'wb') as w_font:
            w_font.write(bd.jetbrainsmono_medium)

    icon_path = os.path.join(RESOURCES, 'icon.ico')
    if not os.path.exists(icon_path):
        with open(icon_path, 'wb') as w_icon:
            w_icon.write(bd.icon)


def get_images_data(folder_path):
    logger.info('Start function: get images data')
    r: list[dict] = []
    t: list = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if not os.path.isfile(file_path):
            continue

        if file_name.split('.')[1] != 'png':
            continue

        logger.debug(file_name)

        with Image.open(file_path) as img:
            width, height = img.size

        if width >= 1620 or height >= 2160:
            t.append(
                f"filename: {file_name},\n\tsize: ({width}, {height}),\n\tfile_path: {file_path},\n\tabs_file_path: {os.path.abspath(file_path)}\n")

        r.append({'name': file_name.split('.')[0], 'width': width, 'height': height, 'tooltip': ''})

    return r, t


def write_table(data: list[dict[str, int, int, str]], output_path: str, name_file: str, override: bool = False):
    logger.info(f"Start function: write \"{name_file}.lua\".")
    file_path = os.path.join(output_path, f"{name_file}.lua")
    if os.path.exists(file_path):
        if override:
            os.remove(file_path)
        else:
            raise FileExistsError()

    with open(file_path, 'w', encoding='utf-8') as f_out:
        f_out.write('Emojis = {\n')

        for item in data:
            f_out.write(
                f"\t{{ name = \"{item.get('name')}\", width = {item.get('width')}, height = {item.get('height')}, tooltip = \"{item.get('tooltip')}\" }}\n")

        f_out.write('}')
    logger.info(f"Stop function: write \"{name_file}.lua\".")

def write_data(data: list[str], output_path: str, override: bool = False):
    logger.info('Start function: write "large_imaget.log".')
    file_path = os.path.join(output_path, 'large_images.log')
    if os.path.exists(file_path):
        if override:
            os.remove(file_path)
        else:
            raise FileExistsError()

    with open(file_path, 'w', encoding='utf-8') as f_out:
        for item in data:
            f_out.write(item)

    logger.info('Stop function: write "large_imaget.log".')


def primary_window():
    def __smart_convert_text(text: str):
        symbols_to_replace = "éöóêåíãøùçõúýæäëîðïàâûôÿ÷ñìèòüáþ¸ÉÖÓÊÅÍÃØÙÇÕÚÝÆÄËÎÐÏÀÂÛÔß×ÑÌÈÒÜÁÞ¨"
        replacement_dict = {
            cp1252_char: cp1252_char.encode('cp1252').decode('cp1251')
            for cp1252_char in symbols_to_replace
        }
        for cp1252_char, cp1251_char in replacement_dict.items():
            text = text.replace(cp1252_char, cp1251_char)
        return text

    def __catch_file_exists(func, title: str, message: str):
        try:
            func()
            return True
        except FileExistsError as e:
            logger.catch(e)
            xdialog.error(title, message)
            return False
        except Exception as e:
            logger.catch(e)
            return False

    def _set_path(sender, app_data, user_data):
        path = xdialog.directory('Select folder...')
        if path is None: return
        imgui.set_value(user_data, path)

    def _create_table(sender, app_data, user_data):
        s1: str = imgui.get_value(user_data[0])
        s2: str = imgui.get_value(user_data[1])
        s3: str = imgui.get_value(user_data[2])

        override: bool = imgui.get_value(user_data[3])

        input_path = __smart_convert_text(s1)
        output_path = __smart_convert_text(s2)
        output_name = __smart_convert_text(s3)

        logger.debug(input_path)
        logger.debug(output_path)
        logger.debug(output_name)

        if not os.path.isdir(input_path):
            logger.warning('The provided path to the input folder is invalid.')
            xdialog.error('Path error', 'The provided path to the input folder is invalid.')
            return

        if not os.path.isdir(output_path):
            logger.warning('The provided path to the output folder is invalid.')
            xdialog.error('Path error', 'The provided path to the output folder is invalid.')
            return

        table, data = get_images_data(input_path)

        if table is None or len(table) <= 0:
            logger.error(f'No files found in the folder.')
            xdialog.error('File(s) error', 'No files found in the folder.')

        if not __catch_file_exists(lambda: write_table(table, output_path, output_name, override), 'File exists', 'The lua file of the table already exists.'):
            return
        if not __catch_file_exists(lambda: write_data(data, LOGS, True), 'File exists', 'The image log file already exists.'):
            return

        if len(data) > 0:
            xdialog.warning('The image(s) are large.', 'Large size image(s) found. Width is greater than 1620 pixels or height is greater than 2160 pixels.\nWe recommend reducing the size of the images.\nMore details in the log file large_images.log')

        xdialog.info('File created', 'It is ok.')

    with imgui.window(label='Primary window') as window:
        with imgui.group(horizontal=True):
            input_text = imgui.add_input_text(label='Input path', tag='input-path-id', width=-150)
            imgui.add_button(label='...', callback=_set_path, user_data='input-path-id')
        with imgui.group(horizontal=True):
            output_text = imgui.add_input_text(label='Output path', tag='output-path-id', width=-150)
            imgui.add_button(label='...', callback=_set_path, user_data='output-path-id')
        imgui.add_spacer(height=2)
        imgui.add_separator()
        imgui.add_spacer(height=2)
        with imgui.tree_node(label='Advanced'):
            override = imgui.add_checkbox(label='Override file')
            name_out_file = imgui.add_input_text(label='Name lua file', tag='name-out-file-id', default_value='outtable')
        with imgui.child_window(height=-30, border=False):
            imgui.add_text()
        imgui.add_button(label='Create lua table', callback=_create_table, user_data=[input_text, output_text, name_out_file, override])

    return window

@logger.catch
def _start():
    logger.info('Start App!')
    imgui.create_context()

    main_font = fl.load(RESOURCES)
    imgui.bind_font(main_font)

    imgui.set_primary_window(primary_window(), True)

    imgui.configure_app(docking=False, docking_space=False)
    imgui.create_viewport(title='Image Sequencer', clear_color=(16, 16, 16), width=640, height=480, resizable=False)

    imgui.set_viewport_small_icon(os.path.join(RESOURCES, 'icon.ico'))
    imgui.set_viewport_large_icon(os.path.join(RESOURCES, 'icon.ico'))

    imgui.setup_dearpygui()

    imgui.show_viewport()
    imgui.start_dearpygui()
    imgui.destroy_context()
    logger.info('Stop App!')


if __name__ == '__main__':
    _start()