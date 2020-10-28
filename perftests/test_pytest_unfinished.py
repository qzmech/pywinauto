import pytest

import os, sys
from time import sleep

sys.path.insert(1, os.path.join(os.path.abspath('..'), '..', "github", "pywinauto"))
import pywinauto
import pywinauto.actionlogger
print(pywinauto.__file__)
from pywinauto.application import Application
from pywinauto.timings import wait_until

#cwd = os.getcwd()
#os.chdir(r"..\..\github\pywinauto")
#os.system('git status')
#os.chdir(cwd)

def setup_module():
    pywinauto.actionlogger.enable()
    global app, dlg
    app = Application(backend="uia")
    app.start(r"mainwindow.exe")
    dlg = app.window(name="Qt Main Window Example")
    
def teardown_module():
    app.kill()
    
@pytest.mark.skip
def test_print():
    dlg = app.window(name="Dolphin 5.0-9281")
    # TODO mock
    dlg.print_control_identifiers(depth=3)
    
def test_perf_children(benchmark):
    #res = benchmark.pedantic(dlg.children)
    res = benchmark(dlg.children)
    assert len(res) > 0
    
def test_perf_desc_3(benchmark):
    # res = benchmark.pedantic(dlg.children)
    res = benchmark(dlg.descendants, depth=3)
    assert len(res) > 0

def test_perf_desc_unlim(benchmark):
    # res = benchmark.pedantic(dlg.children)
    res = benchmark(dlg.descendants)
    assert len(res) > 0