import maya.cmds as cmds
from functools import partial
import json
import re

# Convert the switcher array into a json string and save it to the tool group in the scene
def save_rows():

    if not cmds.objExists(const_group_name):
        const_group = cmds.group(em=True, name=const_group_name)
    
    if not cmds.attributeQuery('nb_Constraint_Row_SaveData', node=const_group_name, exists=True):
        cmds.addAttr(const_group_name, longName='nb_Constraint_Row_SaveData', dt='string')
        cmds.setAttr(const_group_name + '.nb_Constraint_Row_SaveData', lock=True)

    json_string = json.dumps(switcher_array)
    at = const_group_name + '.nb_Constraint_Row_SaveData'
    cmds.setAttr(at, lock=False)
    cmds.setAttr(at, json_string, type='string')
    cmds.setAttr(at, lock=True)

# Return a part of the attr string - either the object name, attribute name or constraint name
def split_attr_parts(attr, part_index):

    if '.' in attr:
        parts = attr.rsplit('.', 2)
        return parts[part_index] if part_index is not None else None
   
# Iterate through all nodes in the scene with custom enum attributes and populate the find tab   
def find_cust_attr(*args):

    # Find custom attributes in the scene and format them
    nodes = cmds.ls(type='transform') or []
    enum_attributes = {}
    if nodes:
        for node in nodes:
            custom_attributes = cmds.listAttr(node, userDefined=True) or []
            for attr in custom_attributes:
                attr_type = cmds.attributeQuery(attr, node=node, attributeType=True)
                if attr_type == 'enum':
                    enum_values = cmds.attributeQuery(attr, node=node, listEnum=True) or []
                    enum_values_split = [value.strip() for value in enum_values[0].split(':')]
                    enum_attributes[node + '.' + attr] = enum_values_split
    
    # Clear the find tab so it can be repopulated correctly
    children = cmds.columnLayout(find_scroll_column, q=True, childArray=True)
    if children:
        for child in children:
            cmds.deleteUI(child)
        
    # Call functions to populate the find tab based on the information in the switcher_array
    if enum_attributes:
        for attr, items in enum_attributes.items():
            if len(switcher_array) > 0:
                found_match = False
                for dict in switcher_array:
                    if dict['Attribute'] == attr:
                        found_match = True
                        break
                if not found_match:
                    populate_found_rows(attr, items)
            else: 
                populate_found_rows(attr, items)
 
# Return the most likely match of a constraint in the scene to an object by comparing string lengths
def string_match(input_string):

    objects = cmds.ls(dag=True)
    longest_match_object = None
    longest_match_length = 0
    
    for obj in objects:
        for i in range(len(obj)):
            for j in range(i + 1, len(obj) + 1):
                substring = obj[i:j]
                if substring in input_string and len(substring) > longest_match_length:
                    node_type = cmds.nodeType(obj)
                    constraint_types = ["pointConstraint", "orientConstraint", "scaleConstraint", "aimConstraint", "parentConstraint"]
                    if node_type in constraint_types:
                        longest_match_length = len(substring)
                        longest_match_object = obj     
    return longest_match_object
 
# Populate the find tab with any custom attributes in the scene that aren't saved in the Switch tab
def populate_found_rows(attr, items):

    obj = split_attr_parts(attr, 0)
    attr_long = attr
    attr = split_attr_parts(attr, 1)
    attr = obj + '.' + attr
    current_value = cmds.getAttr(attr)
    value_array = []
    
    # Row UI
    cmds.setParent(find_scroll_column)
    found_row_separator = cmds.separator(height=7, style='none') 
    found_row = cmds.rowLayout(numberOfColumns=5, cl5=["left", "left", "right", "right", "right"])
    row_name = cmds.text(label=attr, w=100, annotation=attr, align='left')
    row_name_length = cmds.text(row_name, q=True, label=True)
    if len(row_name_length) >= 18:
        cmds.text(label="... ")
    else:
        cmds.text(label="    ")
    option_menu = cmds.optionMenu(bgc=[0.35, 0.35, 0.35], w=76)
    for item in items:
        cmds.menuItem(label=item)
        value_array.append(str(item))
    cmds.optionMenu(option_menu, edit=True, value=value_array[current_value])
    cmds.separator(width=2, style="none")
    add_button = cmds.button(label="Add", bgc=[0.35, 0.35, 0.35], h=20)
    cmds.button(add_button, e=True, command=lambda x: disable_add(attr_long, items, found_row, found_row_separator, switcher_label=None), annotation='Add this attribute to the Switch tab')
    cmds.setParent('..')

# Called when a find row is added. Gets the constraint and adds the attribute to the switch tab. IMPORTANT: Deleting the row ui must be called using cmds.evalDeferred
def disable_add(attr_long, items, found_row, found_row_separator, switcher_label=None):

    constraint = cmds.listConnections(attr_long)
    if constraint:
        constraint = string_match(constraint[0])
        attr = attr_long + '.' + constraint
    else:
        attr = attr + '.None'
    deferred_delete = partial(delete_found, found_row, found_row_separator)
    cmds.evalDeferred(deferred_delete)
    add_existing_attr(attr, items, switcher_label)

# Delete the find row that was added
def delete_found(found_row, found_row_separator):

    cmds.deleteUI(found_row, found_row_separator)
   
# Clear the switch tab and repopulate it using info from the switcher array
def refresh_switch_tab(*args):

    children = cmds.columnLayout(switch_scroll_column, q=True, childArray=True)
    if children:
        for child in children:
            cmds.deleteUI(child)
            
    for item in switcher_array:
        attr = item['Attribute']
        items = item['Items']
        label = item['Label']
        const = item['Constraint']
        simplecheck = split_attr_parts(attr, 1)
        if cmds.objExists(attr) or simplecheck:
            attr = attr + '.' + const
            if simplecheck != 'nbTempSimpleSwitcher':
                add_existing_attr(attr, items, label)
            else:
                add_simple_attr(attr, const, items, label)
        else:
            switcher_array.remove(item)
            
# Populate the Switch tab with rows based on the saved switcher_array, for any items that are simple switchers
def add_simple_attr(attr, const, items, switcher_label):

    cmds.setParent(switch_scroll_column)
    obj = split_attr_parts(attr, 0)
    weight_attr = cmds.parentConstraint(const, q=True, wal=True)  
    current_active_constraint = 0
    for index, item in enumerate(weight_attr):
        if cmds.getAttr(const + '.' + item) == 1:
            current_active_constraint = index + 1
            break
    value_array = []
    
    # Row UI
    switch_row_separator = cmds.separator(height=7, style='none')
    switch_row = cmds.rowLayout(numberOfColumns=6, cl6=["left", "left", "right", "right", "right", "right"], ct6=['right', 'right', 'right', 'right', 'right', 'right'], columnAttach=[(4, 'both', -2), (5, 'both', -2)], height=20, rat=([1, 'both', 0], [2, 'both', 0], [4, 'both', -5], [5, 'both', -5], [6, 'both', -2]))
    if switcher_label is None:
        switcher_label = attr
    if len(switcher_label) >= 18:
        cmds.text(label="  ...")
    else:
        cmds.text(label="     ")
    switch_attr_text = cmds.text(label=switcher_label, w=100, annotation=attr, h=19, al='right', bgc=[0.17, 0.17, 0.17])
    cmds.separator(width=5, style="none")
    int_field = cmds.intField(value=0, width=8, height=30, editable=False, enable=False)
    int_field2 = cmds.intField(value=0, width=5, height=30, editable=False, enable=False)
    cmds.connectControl(int_field, const + '.' + weight_attr[0])
    cmds.connectControl(int_field2, const + '.' + weight_attr[0])
    option_menu = cmds.optionMenu(bgc=[0.35, 0.35, 0.35], w=94, h=21)
    cmds.intField(int_field, e=True, rfc=lambda *args: refocus(switch_row, *args))
    cmds.intField(int_field2, e=True, rfc=lambda *args: refocus(switch_row, *args))
    
    for index, item in enumerate(items):
        cmds.menuItem(label=item, data=index)
        value_array.append(str(item)) 
        
    cmds.optionMenu(option_menu, edit=True, select=current_active_constraint + 1)
    cmds.optionMenu(option_menu, edit=True, changeCommand=lambda x: set_keyframe(attr, option_menu, items))
    cmds.popupMenu()
    cmds.menuItem(label='Key', command=lambda x: set_keyframe(attr, option_menu, items, manual=True))
    cmds.menuItem(label='Select Control', command=lambda x: sel_control(obj))
    cmds.menuItem(label='Select Attribute', command=lambda x: sel_attribute(attr))
    cmds.menuItem(label='Select Constraint', command=lambda x: sel_constraint(const))
    cmds.menuItem(label='Rename', command=lambda x: rename_tool(attr, items, switcher_label, option_menu))
    cmds.menuItem(label='Delete Switcher', command=lambda x: delete_attr(switch_attr_text, attr, switch_row, switch_row_separator))
    
    callback = partial(time_changed_callback, option_menu, const)
    timeJob = cmds.scriptJob(event=["timeChanged", callback], parent=switch_row)
    
    switcher_list = {'Attribute': obj + '.nbTempSimpleSwitcher', 'Items': items, 'Label': switcher_label, 'Constraint': const}
    if switcher_list not in switcher_array:
        switcher_array.append(switcher_list)
        save_rows()

# Populate the Switch tab with rows based on the saved switcher_array, for any real enums
def add_existing_attr(attr, items, switcher_label):

    cmds.setParent(switch_scroll_column)
    obj = split_attr_parts(attr, 0)
    attr_long = attr
    attr = split_attr_parts(attr, 1)
    attr = obj + '.' + attr
    const = split_attr_parts(attr_long, 2)
    current_value = cmds.getAttr(attr)
    value_array = []
    
    # Row UI
    switch_row_separator = cmds.separator(height=7, style='none')
    switch_row = cmds.rowLayout(numberOfColumns=6, cl6=["left", "left", "right", "right", "right", "right"], ct6=['right', 'right', 'right', 'right', 'right', 'right'], columnAttach=[(4, 'both', -2), (5, 'both', -2)], height=20, rat=([1, 'both', 0], [2, 'both', 0], [4, 'both', -5], [5, 'both', -5], [6, 'both', -2]))
    if switcher_label is None:
        switcher_label = attr
    if len(switcher_label) >= 18:
        cmds.text(label="  ...")
    else:
        cmds.text(label="     ")
    switch_attr_text = cmds.text(label=switcher_label, w=100, annotation=attr, h=19, al='right', bgc=[0.17, 0.17, 0.17])
    cmds.separator(width=5, style="none")
    int_field = cmds.intField(value=0, width=8, height=30, editable=False, enable=False)
    int_field2 = cmds.intField(value=0, width=5, height=30, editable=False, enable=False)
    cmds.connectControl(int_field, attr)
    cmds.connectControl(int_field2, attr)
    option_menu = cmds.optionMenu(bgc=[0.35, 0.35, 0.35], w=94, h=21)
    cmds.intField(int_field, e=True, rfc=lambda *args: refocus(switch_row, *args))
    cmds.intField(int_field2, e=True, rfc=lambda *args: refocus(switch_row, *args))
    
    for index, item in enumerate(items):
        cmds.menuItem(label=item, data=index)
        value_array.append(str(item))
        
    cmds.optionMenu(option_menu, edit=True, value=value_array[current_value])
    cmds.optionMenu(option_menu, edit=True, changeCommand=lambda x: set_keyframe(attr, option_menu, items))
    cmds.popupMenu()
    cmds.menuItem(label='Key', command=lambda x: set_keyframe(attr, option_menu, items, manual=True))
    cmds.menuItem(label='Select Control', command=lambda x: sel_control(obj))
    cmds.menuItem(label='Select Attribute', command=lambda x: sel_attribute(attr))
    cmds.menuItem(label='Select Constraint', command=lambda x: sel_constraint(const))
    cmds.menuItem(label='Rename', command=lambda x: rename_tool(attr, items, switcher_label, option_menu))
    cmds.menuItem(label='Delete Switcher', command=lambda x: delete_attr(switch_attr_text, attr, switch_row, switch_row_separator))
    
    cmds.connectControl(option_menu, attr)

    switcher_list = {'Attribute': attr, 'Items': items, 'Label': switcher_label, 'Constraint': const}
    if switcher_list not in switcher_array:
        switcher_array.append(switcher_list)
        save_rows()
 
# Change the focus of the UI off of the keyticks if they are selected
def refocus(switch_row, *args):

        cmds.setFocus(switch_row)

# Update the simpleswitcher optionmenu when time is changed to ensure its selected item is accurate.
def time_changed_callback(option_menu, const, *args):

    weight_attr = cmds.parentConstraint(const, q=True, wal=True)  
    current_active_constraint = 0
    for index, item in enumerate(weight_attr):
        if cmds.getAttr(const + '.' + item) == 1:
            current_active_constraint = index + 1
            break
    cmds.optionMenu(option_menu, edit=True, select=current_active_constraint + 1)

# Delete a switcher from the switch tab, removing its UI (again, call it deferred to prevent crashes) and removing it from the switcher array
def delete_attr(switch_attr_text, attr, switch_row, switch_row_separator):

    confirm = cmds.confirmDialog(message="Are you sure you want to remove '" + cmds.text(switch_attr_text, q=1, label=1) + "'?     ", title='Warning', button=['Yes','Cancel'], defaultButton='Yes', cancelButton='No', dismissString='No', p=win)
    
    if confirm == 'Yes':
        simplecheck = split_attr_parts(attr, 1)
        if simplecheck == 'nbTempSimpleSwitcher':
            attr = split_attr_parts(attr, 0) + '.' + simplecheck
        for dict in switcher_array:
            if dict['Attribute'] == attr:
                switcher_array.remove(dict)
                save_rows()
                break
        cmds.evalDeferred(refresh_switch_tab)
        find_cust_attr()
    else:
        return

# Check what's needed to set a keyframe (or multiple) for either a regular enum switcher or a simple switcher, then call the key frames function
def set_keyframe(attr, option_menu, items, manual=None):

    simplecheck = split_attr_parts(attr, 1)
    simple = False
    if simplecheck == 'nbTempSimpleSwitcher':
        simple = True
    selected_item = cmds.optionMenu(option_menu, query=True, value=True)
    if not manual and not simple:
        cmds.undo()
    current_frame = cmds.currentTime(query=True)
    object = split_attr_parts(attr, 0)
    active_control = get_active_time_control()
        
    start_frame, end_frame = cmds.timeControl(active_control, query=True, rangeArray=True) 
    if end_frame != start_frame + 1:
        if not manual and not cmds.checkBox(autokey_box, q=True, v=True):
            confirm = cmds.confirmDialog(message="Autokey is off but a framerange selection was found. Key frames anyway?", title='Warning', button=['Yes','Cancel'], defaultButton='Yes', cancelButton='No', dismissString='No', p=win)
            if confirm == 'Yes':
                key_multiple(simple, option_menu, start_frame, end_frame, current_frame, attr, items, selected_item, object, manual=True)
            else:
                key_frames(simple, option_menu, attr, items, selected_item, current_frame, object, manual)
        else:
            key_multiple(simple, option_menu, start_frame, end_frame, current_frame, attr, items, selected_item, object, manual)
    else:
        key_frames(simple, option_menu, attr, items, selected_item, current_frame, object, manual)
   
# If a timerange is found then we first key all the frames so that the current constraints are set, then iterate through them and switch them   
def key_multiple(simple, option_menu, start_frame, end_frame, current_frame, attr, items, selected_item, object, manual):

    cmds.undoInfo(openChunk=True)
    try:
        cmds.refresh(suspend=True)
        keyframes = cmds.keyframe(object, query=True, timeChange=True)
        if keyframes:
            keyframes = list(set(keyframes))
            keyframes = [n for n in keyframes if start_frame <= n < end_frame]
            for frame in keyframes:
                cmds.currentTime(frame, edit=True)
                cmds.setKeyframe(object, time=(frame, frame))
                if simple:
                    const = split_attr_parts(attr, 2)
                    weight_attr = cmds.parentConstraint(const, q=True, wal=True)
                    for item in weight_attr:
                        cmds.setKeyframe(const, at=item, time=(frame, frame))
            for frame in keyframes:
                cmds.currentTime(frame, edit=True)
                key_frames(simple, option_menu, attr, items, selected_item, frame, object, manual)
            cmds.currentTime(current_frame)
        cmds.refresh(suspend=False)
        cmds.refresh()
        cmds.undoInfo(closeChunk=True)
    
    except Exception as e:
        print("Error:", e)
        cmds.undoInfo(closeChunk=True)
        cmds.undo()  

# Snap and Key the given frame depending on the arguments
def key_frames(simple, option_menu, attr, items, selected_item, current_frame, object, manual):
    
    snap_t = cmds.xform(object, query=True, worldSpace=True, translation=True)
    snap_r = cmds.xform(object, query=True, worldSpace=True, rotation=True)

    if cmds.checkBox(bruteforce_box, q=True, v=True) and cmds.checkBox(autosnap_box, q=True, v=True):
        sel = cmds.ls(selection=True)
        locator = cmds.spaceLocator()[0]
        cmds.matchTransform(locator, object, pos=True, rot=True)
    
    if simple:
        const = split_attr_parts(attr, 2)
        weight_attr = cmds.parentConstraint(const, q=True, wal=True)
        option_index = cmds.optionMenu(option_menu, q=True, select=True) - 1
        for index, item in enumerate(weight_attr):
            if index + 1 == option_index:
                cmds.setAttr(const + '.' + item, 1)
                if cmds.checkBox(autokey_box, q=True, v=True) or manual:
                    cmds.setKeyframe(const, at=item, time=(current_frame, current_frame))
            else:
                cmds.setAttr(const + '.' + item, 0)
                if cmds.checkBox(autokey_box, q=True, v=True) or manual:
                    cmds.setKeyframe(const, at=item, time=(current_frame, current_frame))
    else:
        cmds.setAttr(attr, items.index(selected_item))

    if cmds.checkBox(autosnap_box, q=True, v=True):
        cmds.xform(object, worldSpace=True, translation=snap_t)
        cmds.xform(object, worldSpace=True, rotation=snap_r)
    
    if cmds.checkBox(bruteforce_box, q=True, v=True) and cmds.checkBox(autosnap_box, q=True, v=True):
        cmds.matchTransform(object, locator, pos=True, rot=True)
        cmds.delete(locator)
        if sel:
            cmds.select(sel[0])
    
    if cmds.checkBox(autokey_box, q=True, v=True) or manual:
        cmds.setKeyframe(object, time=(current_frame, current_frame))
    
# Check if the autosnap box is toggled on or not    
def autosnap_toggled(*args):

    autosnap = cmds.checkBox(autosnap_box, q=True, v=True)
    if autosnap:
        cmds.checkBox(bruteforce_box, e=True, en=True)
    else:
        cmds.checkBox(bruteforce_box, e=True, en=False)
     
# Get the active time control so that we can check the start and end selected frames
def get_active_time_control():

    active_time_control = None
    all_time_controls = cmds.lsUI(type='timeControl')
    if all_time_controls:
        active_time_control = all_time_controls[0]  # Assuming the first time control is the active one
    return active_time_control
    
# Select the control
def sel_control(obj):

    cmds.select(obj)
   
# Select the attribute, or the constraint if using a simpleswitcher   
def sel_attribute(attr):

    simplecheck = split_attr_parts(attr, 1)
    if simplecheck != 'nbTempSimpleSwitcher':
        cmds.select(attr)
    else:
        const = split_attr_parts(attr, 2)
        cmds.select(const)
 
# Select the constraint, or give a warning if no constraint was found 
def sel_constraint(const):

    if const == 'None':
        cmds.confirmDialog(message="Whoops, couldn't find a connected constraint for this switcher!       ", title='Warning', button=['Ok'], p=win)
    else:
        cmds.select(const)
  
# Rename tool - This adds a new tab to the UI where you can rename the chosen switcher row
def rename_tool(attr, items, switcher_label, option_menu):

    global current_edited_attr
    simplecheck = split_attr_parts(attr, 1)
    if simplecheck != 'nbTempSimpleSwitcher':
        current_edited_attr = attr
        cmds.select(attr)
        attr_name = split_attr_parts(attr, 1)
    else:
        current_edited_attr = split_attr_parts(attr, 0) + '.' + split_attr_parts(attr, 1)
        attr_name = 'N/A'
        
    # Rename Tab UI
    cmds.setParent(tabs)
    rename_tab = cmds.columnLayout()
    cmds.tabLayout(tabs, edit=True, tabLabel=(rename_tab, "Rename"))
    cmds.tabLayout(tabs, edit=True, selectTabIndex=4)
    cmds.tabLayout(tabs, edit=True, psc=select_4)
    cmds.setParent(rename_tab)
    cmds.separator(height=6, style='none')
    master_row = cmds.rowLayout(numberOfColumns=3, columnWidth3=(5, 100, 180))
    cmds.separator(width=5, style="none")
    cmds.text(label="Current label: ")
    current_label = cmds.text(label=' ' + switcher_label, bgc=[0.20, 0.20, 0.2], w=142, al='left', h=18)
    cmds.setParent('..')
    cmds.separator(height=5, style='none') 
    master_row = cmds.rowLayout(numberOfColumns=3, columnWidth3=(5, 100, 180))
    cmds.separator(width=5, style="none")
    cmds.text(label='New label: ')
    new_label = cmds.textField(text='', w=142)
    cmds.textField(new_label, e=True, ec=lambda *args: rename_label(current_label, new_label, *args))
    cmds.textField(new_label, e=True, aie=True)
    cmds.setParent('..')
    cmds.separator(height=5, style='none')
    master_row = cmds.rowLayout(numberOfColumns=3, columnWidth3=(5, 100, 180))
    cmds.separator(width=5, style="none")
    cmds.text(label="Attribute name: ")
    current_name = cmds.text(label=' ' + attr_name, bgc=[0.20, 0.20, 0.2], w=142, al='left', h=18)
    cmds.setParent('..')
    cmds.separator(height=5, style='none') 
    master_row = cmds.rowLayout(numberOfColumns=3, columnWidth3=(5, 100, 180))
    cmds.separator(width=5, style="none")
    cmds.text(label='New name: ')
    new_name = cmds.textField(text='', w=142)
    if attr_name == 'N/A':
        cmds.textField(new_name, e=True, ed=False)
    cmds.textField(new_name, e=True, ec=lambda *args: rename_attr(current_name, new_name, *args))
    cmds.textField(new_name, e=True, aie=True)
    cmds.setParent('..')
    cmds.separator(height=5, style='none') 
    master_row = cmds.rowLayout(numberOfColumns=2, columnWidth2=(5, 232))
    cmds.separator(width=4, style="none")
    enum_scroll_list = cmds.textScrollList(w=244, h=80)
    cmds.textScrollList(enum_scroll_list, edit=True, append=items)
    cmds.setParent('..')
    cmds.separator(height=3, style='none') 
    master_row = cmds.rowLayout(numberOfColumns=3, columnWidth3=(5, 100, 180))
    cmds.separator(width=5, style="none")
    cmds.text(label='Rename item: ')
    rename_item_field = cmds.textField(text='', w=142, ed=False)
    cmds.setParent('..')
    cmds.separator(height=15, style='none') 
    master_row = cmds.rowLayout(numberOfColumns=2, columnWidth2=(102, 100), h=30)
    cmds.separator(width=15, style="none")
    done_button = cmds.button(label='Done', command=lambda *args: done_renaming(rename_tab), h=20, w=50)
    cmds.textScrollList(enum_scroll_list, edit=True, sc=lambda *args: rename_item_selected(enum_scroll_list, rename_item_field, option_menu, *args))

# Makes sure you can't select any other tabs while editing
def select_4(*args):

    cmds.tabLayout(tabs, edit=True, selectTabIndex=4)

# Rename the label and update everything correctly
def rename_label(current_label, new_label, *args):

    global current_edited_attr
    attr = current_edited_attr
    label = cmds.textField(new_label, q=True, text=True)
    if len(label) > 0:
        for dict in switcher_array:
            if dict['Attribute'] == attr:
                dict['Label'] = label  
                break
        cmds.text(current_label, e=True, label=' ' + label)
        cmds.textField(new_label, e=True, text='')
        save_rows()
 
# Rename the attribute and update everything correctly (this is not accessible if editing a simpleswitcher)
def rename_attr(current_name, new_name, *args):

    global current_edited_attr
    attr = current_edited_attr
    obj = split_attr_parts(attr, 0)
    attribute = cmds.textField(new_name, q=True, text=True)
    if len(attribute) > 0:
        cmds.text(current_name, e=True, label=' ' + attribute)
        cmds.textField(new_name, e=True, text='')
        cmds.renameAttr(attr, attribute)
        new_attr = obj + '.' + attribute
        for dict in switcher_array:
            if dict['Attribute'] == attr:
                dict['Attribute'] = new_attr
                current_edited_attr = new_attr
                break
        save_rows()

# Rename the items inside the enum/optionmenu of the switcher
def rename_item_selected(enum_scroll_list, rename_item_field, option_menu, *args):

    item = cmds.textScrollList(enum_scroll_list, q=True, si=True)
    item_index = cmds.textScrollList(enum_scroll_list, q=True, sii=True)
    cmds.setFocus(rename_item_field)
    cmds.textField(rename_item_field, e=True, text=item[0])
    cmds.textField(rename_item_field, e=True, ec=lambda *args: rename_item(item, enum_scroll_list, rename_item_field, item_index, option_menu, *args))
    cmds.textField(rename_item_field, e=True, aie=True)
    cmds.textField(rename_item_field, e=True, ed=True)
 
# Called when renaming the items 
def rename_item(item, enum_scroll_list, rename_item_field, item_index, option_menu, *args):

    global current_edited_attr
    attr = current_edited_attr
    original_item = item[0]
    new_item = cmds.textField(rename_item_field, q=True, text=True)
    true_index = item_index[0] - 1
    attr_name = split_attr_parts(attr, 1)
    node = split_attr_parts(attr, 0)
    if len(new_item) > 0:
        cmds.textField(rename_item_field, e=True, text='')
        cmds.textScrollList(enum_scroll_list, e=True, rii=item_index[0])
        cmds.textScrollList(enum_scroll_list, e=True, ap=[item_index[0], new_item])
        cmds.textScrollList(enum_scroll_list, e=True, da=True)
        simplecheck = split_attr_parts(attr, 1)
        if simplecheck != 'nbTempSimpleSwitcher':
            enum_values = cmds.attributeQuery(attr_name, node=node, listEnum=True)
            enum_values_split = [value.strip() for value in enum_values[0].split(':')]
            enum_values_split[true_index] = new_item
            new_enum_values = ':'.join(enum_values_split)
            cmds.addAttr(attr, edit=True, enumName=new_enum_values, attributeType="enum")
            cmds.refresh()
            for dict in switcher_array:
                if dict['Attribute'] == attr:
                    dict['Items'] = enum_values_split
                    break
        else: 
            for dict in switcher_array:
                if dict['Attribute'] == attr:
                    for index, item in enumerate(dict['Items']):
                        if item == original_item:
                            dict['Items'][index] = new_item
                            break        
        save_rows()
  
# Refresh the switch tab and delete the rename tab UI when done editing  
def done_renaming(rename_tab):

    refresh_switch_tab()
    cmds.tabLayout(tabs, edit=True, selectTabIndex=1)
    cmds.tabLayout(tabs, edit=True, psc='pass')
    cmds.deleteUI(rename_tab)
 
# In the link tab, set the selected control 
def set_control():

    if cmds.ls(selection=True):
        selected_obj = cmds.ls(selection=True)[0]
        constraint_types = ['parentConstraint', 'scaleConstraint', 'pointConstraint', 'orientConstraint']
        able = True
        for constraint_name in constraint_types:
            if cmds.objectType(selected_obj, i=constraint_name):
                able = False
        if able:
            cmds.text(contr_name, edit=True, label=' ' + selected_obj)
            cmds.text(contr_name, edit=True, annotation=selected_obj)
            ready = cmds.text(const_name, query=True, label=True)
            labelfilled = cmds.textField(switcher_labelfield, query=True, text=True)
            
            if len(ready) > 0 and len(labelfilled) > 0:
                cmds.button(switcher_only, edit=True, en=True)
                cmds.button(generate, edit=True, en=True)
                cmds.button(clearbutton, edit=True, en=True)  
        else:
            cmds.confirmDialog(message='Cannot set a constraint as a control       ', title='Warning', button=['Ok'], p=win)
   
# In the link tab, set the selected constraint   
def set_constraint():

    if cmds.ls(selection=True):
        selected_obj = cmds.ls(selection=True)[0]
        constraint_types = ['parentConstraint', 'scaleConstraint', 'pointConstraint', 'orientConstraint']
        able = False
        for constraint_name in constraint_types:
            if cmds.objectType(selected_obj, i=constraint_name):
                able = True
        if able:
            cmds.text(const_name, edit=True, label=' ' + selected_obj)
            cmds.text(const_name, edit=True, annotation=selected_obj)
            ready = cmds.text(contr_name, query=True, label=True)
            labelfilled = cmds.textField(switcher_labelfield, query=True, text=True)
            
            if len(ready) > 0 and len(labelfilled) > 0:
                cmds.button(switcher_only, edit=True, en=True)
                cmds.button(generate, edit=True, en=True)
                cmds.button(clearbutton, edit=True, en=True)      
        else:
            cmds.confirmDialog(message='Only a constraint can be set here       ', title='Warning', button=['Ok'], p=win)

# Enable the generate and clear buttons in the link tab when all the information is filled out
def update_buttons(*args):

    if len(cmds.text(const_name, query=True, label=True)) > 0 and len(cmds.text(contr_name, query=True, label=True)) > 0 and len(cmds.textField(switcher_labelfield, query=True, text=True)) > 0:
        cmds.button(switcher_only, edit=True, en=True)
        cmds.button(generate, edit=True, en=True)
        cmds.button(clearbutton, edit=True, en=True) 

# Refresh the link tab so that all fields are default
def clear_link(*args):

    cmds.textField(switcher_labelfield, edit=True, text="SwitcherLabel")
    cmds.text(contr_name, edit=True, label='')
    cmds.text(const_name, edit=True, label='')
    cmds.button(switcher_only, edit=True, en=False)
    cmds.button(generate, edit=True, en=False)
    cmds.button(clearbutton, edit=True, en=False)

# Create a nondestructive simpleswitcher
def generate_simpleswitcher(*args):

    labelfilled = cmds.textField(switcher_labelfield, query=True, text=True)
    if labelfilled == '':
        cmds.confirmDialog(message='Please give your switcher a label       ', title='Warning', button=['Ok'], p=win)
    else:
        contr_to_add = cmds.text(contr_name, query=True, label=True)
        contr_to_add = contr_to_add[1:]
        const_to_add = cmds.text(const_name, query=True, label=True)
        const_to_add = const_to_add[1:]
        weight_attr = cmds.parentConstraint(const_to_add, q=True, wal=True)  
        enum_list = ['Default:']
        pattern = r'W\d$'
        
        for enumname in weight_attr:
            match = re.search(pattern, enumname)
            if match and match.start() == len(enumname) - 2:
                trimmedenum = enumname[:match.start()]
                enum_list.append(str(trimmedenum) + ':')
            else:
                enum_list.append(str(enumname) + ':')
                
        items = [item.rstrip(":") for item in enum_list]
        switcher_label = cmds.textField(switcher_labelfield, q=True, text=True)
        
        if cmds.checkBox(organise_box, q=True, v=True):
            cmds.parent(const_to_add, const_group_name)

        if cmds.checkBox(rename_box, q=True, v=True):
            new_constraint_name = switcher_label.replace(" ", "_")
            cmds.rename(const_to_add, new_constraint_name + '_Constraint')
            
        attr = contr_to_add + '.nbTempSimpleSwitcher' + '.' + const_to_add
        add_simple_attr(attr, const_to_add, items, switcher_label)
        clear_link()

# Create a switcher, which adds an enum to the control, sets driven keys and also attempts to save/convert the existing animation
def generate_switcher(*args):

    labelfilled = cmds.textField(switcher_labelfield, query=True, text=True)
    if labelfilled == '':
        cmds.confirmDialog(message='Please give your switcher a label       ', title='Warning', button=['Ok'], p=win)
    else:
        contr_to_add = cmds.text(contr_name, query=True, label=True)
        contr_to_add = contr_to_add[1:]
        const_to_add = cmds.text(const_name, query=True, label=True)
        const_to_add = const_to_add[1:]
        weight_attr = cmds.parentConstraint(const_to_add, q=True, wal=True)  
        enum_list = ['Default:']
        pattern = r'W\d$'
        
        for enumname in weight_attr:
            match = re.search(pattern, enumname)
            if match and match.start() == len(enumname) - 2:
                trimmedenum = enumname[:match.start()]
                enum_list.append(str(trimmedenum) + ':')
            else:
                enum_list.append(str(enumname) + ':')
                
        enum_string = ''.join(enum_list)
        if not cmds.attributeQuery('Follow', node=contr_to_add, exists=True):
            cmds.addAttr(contr_to_add, longName='Follow', attributeType='enum', enumName=enum_string, keyable=True)
        attr = contr_to_add + '.Follow'
        
        # Gets which weight is set to 1 so we can set our new enum to it later, preserving the current state
        current_active_constraint = None
        for index, item in enumerate(weight_attr):
            if cmds.getAttr(const_to_add + '.' + item) == 1:
                current_active_constraint = index
                break
                
        keyed_weights = {}
        keyframes = cmds.keyframe(const_to_add, query=True, timeChange=True)

        # Iterate through the keyframes and store the values of each weight at that frame, then delete the keys
        if keyframes:
            keyframes = list(set(keyframes))
            keyed_weights = {frame: [] for frame in keyframes}
            for frame in keyframes:
                weight_list = []
                for weight in weight_attr:
                    value = cmds.getAttr(const_to_add + '.' + weight, time=frame)
                    weight_list.append(value)
                keyed_weights[frame] = weight_list
        for weight in weight_attr:
            cmds.cutKey(const_to_add + '.' + weight, cl=True)
        
        # Iterate through the enum list and the weight attributes, setting driven keys respectively
        for i, x in enumerate(enum_list):
            for index, item in enumerate(weight_attr):
                if i-1 == index:
                    cmds.setDrivenKeyframe(const_to_add + '.' + item, cd=attr, driverValue=float(i), value=1)
                else:
                    cmds.setDrivenKeyframe(const_to_add + '.' + item, cd=attr, driverValue=float(i), value=0)
        
        if keyed_weights:        
            # Checks which keyed frames have all the weights off and keys the new enum to default (worldspace)
            for frame, weights in keyed_weights.items():
                if all(value == 0 for value in weights):
                    cmds.setKeyframe(attr, time=frame, value=0)
            # Iterate through the lists of keyframes for each weight attribute, so the new enum is set to whichever one was keyed as 1
                for index, value in enumerate(weights):
                    if value == 1:
                        cmds.setKeyframe(attr, time=frame, value=index + 1)
                        break
                  
        # Sets the new enum to the saved state from earlier
        if current_active_constraint is not None:
            cmds.setAttr(attr, current_active_constraint + 1)
                    
        items = [item.rstrip(":") for item in enum_list]
        switcher_label = cmds.textField(switcher_labelfield, q=True, text=True)
        
        if cmds.checkBox(organise_box, q=True, v=True):
            cmds.parent(const_to_add, const_group_name)
            
        if cmds.checkBox(rename_box, q=True, v=True):
            new_constraint_name = switcher_label.replace(" ", "_")
            cmds.rename(const_to_add, new_constraint_name + '_Constraint')
            
        attr = attr + '.' + const_to_add  
        add_existing_attr(attr, items, switcher_label)
        clear_link()
   
# Close the tool if a new scene is opened to avoid mismatches in saved information   
def scene_opened_callback(*args):

    cmds.deleteUI("Space_Switcher", window = True)
    
# Refresh the viewport
def refresh_ui(*args):

    cmds.refresh()
    
# Close old window if open
if (cmds.window("Space_Switcher", q=True, exists = True)):
    cmds.deleteUI("Space_Switcher", window = True)
            
# Create new window
win = cmds.window("Space_Switcher", title="Space Switcher", sizeable=False)

# All the UI        
cmds.columnLayout(adjustableColumn = True, columnOffset=('both', 20))
cmds.separator(height=10, style='none')
cmds.frameLayout(label='Space Switcher')
cmds.separator(height=6, style='none')  
cmds.setParent('..')

# Create a tab layout
tabs = cmds.tabLayout()

# Create the Switch tab
switch_tab = cmds.columnLayout()
cmds.separator(height=1, style='none')
switch_scroll = cmds.scrollLayout(h=240, w=259, hst=0, bgc=[0.17, 0.17, 0.17], cr=True)
switch_scroll_column = cmds.columnLayout(adjustableColumn = True, columnOffset=('both', 10))
cmds.setParent('..')
cmds.setParent('..')
cmds.separator(height=2, style='none')  
master_row = cmds.rowLayout(numberOfColumns=4, columnWidth4=(4, 70, 77, 70))
cmds.separator(width=9, style="none")
autokey_box = cmds.checkBox(label='Autokey', align='right', annotation="Key space switches within the tool automatically. Maya autokey will still work regardless")
autosnap_box = cmds.checkBox(label='Autosnap', align='right', annotation="Snap space switches within the tool automatically", v=True, cc=autosnap_toggled)
bruteforce_box = cmds.checkBox(label='Force snap', align='right', annotation="Uses temp locators in the background while snapping if autosnap doesn't work as expected")
cmds.setParent('..')
cmds.setParent('..')  # Leave the tab content and go back into the layout

# Create the Link tab
link_tab = cmds.columnLayout()
cmds.separator(height=6, style='none')  
master_row = cmds.rowLayout(numberOfColumns=4, columnWidth4=(5, 60, 32, 80))
cmds.separator(width=10, style="none")
cmds.text(label="Control", annotation='Select your child control and set it here')
set_button = cmds.button(label='>>', command=lambda *args: set_control(), h=20)
contr_name = cmds.text(label="", w=140, h=20,  bgc=[0.20, 0.20, 0.2], align='left')
cmds.setParent('..')
cmds.separator(height=5, style='none')  
master_row = cmds.rowLayout(numberOfColumns=4, columnWidth4=(5, 60, 32, 80))
cmds.separator(width=10, style="none")
cmds.text(label="Constraint", annotation='Select your constraint and set it here')
set_button = cmds.button(label='>>', command=lambda *args: set_constraint(), h=20)
const_name = cmds.text(label="", w=140, h=20,  bgc=[0.20, 0.20, 0.2], align='left')
cmds.setParent('..')
cmds.separator(height=5, style="none")
master_row = cmds.rowLayout(numberOfColumns=3, columnWidth3=(5, 35, 60))
cmds.separator(width=10, style="none")
cmds.text(label="Label", annotation='The label your switcher will have in the Switch tab (can be renamed later)')
switcher_labelfield = cmds.textField(text="SwitcherLabel", w=200, ec=update_buttons)
cmds.setParent('..')
cmds.separator(height=5, style="none")
master_row = cmds.rowLayout(numberOfColumns=3, columnWidth3=(5, 90, 95))
cmds.separator(width=19, style="none")
organise_box = cmds.checkBox(label='Organise', align='right', annotation='Moves the constraint to the nb_SpaceSwitcher group for easy access')
rename_box = cmds.checkBox(label='Rename constraint', align='right', annotation='Renames the constraint to the label above with the suffix _Constraint')
cmds.setParent('..')
cmds.separator(height=10, style="none")
master_row = cmds.rowLayout(numberOfColumns=3, columnWidth3=(2, 114, 60))
cmds.separator(width=15, style="none")
switcher_only = cmds.button(label='Simple Switcher', en=False, h=40, w=110, command=generate_simpleswitcher, annotation='Make a space switcher inside this tool for your control and constraint. Non-destructive')
generate = cmds.button(label='Convert to Enum', en=False, h=40, w=110, command=generate_switcher, annotation='Add an enum to your control with driven keys on your constraint. Destructive. Tries to save animated switches')
cmds.setParent('..')
cmds.separator(height=5, style="none")
master_row = cmds.rowLayout(numberOfColumns=2, columnWidth2=(5, 60))
cmds.separator(width=102, style="none")
clearbutton = cmds.button(label='Clear', en=False, h=20, w=50, command=clear_link, annotation='Resets this tab to default')
cmds.setParent('..')
cmds.setParent('..')  # Leave the tab content and go back into the layout

# Create the Find tab
find_tab = cmds.columnLayout()
cmds.separator(height=1, style='none')
find_scroll = cmds.scrollLayout(h=262, w=259, hst=0, cr=True)
find_scroll_column = cmds.columnLayout(adjustableColumn = True, columnOffset=('both', 10))
cmds.setParent('..')
cmds.setParent('..')
cmds.setParent('..')  # Leave the tab content and go back into the layout


# Add the tabs to the tab layout
cmds.tabLayout(tabs, edit=True, tabLabel=((switch_tab, "  Switch  "), (link_tab, "   Link   "), (find_tab, "   Find   ")))

# Display new window
cmds.showWindow(win)
cmds.window(win, e=True, h=350, w=309)

# Set up the ConstraintManager group and savedata attribute if it doesn't exist
const_group_name = "nb_SpaceSwitcher_grp"

if not cmds.objExists(const_group_name):
    const_group = cmds.group(em=True, name=const_group_name)
    
if not cmds.attributeQuery('nb_Constraint_Row_SaveData', node=const_group_name, exists=True):
        cmds.addAttr(const_group_name, longName='nb_Constraint_Row_SaveData', dt='string')
        cmds.setAttr(const_group_name + '.nb_Constraint_Row_SaveData', lock=True)

# Fill the switcher array with the savedata of this tool from the scene      
json_string = cmds.getAttr(const_group_name + '.nb_Constraint_Row_SaveData')

if json_string is not None:
    switcher_array = json.loads(json_string)
    cmds.evalDeferred(refresh_switch_tab)
else:
    switcher_array = []   
    
current_edited_attr = 'None'

cmds.scriptJob(event=["SceneOpened", scene_opened_callback], parent="Space_Switcher")
cmds.scriptJob(event=("Undo", refresh_ui), parent="Space_Switcher")

# Call the function to find custom attributes in the scene   
find_cust_attr()

