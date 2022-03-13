"""Implementation of the class to deal with an UI element of WPF via injected DLL"""
import json

from six import integer_types, text_type, string_types
from ctypes.wintypes import tagPOINT
import warnings

from pywinauto.handleprops import dumpwindow, controlid
from pywinauto.element_info import ElementInfo
from .win32structures import RECT
from .injector import main, channel

pipes= {}

class WPFElementInfo(ElementInfo):
    re_props = ["class_name", "name", "auto_id", "control_type", "full_control_type", "access_key", "accelerator",
                "value"]
    exact_only_props = ["handle", "pid", "control_id", "enabled", "visible", "rectangle", "framework_id", "runtime_id"]
    search_order = ["handle", "control_type", "class_name", "pid", "control_id", "visible", "enabled", "name",
                    "access_key", "accelerator", "auto_id", "full_control_type", "rectangle", "framework_id",
                    "runtime_id", "value"]
    assert set(re_props + exact_only_props) == set(search_order)

    def __init__(self, elem_id=None, cache_enable=False, pid=None):
        """
        Create an instance of WPFElementInfo from an ID of the element (int or long).

        If elem_id is None create an instance for UI root element.
        """
        self._pid=pid
        if elem_id is not None:
            if isinstance(elem_id, integer_types):
                # Create instance of WPFElementInfo from a handle
                self._element = elem_id
            else:
                raise TypeError("WPFElementInfo object can be initialized " + \
                                "with integer instance only!")
        else:
            self._element = 0

        self.set_cache_strategy(cached=cache_enable)

    @property
    def pipe(self):
        if self._pid is not None and self._pid not in pipes:
            pipes[self._pid] = main.create_pipe(self._pid)
        return pipes[self._pid]

    def set_cache_strategy(self, cached):
        pass

    @property
    def handle(self):
        return 0

    @property
    def name(self):
        command = f"{json.dumps({'action': 'GetProperty', 'element_id': self._element, 'name': 'Name'})}\n"
        reply = self.pipe.transact(command)
        reply = json.loads(reply)
        return reply['value']

    @property
    def rich_text(self):
        return self.name
        #return ''

    @property
    def control_id(self):
        return self._element

    @property
    def process_id(self):
        return self._pid

    pid = process_id

    @property
    def framework_id(self):
        return "WPF"

    @property
    def class_name(self):
        command = f"{json.dumps({'action': 'GetTypeName', 'element_id': self._element})}\n"
        reply = self.pipe.transact(command)
        reply = json.loads(reply)
        return reply['value']

    @property
    def enabled(self):
        return True

    @property
    def visible(self):
        return True

    @property
    def parent(self):
        return None

    def children(self, **kwargs):
        return list(self.iter_children(**kwargs))

    @property
    def control_type(self):
        """Return control type of element"""
        return None

    def iter_children(self, **kwargs):
        if 'process' in kwargs:
            self._pid = kwargs['process']
        command = f"{json.dumps({'action': 'GetChildren', 'element_id': self._element})}\n"
        reply = self.pipe.transact(command)
        reply = json.loads(reply)
        for elem in reply['elements']:
            yield WPFElementInfo(elem, pid=self._pid)


    def descendants(self, **kwargs):
        return list(self.iter_descendants(**kwargs))

    def iter_descendants(self, **kwargs):
        cache_enable = kwargs.pop('cache_enable', False)
        depth = kwargs.pop("depth", None)
        if not isinstance(depth, (integer_types, type(None))) or isinstance(depth, integer_types) and depth < 0:
            raise Exception("Depth must be an integer")

        if depth == 0:
            return
        for child in self.iter_children(**kwargs):
            yield child
            if depth is not None:
                kwargs["depth"] = depth - 1
            for c in child.iter_descendants(**kwargs):
                yield c

    @property
    def rectangle(self):
        return RECT()

    def dump_window(self):
        return {}