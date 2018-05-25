# coding=utf-8

import win32gui
import win32con


class FileUpload:

    # window_class = '#32770'
    # window_caption = u'选择要上载的文件自 devmycis.synnex.org'

    def __init__(self, logger):
        self.logger = logger

    @staticmethod
    def upload(window_class, window_caption, file_name):
        # 获取对话框
        window = win32gui.FindWindow(window_class, window_caption)
        combo_box_ex32 = win32gui.FindWindowEx(window, 0, 'ComboBoxEx32', None)
        combo_box = win32gui.FindWindowEx(combo_box_ex32, 0, 'ComboBox', None)
        # 输入框Edit对象的句柄
        edit_button = win32gui.FindWindowEx(combo_box, 0, 'Edit', None)
        # 确定按钮Button
        commit_button = win32gui.FindWindowEx(window, 0, 'Button', None)

        # 往输入框输入文件的绝对路径
        win32gui.SendMessage(edit_button, win32con.WM_SETTEXT, None, file_name)
        # 按button
        win32gui.SendMessage(window, win32con.WM_COMMAND, 1, commit_button)

    @staticmethod
    def has_upload_window(window_class, window_caption):
        return win32gui.FindWindow(window_class, window_caption) > 0


if __name__ == '__main__':
    FileUpload.has_upload_window('#32770', '选择要上载的文件，通过: testmycis.synnex.org')
