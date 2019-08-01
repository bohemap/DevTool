import pywinauto.application as app
import pywinauto.findwindows as finder

eclipse = finder.find_element(title_re="eclipse.* - Eclipse IDE", found_index=0)
eclipse_app = app.Application(backend="uia").connect(process = eclipse.process_id)
eclipse_window = eclipse_app.window()

eclipse_window.child_window(title="File", control_type="MenuItem").click_input()
eclipse_window.child_window(title="Export...", control_type="MenuItem", ctrl_index=0).click_input()

export = finder.find_element(title="Export")
export_app = app.Application(backend="uia").connect(process = export.process_id)
export_window = export_app.window()

export_window.child_window(title="type filter text", control_type="Edit").set_text("Deployable plug-ins and fragments")
export_window.child_window(title="Deployable plug-ins and fragments", control_type="TreeItem").click_input(double=True)
export_window.child_window(title="type filter text", control_type="Edit").set_text("crossgcc")
export_window.child_window(title_re=".*crossgcc.*", control_type="CheckBox").click_input(double=True)
eclipse_window.child_window(title="Browse...", control_type="Button", ctrl_index=0).click_input()
eclipse_window.child_window(title="Folder:", control_type="Edit").set_text("C:\Renesas\e2_studio\eclipse")
eclipse_window.child_window(title="Select Folder", control_type="Button").click_input()
export_window.child_window(title="Options", control_type="TabItem").click_input()
qualifier = export_window.child_window(title="Qualifier replacement (default value is today's date):", control_type="CheckBox")
qualifier_edit = export_window.child_window(control_type="Edit", ctrl_index=1)

if not qualifier_edit.is_enabled():
    qualifier.click_input()

from os import listdir
from os.path import isfile, join
mypath = "C:\Renesas\e2_studio\eclipse\plugins"
for f in listdir(mypath):
    if isfile(join(mypath, f)) and f.startswith("com.renesas.smc.tools.summary"):
        target_qualifier = "v" + f.split(".v")[1].replace(".jar","")

qualifier_edit.set_text(target_qualifier)
export_window.child_window(title="Finish", control_type="Button").click_input()

