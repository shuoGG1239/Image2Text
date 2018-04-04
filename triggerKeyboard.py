from pykeyboard import PyKeyboardEvent
import time
from threading import Thread

"""
    shuoGG: 本模块只公开key_trigger接口(装饰器)
    eg:
        @key_trigger('ctrl+shift+alt+f8', True) 具体见main函数
"""


def key_trigger(key_str, is_trigger_once=True):
    """
    @装饰器key_trigger
    :param key_str: 快捷键
    :param is_trigger_once: 是否只触发一次
    :return:
    """
    def new_func(func):
        def decorate(*args, **kwargs):
            keyboard_event_thread = Thread(target=__run_keyboard_task, args=(key_str,))
            keyboard_event_thread.setDaemon(is_trigger_once)  # setDaemon(True) --> 主线程挂了则t1跟着挂
            keyboard_event_thread.start()
            global is_key_triggered
            while True:
                if is_key_triggered:
                    is_key_triggered = False
                    func(*args, **kwargs)
                    if is_trigger_once:
                        break
                time.sleep(0.01)

        return decorate

    return new_func

# 用于通知
is_key_triggered = False


def __run_keyboard_task(key_str):
    """
    异步任务: 跑键盘监听任务
    :param key_str:
    :return:
    """
    if TriggerKeyboardEvent.check_key_str(key_str) is False:
        raise NameError('快捷键格式错误')
    p = TriggerKeyboardEvent(key_str)
    p.run()


class TriggerKeyboardEvent(PyKeyboardEvent):
    def __init__(self, key_str='ctrl+shift+alt+f8'):
        PyKeyboardEvent.__init__(self)
        self.key_map = TriggerKeyboardEvent.create_key_map(TriggerKeyboardEvent.parse_full_key_str(key_str))
        self.is_trigger = False

    def run(self):
        super().run()

    def tap(self, keycode, character, press):
        """
        @Override
        :param keycode:
        :param character:
        :param press:
        :return:
        """
        global is_key_triggered
        # print(keycode, character, press)
        character = TriggerKeyboardEvent.to_standard_str(character)
        if character in self.key_map:
            self.key_map[character] = press
        if TriggerKeyboardEvent.check_all_key_pressed(self.key_map):
            is_key_triggered = True

    @staticmethod
    def parse_full_key_str(key_str):
        """
        快捷键串分解成列表
        :param key_str:
        :return: list
        """
        keys = list(map(lambda x: x.strip(), key_str.split('+')))
        return keys

    @staticmethod
    def create_key_map(key_list):
        """
        建立按键辅助表: key为键盘某按钮字符串 value为初始均为False
        :param key_list:
        :return: dict
        """
        key_map = dict()
        for key in key_list:
            key_map[key] = False
        return key_map

    @staticmethod
    def check_all_key_pressed(key_map):
        """
        检查键盘辅助表所有项是否均为True
        :param key_map:
        :return: bool
        """
        for key in key_map.keys():
            if key_map[key] is False:
                return False
        return True

    @staticmethod
    def to_standard_str(character):
        """
        tap回调传进来的character格式不标准,需要转一下
        :param character:
        :return: str
        """
        if character.find('CONTROL') > -1:
            return 'ctrl'
        if character.find('MENU') > -1:
            return 'alt'
        if character.find('SHIFT') > -1:
            return 'shift'
        return character.lower()

    @staticmethod
    def check_key_str(key_str):
        """
        检验输入的快捷键格式是否合法
        :param key_str: eg: 'ctrl+shift+f1'
        :return: bool
        """
        key_list = TriggerKeyboardEvent.parse_full_key_str(key_str)
        sp_key_count = 0
        if len(key_list) < 1:
            return False
        for key in key_list:
            if key.lower() == 'ctrl':
                sp_key_count += 1
            if key.lower() == 'alt':
                sp_key_count += 1
            if key.lower() == 'shift':
                sp_key_count += 1
        if len(key_list) - sp_key_count > 1:
            return False
        else:
            return True


if __name__ == '__main__':
    @key_trigger('ctrl+shift+alt+f9', False)
    def test():
        print('shuoGG')


    test()
