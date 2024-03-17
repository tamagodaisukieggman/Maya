from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance


import maya.mel as mel
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import math as math
import os
from random import randrange

def maya_main_window():
    main_window_ptr= omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    
class OpenImportDialog(QtWidgets.QDialog):

    dlg_instance = None
    
    @classmethod
    def show_dialog(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = OpenImportDialog()
       
        if cls.dlg_instance.isHidden():     
            cls.dlg_instance.show()
        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow()
            

    
    def __init__(self, parent=maya_main_window()):
        super(OpenImportDialog, self).__init__(parent)
        self.move_UI()
        self.setWindowTitle("Pro Boolean") 
        self.setMinimumWidth(350)
        self.setMaximumWidth(460)
        self.setMinimumHeight(130)
        self.setMaximumHeight(166)
           
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

   
    def move_UI(self):
        ''' Moves the UI to the cursor's position '''
        pos = QtGui.QCursor.pos()
        self.move(pos.x()-250, pos.y()-60)         
    
    def create_widgets(self):
        
        font = QtGui.QFont()
        font.setBold(True)
        #font.setPointSize(16)
        
        font1 = QtGui.QFont()
        font1.setBold(True)
        font1.setPointSize(11)        

        font2 = QtGui.QFont()
        font2.setBold(True)
        font2.setPointSize(10)

        font3 = QtGui.QFont()
        font3.setBold(True)
        #font3.setPointSize(9)

        
        self.boolean_number_lb = QtWidgets.QLabel("Boolean number:")
        self.boolean_number_lb.setFont(font)
        
        self.boolean_number = QtWidgets.QLineEdit("0/0")  
        self.boolean_number.setEnabled(False)
        self.boolean_number.setFixedSize(52 ,32)
        self.boolean_number.setMaximumWidth(32)
        self.boolean_number.setFont(font1)
        self.boolean_number.setToolTip("Used with the Cycle Button returns the number of Boolean pieces on a selected booleaned object.")

        self.reset_bool_btn = QtWidgets.QPushButton("#")
        self.reset_bool_btn.setToolTip("Ctrl + Click to open the Help UI window.")
        self.reset_bool_btn.setFont(font)
        self.reset_bool_btn.setFont(font1)
        self.reset_bool_btn.setStyleSheet("color: white;"
                        "background-color: rgb(120,80,80);"); 
        self.reset_bool_btn.setFixedSize(26,26) 

        
        width_btn = 102
        height_btn = 36
        self.bool_union_btn = QtWidgets.QPushButton("UNION")
        #bool_union_btn_image_path = cmds.internalVar(upd=1) + "icons/Mirror_Tool/mirror_x.png"
        #self.bool_union_btn.setIcon(QtGui.QIcon(bool_union_btn_image_path))
        #self.bool_union_btn.setIconSize(QtCore.QSize(60, 60))
        self.bool_union_btn.setFixedSize(width_btn ,height_btn)
        self.bool_union_btn.setFont(font2)
        #self.bool_union_btn.setToolTip("")
        self.bool_union_btn.setStyleSheet("QPushButton::hover"
                     "{"
                     "background-color : grey;"
                     "}")

        self.bool_difference_btn = QtWidgets.QPushButton("DIFFERENCE")
        #bool_difference_btn_align_image_path = cmds.internalVar(upd=1) + "icons/Mirror_Tool/mirror_y.png"
        #self.bool_difference_btn.setIcon(QtGui.QIcon(bool_difference_btn))
        #self.bool_difference_btn.setIconSize(QtCore.QSize(60, 60))
        self.bool_difference_btn.setFixedSize(width_btn ,height_btn)
        self.bool_difference_btn.setFont(font2)
        #self.bool_difference_btn.setToolTip("")
        self.bool_difference_btn.setStyleSheet("QPushButton::hover"
                     "{"
                     "background-color : grey;"
                     "}")
                     
        self.bool_intersection_btn = QtWidgets.QPushButton("INTERSECTION")
        #bool_intersection_btn_image_path = cmds.internalVar(upd=1) + "icons/Mirror_Tool/mirror_z.png"
        #self.bool_intersection_btn.setIcon(QtGui.QIcon(bool_intersection_btn))
        #self.bool_intersection_btn.setIconSize(QtCore.QSize(60, 60))
        self.bool_intersection_btn.setFixedSize(width_btn ,height_btn)
        self.bool_intersection_btn.setFont(font2)
        #self.bool_intersection_btn.setToolTip("")
        self.bool_intersection_btn.setStyleSheet("QPushButton::hover"
                     "{"
                     "background-color : grey;"
                     "}")

        self.bool_panel_btn = QtWidgets.QPushButton("PANEL")
        #bool_panel_btn_image_path = cmds.internalVar(upd=1) + "icons/Mirror_Tool/mirror_z.png"
        #self.bool_panel_btn.setIcon(QtGui.QIcon(bool_panel_btn))
        #self.bool_panel_btn.setIconSize(QtCore.QSize(60, 60))
        self.bool_panel_btn.setFixedSize(width_btn ,height_btn)
        self.boolean_number.setToolTip("Default Click Button will create booleans by duplicating your boolean objects and perform 2 operations 1. Intersect 2. Subtract.\nThis result will give you 2 wireframe meshes for each boolean object you decide to use.\nCtrl + Click to use the second method which is just creates a booleean difference with a small polyExtrude operation (this method requires a manual clenaup pass from the user to avoid having double face geometry with the booleans are baked and have their verrices merged.")
        self.bool_panel_btn.setFont(font2)
        #self.bool_panel_btn.setToolTip("")
        self.bool_panel_btn.setStyleSheet("QPushButton::hover"
                     "{"
                     "background-color : grey;"
                     "}")
        
        
        self.show_all_btn = QtWidgets.QPushButton("Show All")
        self.show_all_btn.setToolTip("Shows all boolean operation within a scene.")
        self.show_all_btn.setFont(font3)
        									  
        self.hide_all_btn = QtWidgets.QPushButton("Hide All")
        self.hide_all_btn.setToolTip("Hides all boolean operation within a scene.")
        self.hide_all_btn.setFont(font3)
        
        self.show_only_selected_btn = QtWidgets.QPushButton("Show Selected")
        self.show_only_selected_btn.setFont(font3)        
        self.show_only_selected_btn.setToolTip("Shows only selected boolean operations (related to your selection), will hide all other boolean operations in your scene that are not selected.\nIf you select the main pro bool object, it will show only all associated pro boolean objects (will hide the rest).\nCtrl + Click to on the main boolean object to select all associated live booleans")
                
        self.cycle_booleans_btn = QtWidgets.QPushButton("Cycle")
        self.cycle_booleans_btn.setToolTip("Cycles through your boolean operations.\nCtrl + Click to cycle backwards.\nShit + Click to cycle between boolean operations (union, difference amd intersection).")
        self.cycle_booleans_btn.setFont(font3)
        
        self.tgl_xray_btn = QtWidgets.QPushButton("Xray")
        self.tgl_xray_btn.setToolTip("Toggles x-Ray mode")
        self.tgl_xray_btn.setFont(font3)
        
        self.freeze_boolean_piece_btn = QtWidgets.QPushButton("Freeze")
        
        self.clean_btn = QtWidgets.QPushButton("Clean")
        self.clean_btn.setFont(font3)
        self.clean_btn.setToolTip("Click to delete the Boolean_Tag_num attribute.\nUse with caution as this will affect all other boolean operation if used incorrectly (e.g. Boolean numbers will display the wrong values).\nIf nothing is selected the tool will clean the Pro_Boolean_Folder of any junk files.\n\nCtrl + Click will replace the attribute only on objects that already have the booelan attribute (objects with no attribute will be deselected).\nCtrl + Alt to switch your wireframe cutters in shaded mode with no wireframe color. (You can toggle this for as long as your cutters have a Boolean Tag ID attribute).")
        
        self.bake_btn = QtWidgets.QPushButton("BAKE")
        self.bake_btn.setFont(font3)
        self.bake_btn.setToolTip("Will bake the final result of the boolean operation on the selected objects.\nCtrl +Click to keep the boolean objects after the bake is complete.")
        self.bake_btn.setStyleSheet("color: white;""background-color: rgb(130,130,10);"); 
        
        
        self.close_btn = QtWidgets.QPushButton("Close")
        self.close_btn.setFont(font3)
        self.close_btn.setStyleSheet("background-color:rgb(55,55,55)");
     
    def create_layouts(self):
        #MAIN LAYOUT

        button_layout = QtWidgets.QHBoxLayout()
        #button_layout.setSpacing(0)
        button_layout.setContentsMargins(0,0,0,0)
        button_layout.addWidget(self.bool_union_btn)
        button_layout.addWidget(self.bool_difference_btn)
        button_layout.addWidget(self.bool_intersection_btn)
        button_layout.addWidget(self.bool_panel_btn)        
        
        button_layout2= QtWidgets.QHBoxLayout()
        #button_layout2.setSpacing(0)
        button_layout.setContentsMargins(0,0,0,0)
        button_layout2.addWidget(self.clean_btn)
        button_layout2.addWidget(self.hide_all_btn)
        button_layout2.addWidget(self.show_all_btn)
        button_layout2.addWidget(self.show_only_selected_btn)      
        #button_layout2.addWidget(self.freeze_boolean_piece_btn)
        
        
        #button_layout2.addStretch()

        button_layout3= QtWidgets.QHBoxLayout()
        #button_layout2.setSpacing(0)
        #button_layout.setContentsMargins(0,0,0,0)
        button_layout3.addWidget(self.boolean_number_lb)        
        button_layout3.addWidget(self.boolean_number) 
        button_layout3.addWidget(self.reset_bool_btn) 
        button_layout3.addWidget(self.cycle_booleans_btn)   
        button_layout3.addWidget(self.tgl_xray_btn) 
        button_layout3.addWidget(self.bake_btn)   
        button_layout3.addStretch()
        
        
        close_layout = QtWidgets.QHBoxLayout()
        close_layout.setSpacing(0)
        #close_layout.setContentsMargins(0,0,0,0)
        close_layout.addWidget(self.close_btn)        
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(button_layout2)
        main_layout.addLayout(button_layout3)
        main_layout.addLayout(close_layout)

    def create_connections(self):
        
        self.bool_union_btn.clicked.connect(self.union_modifier)
        self.bool_difference_btn.clicked.connect(self.difference_modifier)
        self.bool_intersection_btn.clicked.connect(self.intersection_modifier)
        self.bool_panel_btn.clicked.connect(self.panel_modifier)
        
        
        self.show_all_btn.clicked.connect(self.show_all_boolean_pieces)
        self.hide_all_btn.clicked.connect(self.hide_modifier)
        self.show_only_selected_btn.clicked.connect(self.show_only_selected_modifier)
        
        self.reset_bool_btn.clicked.connect(self.reset_help_modifier)
        self.cycle_booleans_btn.clicked.connect(self.cycle_modifier)
        self.tgl_xray_btn.clicked.connect(self.xray_toggle)
        #self.freeze_boolean_piece_btn.clicked.connect(self.dummy_code)
        self.clean_btn.clicked.connect(self.clean_modifier)
        self.bake_btn.clicked.connect(self.bake_modifier)

        self.close_btn.clicked.connect(self.close)
        
        self.bool_union_btn.clicked.connect(self.reset_counter)   
        self.bool_difference_btn.clicked.connect(self.reset_counter)     
        self.bool_difference_btn.released.connect(self.reset_counter)     
   
        self.bool_intersection_btn.clicked.connect(self.reset_counter)
        self.bool_panel_btn.clicked.connect(self.reset_counter)
#FUNCTIONS _____________________________________________________________________________________________________________________________________________________________________________________________        

    def boolean_union_operations(self):
        cmds.selectPref(trackSelectionOrder = 1)

        sel = self.group_selection(1) # works if you have groups selected
        if len(sel)==0:
            cmds.warning("Nothing selected! Please make a selection to perform a pro boolean operation.")
        else:
            #self.tag_id_checker() ####

            #Entered the method self.tag_id_checker here raw with a warning instead of baking / Because it has an impact on how the cmds.unodoInfo command works.
            #_________________________________________________________________________________________________
            #RAW tag_id_checker method
            sel = cmds.ls(sl=1,l=1)
            selection = cmds.ls(sl=1,l=1)
            attrExist = cmds.attributeQuery('BTnum', node=selection[0], exists=True)
            #print(attrExist)
            tag_number_clashing = False
            empty = []
            if attrExist:
                get_btag_value_of_fist_sel = cmds.getAttr("{}.BTnum".format(selection[0]))
                #print("get_btag_value_of_fist_sel is {}".format(get_btag_value_of_fist_sel))
                for i in selection[1:]:
                    
                    attrExist_for_i = cmds.attributeQuery('BTnum', node=i, exists=True)
                    if attrExist_for_i:
                        
                        get_btag_value = cmds.getAttr("{}.BTnum".format(i))
                        #print("get_btag_value is {}".format(get_btag_value))
                        
                        has_booleans = False
                        getHistory = cmds.listHistory(i)
                        for history in getHistory:
                            if "polyCBoolOp" in history:
                                has_booleans = True
                        
                        if get_btag_value != get_btag_value_of_fist_sel and  has_booleans:
                            tag_number_clashing = True
                            #cmds.warning("Tags dont match")
                            #cmds.select(i)
                            #bm = self.bake_options(1)
                            new_sel = cmds.ls(sl=1, l=1)
                            empty.append(i)

            elif not attrExist:
                for i in selection[1:]:
                    #print(i)
                    attrExist_for_i = cmds.attributeQuery('BTnum', node=i, exists=True)
                    if attrExist_for_i:
                        #print("i is {}".format(i))
                        get_btag_value = cmds.getAttr("{}.BTnum".format(i))

                        has_booleans = False
                        getHistory = cmds.listHistory(i)
                        for history in getHistory:
                            if "polyCBoolOp" in history:
                                has_booleans = True
                                tag_number_clashing = True
                                empty.append(i)
            
            empty = list(dict.fromkeys(empty)) 
            #_________________________________________________________________________________________________

            if tag_number_clashing:
                cmds.warning("Boolean_Tag_num present in [union] object! :The object you are trying to Boolean with {} already has pro booleans operations associated with it (Boolean_Tag_num attr). Please bake the boolean operation before using it as a boolean.".format(empty))
                #p_message = "The object you are trying to Boolean {} already has probooleans operations associated with it.\nPlease bake the boolean operation before using it as a boolean.".format(empty)
                #result = cmds.confirmDialog( title='Boolean Warning',icon="information", message= p_message, button=['Cancel'],  cancelButton='Cancel', dismissString='No' )
              
            else:            
      
                #selection = cmds.ls(sl=1, l=1)
                selection = self.group_selection(2) # works if you have groups selected
                sel_pop = sel.pop(0)
                final_sel = selection[0]
                counter = 0
                counternum = 0
                empty = []
                final_meshes = []
                for i in sel:
                    if counter ==0:
                        cmds.select(final_sel, i)
                        result = self.pro_boolean(1,0,0)
                        final_meshes.append(result[0])
                        empty.append(result[0])
                        counter+=1
                    else:
                        cmds.select(empty[counternum], i)
                        result = self.pro_boolean(1,0,0)
                        final_meshes.append(result[0])
                        empty.append(result[0])
                        counternum +=1 
                    cmds.select(final_meshes[-1])
                
    def boolean_difference_operations(self):
        cmds.selectPref(trackSelectionOrder = 1)
        
        sel = cmds.ls(sl=1, l=1)  
        
        #group_checker = self.check_for_groups(sel)
        
        sel = self.group_selection(1) # works if you have groups selected

        
        
        if len(sel)==0:
            cmds.warning("Nothing selected! Please make a selection to perform a pro boolean operation.") 
        else: 
            
            #self.tag_id_checker() ####
            #Entered the method self.tag_id_checker here raw with a warning instead of baking / Because it has an impact on how the cmds.unodoInfo command works.
            #_________________________________________________________________________________________________
            
            sel = cmds.ls(sl=1,l=1)
            selection = cmds.ls(sl=1,l=1)
            attrExist = cmds.attributeQuery('BTnum', node=selection[0], exists=True)
            #print(attrExist)
            tag_number_clashing = False
            empty = []
            if attrExist:
                #print("selection is {}".format(selection))
                get_btag_value_of_fist_sel = cmds.getAttr("{}.BTnum".format(selection[0]))
                #print("get_btag_value_of_fist_sel is {}".format(get_btag_value_of_fist_sel))
                for i in selection[1:]:
                    #print(i)
                    attrExist_for_i = cmds.attributeQuery('BTnum', node=i, exists=True)
                    if attrExist_for_i:
                        #print("i is {}".format(i))
                        get_btag_value = cmds.getAttr("{}.BTnum".format(i))
                        #print("get_btag_value is {}".format(get_btag_value))
                        
                        has_booleans = False
                        getHistory = cmds.listHistory(i)
                        for history in getHistory:
                            if "polyCBoolOp" in history:
                                has_booleans = True
                        
                        if get_btag_value != get_btag_value_of_fist_sel and  has_booleans:
                            tag_number_clashing = True
                            #cmds.warning("Tags dont match")
                            #cmds.select(i)
                            #bm = self.bake_options(1)
                            new_sel = cmds.ls(sl=1, l=1)
                            empty.append(i)

            elif not attrExist:
                for i in selection[1:]:
                    #print(i)
                    attrExist_for_i = cmds.attributeQuery('BTnum', node=i, exists=True)
                    if attrExist_for_i:
                        #print("i is {}".format(i))
                        get_btag_value = cmds.getAttr("{}.BTnum".format(i))

                        has_booleans = False
                        getHistory = cmds.listHistory(i)
                        for history in getHistory:
                            if "polyCBoolOp" in history:
                                has_booleans = True
                                tag_number_clashing = True
                                empty.append(i)
              
            empty = list(dict.fromkeys(empty))              
            #_________________________________________________________________________________________________

            if tag_number_clashing:
                cmds.warning("Boolean_Tag_num present in [cutter] object! :The object you are trying to Boolean with {} already has pro booleans operations associated with it (Boolean_Tag_num attr). Please bake the boolean operation before using it as a boolean.".format(empty))
                #p_message = "The object you are trying to Boolean {} already has probooleans operations associated with it.\nPlease bake the boolean operation before using it as a boolean.".format(empty)
                #result = cmds.confirmDialog( title='Boolean Warning',icon="information", message= p_message, button=['Cancel'],  cancelButton='Cancel', dismissString='No' )
                
            else:
                selection = self.group_selection(2) # works if you have groups selected
                sel_pop = sel.pop(0)
                final_sel = selection[0]
                counter = 0
                counternum = 0
                empty = []
                final_meshes = []
                
                for i in sel:
                    if counter ==0:
                        cmds.select(final_sel, i)
                        result = self.pro_boolean(2,0,0)
                        final_meshes.append(result[0])
                        empty.append(result[0])
                        counter+=1
                    else:
                        cmds.select(empty[counternum], i)
                        result = self.pro_boolean(2,0,0)
                        final_meshes.append(result[0])
                        empty.append(result[0])
                        counternum +=1  
                    cmds.select(final_meshes[-1])


    def boolean_panel_difference_operations(self, number):
        cmds.selectPref(trackSelectionOrder = 1)
        extrude = number
        #sel = cmds.ls(sl=1, l=1)  
        sel = self.group_selection(1) # works if you have groups selected
        if len(sel)==0:
            cmds.warning("Nothing selected! Please make a selection to perform a pro boolean operation.")        

        elif len(sel)==1:
            cmds.warning("Please select one more object to perform a pro boolean operation.")               
        
        else:
            if extrude ==1 and len(sel) >=2:
                extrude = self.extrude_panel(sel) 
                sel = extrude            
            
            #self.tag_id_checker() ####
            
            
            #Entered the method self.tag_id_checker here raw with a warning instead of baking / Because it has an impact on how the cmds.unodoInfo command works.
            #_________________________________________________________________________________________________
            #RAW tag_id_checker method
            sel = cmds.ls(sl=1,l=1)
            selection = cmds.ls(sl=1,l=1)
            attrExist = cmds.attributeQuery('BTnum', node=selection[0], exists=True)
            #print(attrExist)
            tag_number_clashing = False
            empty = []
            if attrExist:
                get_btag_value_of_fist_sel = cmds.getAttr("{}.BTnum".format(selection[0]))
                #print("get_btag_value_of_fist_sel is {}".format(get_btag_value_of_fist_sel))
                for i in selection[1:]:
                    
                    attrExist_for_i = cmds.attributeQuery('BTnum', node=i, exists=True)
                    if attrExist_for_i:
                        
                        get_btag_value = cmds.getAttr("{}.BTnum".format(i))
                        #print("get_btag_value is {}".format(get_btag_value))
                        
                        has_booleans = False
                        getHistory = cmds.listHistory(i)
                        for history in getHistory:
                            if "polyCBoolOp" in history:
                                has_booleans = True
                        
                        if get_btag_value != get_btag_value_of_fist_sel and  has_booleans:
                            tag_number_clashing = True
                            #cmds.warning("Tags dont match")
                            #cmds.select(i)
                            #bm = self.bake_options(1)
                            new_sel = cmds.ls(sl=1, l=1)
                            empty.append(i)

            elif not attrExist:
                for i in selection[1:]:
                    #print(i)
                    attrExist_for_i = cmds.attributeQuery('BTnum', node=i, exists=True)
                    if attrExist_for_i:
                        #print("i is {}".format(i))
                        get_btag_value = cmds.getAttr("{}.BTnum".format(i))

                        has_booleans = False
                        getHistory = cmds.listHistory(i)
                        for history in getHistory:
                            if "polyCBoolOp" in history:
                                has_booleans = True
                                tag_number_clashing = True
                                empty.append(i)

            empty = list(dict.fromkeys(empty)) 
            #_________________________________________________________________________________________________

            if tag_number_clashing:
                cmds.warning("Boolean_Tag_num present in [cutter] object! :The object you are trying to Boolean with {} already has pro booleans operations associated with it (Boolean_Tag_num attr). Please bake the boolean operation before using it as a boolean.".format(empty))
                #p_message = "The object you are trying to Boolean {} already has probooleans operations associated with it.\nPlease bake the boolean operation before using it as a boolean.".format(empty)
                #result = cmds.confirmDialog( title='Boolean Warning',icon="information", message= p_message, button=['Cancel'],  cancelButton='Cancel', dismissString='No' )
              
            else:            
                selection = self.group_selection(2) # works if you have groups selected
                #selection = cmds.ls(sl=1, l=1)
                sel_pop = sel.pop(0)
                final_sel = selection[0]
                counter = 0
                counternum = 0
                empty = []
                final_meshes = []
                for i in sel:
                    if counter ==0:
                        cmds.select(final_sel, i)
                        result = self.pro_boolean(2,0,0)
                        final_meshes.append(result[0])  
                        empty.append(result[0])
                        counter+=1
                    else:
                        cmds.select(empty[counternum], i)
                        result = self.pro_boolean(2,0,0)
                        final_meshes.append(result[0]) 
                        empty.append(result[0])
                        counternum +=1
      
                    cmds.select(final_meshes[-1])

    
    def boolean_intersection_operations(self):
        cmds.selectPref(trackSelectionOrder = 1)
        sel = self.group_selection(1) # works if you have groups selected
        if len(sel)==0:
            cmds.warning("Nothing selected! Please make a selection to perform a pro boolean operation.")
        else:
            #self.tag_id_checker() ####
            #Entered the method self.tag_id_checker here raw with a warning instead of baking / Because it has an impact on how the cmds.unodoInfo command works.
            #_________________________________________________________________________________________________
            #RAW tag_id_checker method
            sel = cmds.ls(sl=1,l=1)
            selection = cmds.ls(sl=1,l=1)
            attrExist = cmds.attributeQuery('BTnum', node=selection[0], exists=True)
            #print(attrExist)
            tag_number_clashing = False
            empty = []
            if attrExist:
                get_btag_value_of_fist_sel = cmds.getAttr("{}.BTnum".format(selection[0]))
                #print("get_btag_value_of_fist_sel is {}".format(get_btag_value_of_fist_sel))
                for i in selection[1:]:
                    
                    attrExist_for_i = cmds.attributeQuery('BTnum', node=i, exists=True)
                    if attrExist_for_i:
                        
                        get_btag_value = cmds.getAttr("{}.BTnum".format(i))
                        #print("get_btag_value is {}".format(get_btag_value))
                        
                        has_booleans = False
                        getHistory = cmds.listHistory(i)
                        for history in getHistory:
                            if "polyCBoolOp" in history:
                                has_booleans = True
                        
                        if get_btag_value != get_btag_value_of_fist_sel and  has_booleans:
                            tag_number_clashing = True
                            #cmds.warning("Tags dont match")
                            #cmds.select(i)
                            #bm = self.bake_options(1)
                            new_sel = cmds.ls(sl=1, l=1)
                            empty.append(i)
            
            elif not attrExist:
                for i in selection[1:]:
                    #print(i)
                    attrExist_for_i = cmds.attributeQuery('BTnum', node=i, exists=True)
                    if attrExist_for_i:
                        #print("i is {}".format(i))
                        get_btag_value = cmds.getAttr("{}.BTnum".format(i))

                        has_booleans = False
                        getHistory = cmds.listHistory(i)
                        for history in getHistory:
                            if "polyCBoolOp" in history:
                                has_booleans = True
                                tag_number_clashing = True
                                empty.append(i)            
            
            empty = list(dict.fromkeys(empty)) 
            #_________________________________________________________________________________________________

            if tag_number_clashing:
                cmds.warning("Boolean_Tag_num present in [intersect] object! :The object you are trying to Boolean with {} already has pro booleans operations associated with it (Boolean_Tag_num attr). Please bake the boolean operation before using it as a boolean.".format(empty))
                #p_message = "The object you are trying to Boolean {} already has probooleans operations associated with it.\nPlease bake the boolean operation before using it as a boolean.".format(empty)
                #result = cmds.confirmDialog( title='Boolean Warning',icon="information", message= p_message, button=['Cancel'],  cancelButton='Cancel', dismissString='No' )
              
            else:            
                selection = self.group_selection(2) # works if you have groups selected
                sel_pop = sel.pop(0)
                final_sel = selection[0]
                counter = 0
                counternum = 0
                empty = []
                final_meshes = []
                for i in sel:
                    if counter ==0:
                        cmds.select(final_sel, i)
                        result = self.pro_boolean(3,0,0)
                        final_meshes.append(result[0])
                        empty.append(result[0])
                        counter+=1
                    else:
                        cmds.select(empty[counternum], i)
                        result = self.pro_boolean(3,0,0)
                        final_meshes.append(result[0])
                        empty.append(result[0])
                        counternum +=1         
                    cmds.select(final_meshes[-1])
                

    def bool_panel(self):
        cmds.selectPref(trackSelectionOrder = 1)
        filter_groups = self.group_selection2()
        sel = cmds.ls(sl=1)
        selection = cmds.ls(sl=1, l=1)
        print("selection is {}".format(selection) )
        
        if len(sel)==0:
            cmds.warning("Nothing selected! Please make a selection to perform a pro boolean operation.")        
        else:    
            #check = self.tag_id_checker()
            
            #if check[0]:
            #    sel = check[1]
            #    selection =check[2]       
            #Entered the method self.tag_id_checker here raw with a warning instead of baking / Because it has an impact on how the cmds.unodoInfo command works.
            #_________________________________________________________________________________________________
            #RAW tag_id_checker method
            sel = cmds.ls(sl=1,l=1)
            selection = cmds.ls(sl=1,l=1)
            attrExist = cmds.attributeQuery('BTnum', node=selection[0], exists=True)
            #print(attrExist)
            tag_number_clashing = False
            empty = []
            if attrExist:
                get_btag_value_of_fist_sel = cmds.getAttr("{}.BTnum".format(selection[0]))
                #print("get_btag_value_of_fist_sel is {}".format(get_btag_value_of_fist_sel))
                for i in selection[1:]:
                    
                    attrExist_for_i = cmds.attributeQuery('BTnum', node=i, exists=True)
                    if attrExist_for_i:
                        
                        get_btag_value = cmds.getAttr("{}.BTnum".format(i))
                        #print("get_btag_value is {}".format(get_btag_value))
                        
                        has_booleans = False
                        getHistory = cmds.listHistory(i)
                        for history in getHistory:
                            if "polyCBoolOp" in history:
                                has_booleans = True
                        
                        if get_btag_value != get_btag_value_of_fist_sel and  has_booleans:
                            tag_number_clashing = True
                            #cmds.warning("Tags dont match")
                            #cmds.select(i)
                            #bm = self.bake_options(1)
                            new_sel = cmds.ls(sl=1, l=1)
                            empty.append(i)
            
            elif not attrExist:
                for i in selection[1:]:
                    #print(i)
                    attrExist_for_i = cmds.attributeQuery('BTnum', node=i, exists=True)
                    if attrExist_for_i:
                        #print("i is {}".format(i))
                        get_btag_value = cmds.getAttr("{}.BTnum".format(i))

                        has_booleans = False
                        getHistory = cmds.listHistory(i)
                        for history in getHistory:
                            if "polyCBoolOp" in history:
                                has_booleans = True
                                tag_number_clashing = True
                                empty.append(i)            
            
            empty = list(dict.fromkeys(empty)) 
            #_________________________________________________________________________________________________

            if tag_number_clashing:
                cmds.warning("Boolean_Tag_num present in [cutter] object! :The object you are trying to Boolean with {} already has pro booleans operations associated with it (Boolean_Tag_num attr). Please bake the boolean operation before using it as a boolean.".format(empty))
                #p_message = "The object you are trying to Boolean {} already has probooleans operations associated with it.\nPlease bake the boolean operation before using it as a boolean.".format(empty)
                #result = cmds.confirmDialog( title='Boolean Warning',icon="information", message= p_message, button=['Cancel'],  cancelButton='Cancel', dismissString='No' )
              
            else:                               
                  
                sel_pop = sel.pop(0)
                final_sel = selection[0]
                print("final_sel is {}".format(final_sel) )

                counter = 0
                counternum = 0
                boolean_result_meshes = []
                subtract_2nd_pass = []
                original_tag_number = []
                ran_number = randrange(1, 9999)
                final_rename = []
                final_meshes = []
                for i in sel:
                    if counter ==0:
                        cmds.warning("selection[counter] is {}".format(selection[counter]) )
                        cmds.warning("is {}".format(i) )
                        duplicate_sel = cmds.duplicate(selection[counter], i)
                        
                        cmds.select(duplicate_sel)
                        result1 = self.pro_boolean(3,1,ran_number)
                        cmds.warning("result1[1] is {}".format(result1[1]))
                        
                        final_rename.append(result1[0])
                        
                        result_pass_1 = result1[1]
                        
                        cmds.warning("result_pass_1[-2] is {}".format(result_pass_1[-2]))
                        make_visible = cmds.setAttr("{}.visibility".format(result_pass_1[-2]), 0)
                        cmds.setAttr("{}.BTnum".format(result_pass_1[-2]), l=0)  
                        cmds.deleteAttr( result_pass_1[-2], at='Boolean_Tag_num')   
                        cmds.rename(result_pass_1[-2], "transform0")
                        
                        original_sel = cmds.select(final_sel, i)
                        result2 = self.pro_boolean(2,1,ran_number)
                        boolean_result_meshes.append(result2[0])
                        cmds.warning("boolean_result_meshes is {}".format(result2))
                        cmds.warning("boolean_result_meshes2222 is {}".format(result2[0]))
                    else:
                        print(counter)
                        print(selection)
                        
                        print("boolean_result_meshes is {}".format(boolean_result_meshes))
                        print("final_rename is {}".format(final_rename))
                        
                        duplicate_sel = cmds.duplicate(boolean_result_meshes[-1],i)
                        print("duplicate_sel is {}".format(duplicate_sel))

                        #cmds.warning("boolean_result_meshes is {}".format(boolean_result_meshes))
                        cmds.warning("selection[counter+1]is {}".format(selection[counter+1]))
                        
                        #cmds.select(boolean_result_meshes[-1], selection[counter+1]) #selects the initial boolean piece and uses that to boolean from (test)
                        cmds.select(duplicate_sel) #selects the initial boolean piece and uses that to boolean from (test)
                        
                        result3 = self.pro_boolean(3,1,ran_number) 
                        cmds.warning("result3 is {}".format(result3))
                        
                        result_pass_3 = result3[1]
                        #hide wireframe of intersection
                        cmds.warning("result_pass_3[-2] is {}".format(result_pass_3[-2]))
                        make_visible = cmds.setAttr("{}.visibility".format(result_pass_3[-2]), 0)
                        cmds.setAttr("{}.BTnum".format(result_pass_3[-2]), l=0)  
                        cmds.deleteAttr( result_pass_3[-2], at='Boolean_Tag_num')   
                        cmds.rename(result_pass_3[-2], "transform0") 
                        
                        print("boolean_result_meshes is {}".format(boolean_result_meshes))
                        cmds.select(boolean_result_meshes[-1], i)

                        result4 = self.pro_boolean(2,1,ran_number) 
                        cmds.warning("result4 is {}".format(result4))
                        cmds.select(result4[0])
                        boolean_result_meshes.append(result4[0])
                        
                    counter+=1
                    counternum+=1

    def union_modifier(self):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ShiftModifier:
            print('Shift+Click')
        elif modifiers == QtCore.Qt.ControlModifier:
            print('Control+Click')
        elif modifiers == (QtCore.Qt.ControlModifier |
                           QtCore.Qt.ShiftModifier):
            print('Control+Shift+Click')
        else:
            print('Click')
            def operation():
                self.boolean_union_operations()
            self.open_close_undo_chunk(operation)

    def difference_modifier(self):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ShiftModifier:
            print('Shift+Click')
        elif modifiers == QtCore.Qt.ControlModifier:
            print('Control+Click')
        elif modifiers == (QtCore.Qt.ControlModifier |
                           QtCore.Qt.ShiftModifier):
            print('Control+Shift+Click')
        else:
            print('Click')
            def operation():
                self.boolean_difference_operations()
            self.open_close_undo_chunk(operation)
            
    def intersection_modifier(self):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ShiftModifier:
            print('Shift+Click')
        elif modifiers == QtCore.Qt.ControlModifier:
            print('Control+Click')
        elif modifiers == (QtCore.Qt.ControlModifier |
                           QtCore.Qt.ShiftModifier):
            print('Control+Shift+Click')
        else:
            print('Click')
            def operation():
                self.boolean_intersection_operations()
            self.open_close_undo_chunk(operation)

    def panel_modifier(self):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ShiftModifier:
            print('Shift+Click')
            
            return test
        elif modifiers == QtCore.Qt.ControlModifier:
            print('Control+Click')
            def operation():
                self.boolean_panel_difference_operations(1)
            self.open_close_undo_chunk(operation)

        elif modifiers == (QtCore.Qt.ControlModifier |
                           QtCore.Qt.ShiftModifier):
            print('Control+Shift+Click')
            return test
        else:
            print('Click')
            def operation():
                self.bool_panel()
            self.open_close_undo_chunk(operation)

    def hide_modifier(self):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ShiftModifier:
            print('Shift+Click')
        elif modifiers == QtCore.Qt.ControlModifier:
            print('Control+Click')
            def operation():
                self.hide_boolean_pieces(1)
            self.open_close_undo_chunk(operation)

        elif modifiers == (QtCore.Qt.ControlModifier |
                           QtCore.Qt.ShiftModifier):
            print('Control+Shift+Click')
        else:
            print('Click')
            def operation():
                self.hide_boolean_pieces(0)
            self.open_close_undo_chunk(operation)
      
    def cycle_modifier(self):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ShiftModifier:
            print('Shift+Click')
            test = self.cycle_operations()
            return test
            
        elif modifiers == QtCore.Qt.ControlModifier:
            print('Control+Click')
            def operation():
                self.cycle_booleans(1)
            self.open_close_undo_chunk(operation)

        elif modifiers == (QtCore.Qt.ControlModifier |
                           QtCore.Qt.ShiftModifier):
            print('Control+Shift+Click')
        else:
            print('Click')
            def operation():
                self.cycle_booleans(0)
            self.open_close_undo_chunk(operation)

    def bake_modifier(self):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ShiftModifier:
            print('Shift+Click')
        elif modifiers == QtCore.Qt.ControlModifier:
            print('Control+Click')
            def operation():
                self.bake_options(0)
            self.open_close_undo_chunk(operation)
        elif modifiers == (QtCore.Qt.ControlModifier |
                           QtCore.Qt.ShiftModifier):
            print('Control+Shift+Click')
        else:
            print('Click')
            def operation():
                self.bake_options(1)
            self.open_close_undo_chunk(operation)


   
    def clean_modifier(self):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ShiftModifier:
            print('Shift+Click')

        elif modifiers == QtCore.Qt.ControlModifier:
            print('Control+Click')
            def operation():
                self.create_attribute()
                self.clean_duplicated_mesh()
                self.reset_counter()
            self.open_close_undo_chunk(operation)
        
        elif modifiers == QtCore.Qt.AltModifier:
            print('Alt+Click')

        elif modifiers == (QtCore.Qt.AltModifier |
                           QtCore.Qt.ControlModifier):
            print('Control+Alt+Click')
            def operation():
                self.restore_wireframe()
            self.open_close_undo_chunk(operation)

       
        elif modifiers == (QtCore.Qt.ControlModifier |
                           QtCore.Qt.ShiftModifier):
            print('Control+Shift+Click')
        else:
            sel = cmds.ls(sl=1)
            if len(sel)==0:
                def operation():
                    #self.clean_empty_groups()
                    self.clean_groups_2()
                self.open_close_undo_chunk(operation)
            else:
                def operation():
                    self.clean(0)
                self.open_close_undo_chunk(operation)


    def reset_help_modifier(self):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ShiftModifier:
            print('Shift+Click')
            
            return test
        elif modifiers == QtCore.Qt.ControlModifier:
            print('Control+Click')
            def operation():
                self.help_UI()
            self.open_close_undo_chunk(operation)

        elif modifiers == (QtCore.Qt.ControlModifier |
                           QtCore.Qt.ShiftModifier):
            print('Control+Shift+Click')
            return test
        else:
            print('Click')
            def operation():
                self.reset_counter()
            self.open_close_undo_chunk(operation)
    
    
    def show_only_selected_modifier(self):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ShiftModifier:
            print('Shift+Click')
            
            return test
        elif modifiers == QtCore.Qt.ControlModifier:
            print('Control+Click')
            def operation():
                self.show_boolean_pieces_from_selected(1)
            self.open_close_undo_chunk(operation)

        elif modifiers == (QtCore.Qt.ControlModifier |
                           QtCore.Qt.ShiftModifier):
            print('Control+Shift+Click')
            return test
        else:
            print('Click')
            def operation():
                self.show_boolean_pieces_from_selected(0)
            self.open_close_undo_chunk(operation)


    def restore_wireframe(self):
        sel = cmds.ls(sl=1, l=1)
        for i in sel:
            check = cmds.getAttr("{}.overrideEnabled".format(i))
            if check:
                cmds.setAttr("{}.overrideEnabled".format(i), 0)
            else:
                attrExist = cmds.attributeQuery('BTnum', node=i, exists=True)
                if attrExist:
                    cmds.setAttr("{}.overrideEnabled".format(i), 1)
                
            
    def set_wireframe_color(self, ctrl, color = (1,1,1)): #changes the color of the wireframe
        rgb = ("R","G","B")
        cmds.setAttr(ctrl + ".overrideEnabled",1)
        cmds.setAttr(ctrl + ".overrideRGBColors",1)
        for channel, color in zip(rgb, color):
            cmds.setAttr(ctrl + ".overrideColor%s" %channel, color)

    def pro_boolean(self, number, tag_number, setnumber):
        result = number
        constant_tag = tag_number
        #BOOLEAN TAG - Tagging system to identify bool_objects that belong to the same base mesh
        #---------------------------------------------------------------------------------------------------------------------------    
        if constant_tag ==1:
            main_bool_id_number = setnumber
        else:
            main_bool_id_number = randrange(1, 9999)
        
        sel = cmds.ls(sl=1, l=1)
        #query if the boolean attribute exists
        attrExist = cmds.attributeQuery('BTnum', node=sel[0], exists=True)
        attr_on_second_sel_exists = False
        second_attrExist = cmds.attributeQuery('BTnum', node=sel[1], exists=True)
        #create the bool_tag_id
        if attrExist:
            get_btag_value = cmds.getAttr("{}.BTnum".format(sel[0]))
        else:
            boolean_serial_key = cmds.addAttr(sel[0], ln="Boolean_Tag_num", sn="BTnum", at="short", k=1, max=9999, dv=main_bool_id_number)
            cmds.setAttr("{}.BTnum".format(sel[0]), l=1)
            get_btag_value = cmds.getAttr("{}.BTnum".format(sel[0]))
            get_btag_value = get_btag_value * 1
            if not second_attrExist:
                inherit_bool_id_key = cmds.addAttr(sel[1], ln="Boolean_Tag_num", sn="BTnum", at="short", k=1, max=9999, dv=get_btag_value)
                cmds.setAttr("{}.BTnum".format(sel[1]), l=1)  
        #---------------------------------------------------------------------------------------------------------------------------    
   
        if second_attrExist:
            #cmds.warning("Second attribute Exists")
            cmds.setAttr("{}.BTnum".format(sel[1]), l=0)  
            cmds.deleteAttr( sel[1], at='Boolean_Tag_num')       
            
            parent = cmds.listRelatives(sel[1], p=1, type="transform")
            if parent == None:
                parent = "mesh"
            
            if parent:
                if result == 1:
                    name = "union"
                elif result == 2:
                    name = "difference"
                elif result == 3:
                    name = "intersection"  
                if "_" in sel[1]:
                    split_name = sel[1].split("_")
                    cmds.warning("parent name is {}".format(split_name)) 
                    parent = [split_name[0]]
                else:
                    parent = ["Boolean"]
            
            ran_name = self.random_name_generator()                
            Name = "{}{}".format(ran_name,parent[0])
            #Name = "num{}_{}".format(str(main_bool_id_number),parent[0])

            new_name = cmds.rename(sel[1], Name)
            
            try:
                parent_to_world = cmds.parent(new_name, w=1)
            except RuntimeError:
                pass
            
            selection2 = cmds.ls(sl=1, l=1)

            cmds.select(sel[0], selection2)
            sel = cmds.ls(sl=1)
            
            #test_sel = cmds.ls(sl=1,l=1)
            #cmds.warning("sel is {}".format(sel))
            #cmds.warning("test_sel is {}".format(test_sel))#

            attr_on_second_sel_exists = True
            try:
                en_overrides = cmds.setAttr("{}.overrideEnabled".format(sel[1]), 0)
                shading_off = cmds.setAttr("{}.overrideShading".format(sel[1]), 1)
                get_shape = cmds.listRelatives(sel[1], s=1)
                #shading_off = cmds.setAttr("{}.intermediateObject".format(get_shape[0]), 1)
                shading_off = cmds.getAttr("{}.intermediateObject".format(get_shape[0]))
                print("shading_off is {}".format(shading_off))
                if shading_off:
                    shading_off = cmds.setAttr("{}.intermediateObject".format(get_shape[0]), 0)
                else:
                    shading_off = cmds.setAttr("{}.intermediateObject".format(get_shape[0]), 0)
                      
            except RuntimeError:
                pass
        
        #===========================================================================================================================
        #Boolean start
        
        sel = cmds.ls(sl=1, l=1)    
        
        listgroups=cmds.ls(type = "transform")
        if result == 1:
            name = "union"
        elif result == 2:
            name = "difference"
        elif result == 3:
            name = "intersection"  
        
        random_name = self.random_name_generator()
        boolean_group_name = "Pro_Bool_{}{}_{}_{}".format(name, sel[-1],random_name, str(get_btag_value))
        boolean_mesh_name= "{}_boolean_{}_{}".format(sel[1], name, str(get_btag_value))
        master_group_name  = "Pro_Boolean_Master"
        operation = number
        
        #Boolean Python version: destroys shading! Dont use anymore// Mel version works bettter
        #bool_operation = cmds.polyBoolOp(o=1, op=number, ch=1, n= "bool_result_00")
        if result == 1:
            mel.eval("PolygonBooleanUnion;")
        elif result == 2:
            mel.eval("PolygonBooleanDifference;")
        elif result == 3:
            mel.eval("PolygonBooleanIntersection;")
        
        bool_sel = cmds.ls(sl=1, l=1)
        print("bool_sel is {}".format(bool_sel))
        
        bool_id_key0 = cmds.addAttr(bool_sel, ln="Boolean_Tag_num", sn="BTnum", at="short", k=1, max=9999, dv=get_btag_value)
        cmds.setAttr("{}.BTnum".format(bool_sel[0]), l=1)   #lock the attribute of the resulted boolean operation
        
        if master_group_name in listgroups:
            Boolean_grp = cmds.group(sel, n= boolean_group_name)
            Master_group = cmds.parent(Boolean_grp, master_group_name)
        else:
            Boolean_grp = cmds.group(sel, n= boolean_group_name)
            Master_group = cmds.group(Boolean_grp, n= master_group_name, w=1)
        
        #____________________________________________________________________
        bool_kids = []
        kids  = cmds.listRelatives(Boolean_grp, ad=1, f=1, type="transform")
        for ki in kids:
            if "transform" in ki:
                print(ki)
                bool_kids.append(ki)
        #new_sel = bool_kids
        print("bool_kids is {}".format(bool_kids))
        #____________________________________________________________________
        cmds.setAttr("{}.BTnum".format(bool_sel[0]), l=1)   #lock the attribute of the resulted boolean operation
        '''
        #new_sel = Boolean_grp
        new_sel = cmds.ls(sl=1)

        children = cmds.listRelatives(new_sel, ad=1, f=1, type = "transform")
        #print("Children are {}".format(children))
        cmds.select(children)
        
        alt_selection = cmds.ls(sl=1,l=1) # used for intersection operations
        #cmds.warning("alt_selection is {}".format(alt_selection))
        ghost_transform = cmds.select(children[-2])
        
        cmds.setAttr("{}.BTnum".format(bool_sel[0]), l=1)   #lock the attribute of the resulted boolean operation
        
        
        
        print("new_sel is {}".format(new_sel))
        print("children is {}".format(children))
        print("alt_selection is {}".format(alt_selection))
        print("bool_sel is {}".format(bool_sel))
        '''
        
        list_of_final_renamed_transforms = [] 
        if result == 2 or result == 1:
            transf_sel = bool_kids[1]

            get_shape_node = cmds.listRelatives(transf_sel, s=1, f=1)
            bool_id_key1 = cmds.addAttr(transf_sel, ln="Boolean_Tag_num", sn="BTnum", at="short", k=1, max=9999, dv=get_btag_value)
            make_visible = cmds.setAttr("{}.visibility".format(transf_sel), 1)
            en_overrides = cmds.setAttr("{}.overrideEnabled".format(transf_sel), 1)
            shading_off = cmds.setAttr("{}.overrideShading".format(get_shape_node[0]), 0)
            
            shape_override_off = cmds.setAttr("{}.overrideEnabled".format(get_shape_node[0]), 0)
            
            shading_off2 = cmds.setAttr("{}.overrideShading".format(transf_sel), 0)
            get_shape = cmds.listRelatives(transf_sel, s=1, f=1)
            shading_off = cmds.setAttr("{}.intermediateObject".format(get_shape[0]), 0)
            
            if result == 2:
                set_wireframe = self.set_wireframe_color(transf_sel, color =(1,0.05,0.05))
            else:
                set_wireframe = self.set_wireframe_color(transf_sel, color =(1,0.3,1))
           
            #lock attr
            cmds.setAttr("{}.BTnum".format(transf_sel), l=1)  
            
            #rename
            getTransfrom = cmds.listRelatives(transf_sel, p=1)
             
             
            re_name= "{}_boolean_{}_{}".format(getTransfrom[0], name, str(get_btag_value)) 
            rename_boolean = cmds.rename(transf_sel, re_name )

            final_sel = cmds.ls(sl=1, l=1)
            
            #cmds.parent(final_sel[0], w=1)  #enable to parent every boolean result to the world

                
        else: #for intersection operations
            list_of_final_renamed_transforms = [] 
            for i in bool_kids:

                if "transform" in i:
                    cmds.select(i)
                    getshape_i = cmds.listRelatives(i, s=1, f=1)
                    
                    bool_id_key = cmds.addAttr(i, ln="Boolean_Tag_num", sn="BTnum", at="short", k=1, max=9999, dv=get_btag_value)
                    make_visible = cmds.setAttr("{}.visibility".format(i), 1)
                    #en_overrides = cmds.setAttr("{}.overrideEnabled".format(i), 1)
                    shading_off = cmds.setAttr("{}.overrideShading".format(i), 0)
                    
                    #shape_override_off = cmds.setAttr("{}.overrideEnabled".format(i), 0)
                    
                    shading_off = cmds.setAttr("{}.overrideShading".format(getshape_i[0]), 0)
                    get_shape = cmds.listRelatives(i, s=1, f=1)
                    
                    
                    #check if the shape node has override enabled / if yes then disable
                    query_enabled = cmds.getAttr("{}.overrideEnabled".format(get_shape[0]))
                    if query_enabled:
                        shape_override_off = cmds.setAttr("{}.overrideEnabled".format(get_shape[0]), 0)
                    
                    
                    get_shape_short = cmds.listRelatives(i, s=1)
                    #print(get_shape)
                    shading_off = cmds.setAttr("{}.intermediateObject".format(get_shape[0]), 0)
                    set_wireframe = self.set_wireframe_color(i, color =(1.0,0.8,0.3))
                    
                    x = get_shape_short[0].replace("Shape", "", 1)
                    #print("x is {}".format(x))
                    getTransfrom = cmds.listRelatives(i, p=1, f=1)
                    getkid = cmds.listRelatives(getTransfrom[0], c=1, f=1)   
                    #print("getkid is {}".format(getkid))   
                    get_shape_kid = cmds.listRelatives(getkid[0], s=1, f=1)  
                    #print("get_shape_kid is {}".format(get_shape_kid))  

                    
                    parent = cmds.listRelatives(i, p=1, type="transform")
                    
                    #Rename section
                    if tag_number==1:
                        parent_split = parent[0].split("_")
                        par= parent_split[0]
                        ran_name = self.random_name_generator()
                        #print("par is {}".format(par))  
                        name = "{}_boolean_intersection_{}".format(par, str(get_btag_value) )#not working as expected / gives same result as else:
                        rename_boolean = cmds.rename(getkid[-1], name)
                        list_of_final_renamed_transforms.append(rename_boolean)                   
                    else:
                        name = "{}_boolean_intersection_{}".format(parent[0],str(get_btag_value) )
                        rename_boolean = cmds.rename(getkid[-1], name)
                        list_of_final_renamed_transforms.append(rename_boolean)
                    
                    if parent == None:
                        boolean_mesh_name= "{}_boolean_{}_{}".format(x, name, get_btag_value)
                        rename_boolean = cmds.rename(getkid[-1], boolean_mesh_name )
                        final_sel = cmds.ls(sl=1, l=1)
                        cmds.setAttr("{}.BTnum".format(final_sel[0]), l=1)   #lock attribute  
                    else:
                        cmds.setAttr("{}.BTnum".format(rename_boolean), l=1)   #lock attribute                                     
                                                       
                else:
                    pass
                 
            #cmds.warning("list_of_final_renamed_transforms is : {}".format(list_of_final_renamed_transforms))
        return bool_sel[0], list_of_final_renamed_transforms, rename_boolean                 
        
    def random_name_generator(self):
        random_number = randrange(1, 999999)
        list_random_name = []
        letters = ["a","b","c","d","e","f","g","h","i","j","k"]
        convert_to_string = str(random_number)
        for number in convert_to_string:
            num = int(number)
            get_letter = letters[num]
            list_random_name.append(get_letter)

        separator = ''
        random_name = separator.join(list_random_name)
        return random_name


    def is_group(self, groupName): 
        try:
            children = cmds.listRelatives(groupName, children=True)
            for child in children:
                if not cmds.ls(child, transforms = True):
                    return False
            return True
        except:
            return False

    def deleteEmptyGroups_inMasterFolder(self):
         
        def delete_empty_grps():
            if cmds.objExists('Pro_Boolean_Master'):
                master_folder = cmds.listRelatives("Pro_Boolean_Master", ad=1, f=1, type = "transform")
                if master_folder ==None:
                    pass
                else:
                    #print("master_folder is {}".format(master_folder))
                    
                    transforms =  master_folder
                    deleteList = []
                    
                    for tran in transforms:
                            if cmds.nodeType(tran) == 'transform':
                                children = cmds.listRelatives(tran, c=True) 
                                if children == None:
                                    deleteList.append(tran)  

                    if len(deleteList) == 0:
                        pass
                    else:
                        cmds.delete(deleteList)
            
        x = range(80)
        if cmds.objExists('Pro_Boolean_Master'):
            for n in x:
                    delete_empty_grps()
        else:
            cmds.warning("Pro_Boolean_Master folder missing.")
        
    def get_all_boolean_pieces(self):

        master_folder = cmds.listRelatives("Pro_Boolean_Master", ad=1, f=1, type = "transform")

        self.deleteEmptyGroups_inMasterFolder()
        master_folder = cmds.listRelatives("Pro_Boolean_Master", ad=1, f=1, type = "transform")

        boolean_pieces = []
        for i in master_folder:
            attrExist = cmds.attributeQuery('BTnum', node=i, exists=True)
            if self.is_group(i):
                pass
            else:
                if attrExist:
                    kids = cmds.listRelatives(i, c=1, f=1, type ="transform")
                    if kids == None:
                        boolean_pieces.append(i)
                else:
                    kids = cmds.listRelatives(i, c=1, f=1, type ="transform")
                    if kids == None:
                        boolean_pieces.append(i)
        return boolean_pieces
    
    def hide_boolean_pieces(self, number):
        
        if not cmds.objExists('Pro_Boolean_Master'):
            cmds.warning("No Booleans exist in scene.")
        
        else:
            result = number    
            all_bool_pieces = self.get_all_boolean_pieces()
            print(all_bool_pieces)
            if result ==1:
                sel = cmds.ls(sl=1, l=1)   
                for i in sel:
                    attr = "{}.visibility".format(i)
                    is_visible = cmds.getAttr(attr)
                    if is_visible:
                        set_invisible = cmds.setAttr(attr, 0)

            else:
                for i in all_bool_pieces:
                    attr = "{}.visibility".format(i)
                    is_visible = cmds.getAttr(attr)
                    if is_visible:
                        set_invisible = cmds.setAttr(attr, 0)

    def show_all_boolean_pieces(self):
        
        if not cmds.objExists('Pro_Boolean_Master'):
            cmds.warning("No Booleans exist in scene.")
        
        else:
            all_bool_pieces = self.get_all_boolean_pieces()
            
            for i in all_bool_pieces:
                attrExist = cmds.attributeQuery('BTnum', node=i, exists=True)
                if attrExist:
                    attr = "{}.visibility".format(i)
                    is_visible = cmds.getAttr(attr)
                    if not is_visible:
                        set_invisible = cmds.setAttr(attr, 1)
        


    def show_boolean_pieces_from_selected(self, number):
        result = number
        select_those_booleans = []
        
        sel = cmds.ls(sl=1, l=1)
        
        
        if len(sel)==0:
            cmds.warning("Nothing selected. Please select an object with pro boolean operations in order to only show those in your scene.")
        else:    
            show_from_object = False
            empty = []
            pieces = self.get_all_boolean_pieces()
            #print(pieces)
            
            #check bool folder
            folder_exists = False
            if cmds.objExists('Pro_Boolean_Master'):
                master_folder = cmds.listRelatives("Pro_Boolean_Master", ad=1, f=1, type = "transform")
                folder_exists = True
            
            
            inside_folder = []
            outside_folder = []
            get_tag_numbers = []
            for item in sel:
                if item in master_folder:
                    inside_folder.append(item)
                else:
                    outside_folder.append(item)
            
            #for piece in inside_folder:
            #    attrExist = cmds.attributeQuery('BTnum', node=piece, exists=True)
            #    if attrExist:
            #        get_btag_value = cmds.getAttr("{}.BTnum".format(piece))
            #        get_tag_numbers.append(get_btag_value)
                    
                
            for pie in outside_folder:
                attrExist = cmds.attributeQuery('BTnum', node=pie, exists=True)
                if attrExist:
                    get_btag_value = cmds.getAttr("{}.BTnum".format(pie))
                    #print(get_btag_value)
                    get_tag_numbers.append(get_btag_value)                
            
            sort_tag_num = list(dict.fromkeys(get_tag_numbers))   
                
            #print("inside_folder is {}".format(inside_folder))
            #print("outside_folder is {}".format(outside_folder))
            #print("sort_tag_num is {}".format(sort_tag_num))
            
            #print(len(sort_tag_num))

            tagged_pieces = []
            counter = 0
            for iteration in range(len(sort_tag_num)):
                for x in pieces:
                    attrExist = cmds.attributeQuery('BTnum', node=x, exists=True)
                    if attrExist:
                        get_btag_value = cmds.getAttr("{}.BTnum".format(x))
                        if get_btag_value == sort_tag_num[counter]:
                            tagged_pieces.append(x)
                counter+=1       
            
            for p in pieces: #set all in the folder to invisible
                cmds.setAttr("{}.visibility".format(p), 0)            
            
            
            if not inside_folder and outside_folder:
                for tag in tagged_pieces: #same tag numb ids as selection will be visible
                    cmds.setAttr("{}.visibility".format(tag), 1) 
                    
            elif  inside_folder or inside_folder and outside_folder:
                for i in sel:#make your selection visible
                    cmds.setAttr("{}.visibility".format(i), 1)
            
            if result ==1:   
                cmds.select(sel, tagged_pieces)
        

    def cycle_booleans(self, number):
        result = number
        sel = cmds.ls(sl=1, l=1)
        try:
            attrExist = cmds.attributeQuery('BTnum', node=sel[0], exists=True)#
        except IndexError:
            pass
        
        if len(sel) != 1:
            cmds.warning("Please select a pro boolean object to cycle through.")
       
        if len(sel) == 1 and attrExist==False:
            cmds.warning("Please select a pro boolean object to cycle through.")
                    
        elif len(sel)==1 and attrExist:

            attrExist = cmds.attributeQuery('BTnum', node=sel[0], exists=True)
            same_bool_tag_number = []

            if attrExist:
                get_btag_value = cmds.getAttr("{}.BTnum".format(sel[0]))
                all_bool_pieces = self.get_all_boolean_pieces()
                
                filter_bool_pieces = []
                for piece in all_bool_pieces:
                    attrExist = cmds.attributeQuery('BTnum', node=piece, exists=True)
                    if attrExist:
                        kids = cmds.listRelatives(piece, c=1, f=1, type="transform")
                        if kids == None:
                            filter_bool_pieces.append(piece)
                        
                
                
                for item in filter_bool_pieces: #filters only the same tagged booleans
                    
                    if str(get_btag_value) in item:
                        same_bool_tag_number.append(item)

                    attr = "{}.visibility".format(item)
                    is_visible = cmds.getAttr(attr)
                    if is_visible:
                        set_invisible = cmds.setAttr(attr, 0)  
                
                counter =0
                if result == 1:
                    same_bool_tag_number.reverse()
                
                for boolean in same_bool_tag_number:
                    if sel[0] ==boolean:
                        counter+=1
                        break
                    else:
                        counter+=1
                

                length_same_bool_tag_number = len(same_bool_tag_number)
                
                if counter == length_same_bool_tag_number:
                    counter = 0
                                  
                if result ==1:
                    #___________________________________________________________________
                    calculate_cycle = "{}/{}".format(abs(counter-len(same_bool_tag_number)), len(same_bool_tag_number))
                    self.boolean_number.setText(calculate_cycle)
                    #___________________________________________________________________            

                else:
                    #___________________________________________________________________
                    calculate_cycle = "{}/{}".format(counter+1, len(same_bool_tag_number))
                    self.boolean_number.setText(calculate_cycle)
                    #___________________________________________________________________
                                    
                cyled_boolean = cmds.select(same_bool_tag_number[counter])
                
                final_sel = cmds.ls(sl=1, l=1)        
                attr = "{}.visibility".format(final_sel[0])
                is_visible = cmds.getAttr(attr)
                if not is_visible:
                    set_invisible = cmds.setAttr(attr, 1)  

    def freeze_boolean_piece(self):
        sel = cmds.ls(sl=1)
        shape = cmds.listRelatives(sel[0], s=1, f=1)
        #print(shape)
        bool_list = []
        connections = cmds.listConnections(shape[0])
        #print("connections is {}".format(connections))
        set_wireframe = self.set_wireframe_color(sel[0], color =(0.45,0.45,0.45))
        if "polyCBoolOp" in connections[0]:
            cmds.setAttr("{}.nodeState".format(connections[0]), 2)
            bool_list.append(connections[0])
            
        deeper_connections = cmds.listConnections(connections[0])
        #print("deeper_connections is {}".format(deeper_connections))
        
        list_history = cmds.listHistory(deeper_connections[0])
        #print("list_history is {}".format(list_history))
        for i in list_history:
            if connections[0] == i:
                cmds.delete(i)
                            
    def xray_toggle(self):
        query_xray = cmds.modelEditor("modelPanel4", q=1,  xr=1)
        if query_xray:
            mel.eval("setXrayOption false modelPanel4;")
        else:
            mel.eval("setXrayOption true modelPanel4;")
          

        
    def reset_counter(self):
        sel = cmds.ls(sl=1, l=1)
        #TODO select a bool mesh/ hit the button and it should tell you which order it is in  e.g. 4/6
        same_bool_tag_number = []
        if len(sel) ==0:
            cmds.warning("Nothing selected, please select a Pro_Boolean mesh to query the amount of booleans it has.")
            self.boolean_number.setText(str(0))

        else:
            attrExist = cmds.attributeQuery('BTnum', node=sel[0], exists=True)
            if not attrExist:
                #cmds.warning("Boolean tag id attribute missing. Please select a mesh that has been booleaned using the Pro_Boolean tool.")
                self.boolean_number.setText(str(0))
            else:

                get_btag_value = cmds.getAttr("{}.BTnum".format(sel[0]))
                all_bool_pieces = self.get_all_boolean_pieces()

                for item in all_bool_pieces: #filters only the same tagged booleans
                
                    split_item = item.split("|")[-1]

                    if str(get_btag_value) in split_item:
                        same_bool_tag_number.append(item)
                        self.boolean_number.setText(str(len(same_bool_tag_number)))

    def deleteEmptyGroups(self):
        self.clean_groups_2()


    def clean(self, number):

        result = number
        
        folder_exists = False
        sel = cmds.ls(sl=1)
        folder_kids = []
        
        for allitems in sel:
            
            if cmds.objExists('Pro_Boolean_Master'):
                master_folder_children = cmds.listRelatives("Pro_Boolean_Master", c=1, f=1, type = "transform")
                master_folder = cmds.listRelatives("Pro_Boolean_Master", ad=1, f=1, type = "transform")
                folder_exists = True
                
                if master_folder:
                    for file in master_folder:
                            folder_kids.append(file)   
            
            #delete Attribute on selected object
            if result==0:
                #print("Clean pass 1")
                if folder_exists:
                    for i in sel:
                        attrExist = cmds.attributeQuery('BTnum', node=i, exists=True)

                        if attrExist:
                            cmds.setAttr("{}.BTnum".format(i), l=0)  
                            cmds.deleteAttr( i, at='Boolean_Tag_num') 
                            cmds.inViewMessage(amg='<span style=\"color:#FF9933;\">Boolean</span> attribute <hl>Removed</hl>.', pos='topCenter', fade=True, fit=300, fst=900, fot=300 )  
                    self.deleteEmptyGroups_inMasterFolder() 
                else:
                    for i in sel:
                        attrExist = cmds.attributeQuery('BTnum', node=i, exists=True)

                        if attrExist:
                            cmds.setAttr("{}.BTnum".format(i), l=0)  
                            cmds.deleteAttr( i, at='Boolean_Tag_num')  
                            try:
                                self.deleteEmptyGroups_inMasterFolder() 
                            except ValueError:
                                pass
                            cmds.inViewMessage(amg='<span style=\"color:#FF9933;\">Boolean</span> attribute <hl>Removed</hl>.', pos='topCenter', fade=True, fit=300, fst=900, fot=300 ) 
                            #cmds.inViewMessage(bkc=0x00000000, amg='<span style=\"color:#FF9933;\">Boolean</span> attribute <hl>Removed</hl>.', pos='topCenter', fade=True, fit=300, fst=900, fot=300 ) 
                            cmds.warning("Boolean attribute deleted.")

            #clean (master group)
            elif result ==1:   #CAN BREAK OUT OF THE LOOP
                transforms = cmds.ls(transforms=True, l=1)
                #print(transforms)
                polyMeshes = cmds.filterExpand(transforms, selectionMask=12)
                #print(polyMeshes) #need to only get meshes that exist outside the Pro_Boolean folder in Maya
                alltags = []
                
                '''
                list_comparison = list(set(transforms).difference(folder_kids))
                #print(list_comparison)
                if "|Pro_Boolean_Master" in list_comparison:
                    list_comparison.remove("|Pro_Boolean_Master")   
                polylist_comparison = cmds.filterExpand(list_comparison, selectionMask=12)
                #print("polylist_comparison is {}".format(polylist_comparison))       #returns all meshes outside the master folder
                '''

                for mesh in polyMeshes:
                #for mesh in polylist_comparison: #because of boolean history it also deletes the mesh outside the master folder // 
                    attrExist = cmds.attributeQuery('BTnum', node=mesh, exists=True)
                    if attrExist:
                        get_btag_value = cmds.getAttr("{}.BTnum".format(mesh))
                        alltags.append(get_btag_value)
                
                if folder_exists:
                    for i in master_folder_children:
                        split_i = i.split("_")
                        get_number = (split_i[-1])
                        
                        if get_number not in str(alltags):
                            cmds.delete(i)
                            cmds.inViewMessage(amg='<hl>Pro Boolean Master</hl> folder cleaned.', pos='topCenter', fade=True, fit=300, fst=900, fot=300 ) 
                else:
                    cmds.warning("Pro Boolean Master folder is empty/or all Boolean_Tag_num attributes within the folder are currently used in your scene.")
                    
                self.deleteEmptyGroups_inMasterFolder()
        
            
   
    def bake_options(self, number):    

        sel = cmds.ls(sl=1, l=1)
        
        if cmds.objExists('Pro_Boolean_Master'):
      
            for i in sel:
                meshes_in_scene_with_same_id = []
                
                attrExist = cmds.attributeQuery('BTnum', node=i, exists=True)
                if attrExist:
                    bool_id = cmds.getAttr("{}.BTnum".format(i)) #get the ID of your selection
                    
                    allobjects = cmds.ls(type="transform",l=1)  #search for all objects in scene with same id
                    for obj in allobjects:
                        shape = cmds.listRelatives(obj, s=1, f=1)
                        if shape:
                            parent = cmds.listRelatives(obj, ap=1, f=1, type="transform")
                            if parent:
                                split_parent = parent[0].split("|")[1]
                            if parent == None or "Pro_Boolean_Master" not in split_parent: #filter to get all object transform outside the Pro_Boolean so we can quey the id
                                id_num = cmds.attributeQuery('BTnum', node=obj, exists=True)
                                
                                if id_num:
                                    get_id = cmds.getAttr("{}.Boolean_Tag_num".format(obj))
                                    if get_id == bool_id:
                                        meshes_in_scene_with_same_id.append(obj)
                    
                if meshes_in_scene_with_same_id:
                    bool_meshes = []
                    
                    for obj in meshes_in_scene_with_same_id:
                        cmds.delete(obj, ch=1)
                        cmds.setAttr("{}.BTnum".format(obj), l=0)  
                        cmds.deleteAttr( obj, at='Boolean_Tag_num') 
                    
                    for mesh in meshes_in_scene_with_same_id:

                        if number == 1:
                            master_folder = cmds.listRelatives("Pro_Boolean_Master", c=1, f=1, type = "transform")
                            if master_folder:
                                for file in master_folder:
                                    get_num_from_master_folder = file.split("_")[-1]
                                    if int(get_num_from_master_folder) == bool_id:
                                        cmds.delete(file)
                            
                        else:   
                            all_bool_pieces = self.get_all_boolean_pieces()
                            for piece in all_bool_pieces:
                                attrExist = cmds.attributeQuery('BTnum', node=piece, exists=True)
                                if attrExist:
                                    get_num_from_file = piece.split("_")[-1]
                                    if int(get_num_from_file) == bool_id:
                                        
                                        cmds.setAttr("{}.BTnum".format(piece), l=0)  
                                        cmds.deleteAttr( piece, at='Boolean_Tag_num') 
                                        
                                        cmds.select(piece)
                                        self.restore_wireframe()
                                        bool_meshes.append(piece)
                                      
                    if bool_meshes:
                        cmds.select(bool_meshes)
                        cmds.parent(bool_meshes, w=1)
                        
                        self.clean_groups_2()
                        
            


    def clean_empty_groups(self):
        self.deleteEmptyGroups()

        
    def tag_id_checker(self): #this will check if any of your selection (apart from the first one) has a separate bool tag id / if it does it will bake those assets.

        sel = cmds.ls(sl=1,l=1)
        selection = cmds.ls(sl=1,l=1)
        attrExist = cmds.attributeQuery('BTnum', node=selection[0], exists=True)
        #print(attrExist)
        tag_number_clashing = False
        empty = []
        if attrExist:
            get_btag_value_of_fist_sel = cmds.getAttr("{}.BTnum".format(selection[0]))
            #print("get_btag_value_of_fist_sel is {}".format(get_btag_value_of_fist_sel))
            for i in selection[1:]:
                
                attrExist_for_i = cmds.attributeQuery('BTnum', node=i, exists=True)
                if attrExist_for_i:
                    
                    get_btag_value = cmds.getAttr("{}.BTnum".format(i))
                    #print("get_btag_value is {}".format(get_btag_value))
                    
                    if get_btag_value != get_btag_value_of_fist_sel:
                        tag_number_clashing = True
                        cmds.warning("Tags dont match")
                        cmds.select(i)
                        bm = self.bake_options(1)
                        new_sel = cmds.ls(sl=1, l=1)
                        empty.append(new_sel[0])
                    
                else:
                    #print("Tags match")
                    empty.append(i)
     
            cmds.select(sel[0], empty)
            sel = cmds.ls(sl=1)
            selection = cmds.ls(sl=1,l=1)
        
        return tag_number_clashing, sel, selection
            
    def cycle_operations(self):
        
        sel = cmds.ls(sl=1)
        for i in sel:    
            attrExist = cmds.attributeQuery('BTnum', node=i, exists=True)
            if attrExist:
                shape = cmds.listRelatives(i, s=1, f=1)
                connections = cmds.listConnections(shape[0])

                if "polyCBoolOp" in connections[0]:
                    
                    number = cmds.getAttr("{}.operation".format(connections[0]))

                    get_bool_operation = number + 1
                    
                    if get_bool_operation > 3:
                        get_bool_operation = 1
                           
                    for x in range(1):
                        
                        if get_bool_operation == 1:
                            set_wireframe = self.set_wireframe_color(i, color =(1,0.3,1))
                            cmds.setAttr("{}.operation".format(connections[0]),1)
                            cmds.inViewMessage( amg='Operation changed to <hl>Union</hl>.', pos='topRight', fade=True, fit=300, fst=900, fot=300 ) 
                            print("Boolean operation {} changed to union.".format(i))
                            
                        elif get_bool_operation == 2:
                            set_wireframe = self.set_wireframe_color(i, color =(1,0.05,0.05))
                            cmds.setAttr("{}.operation".format(connections[0]),2)
                            cmds.inViewMessage( amg='Operation changed to <hl>Difference</hl>.', pos='topRight', fade=True, fit=300, fst=900, fot=300 )
                            print("Boolean operation {} changed to difference.".format(i))
      
                        elif get_bool_operation == 3:
                            set_wireframe = self.set_wireframe_color(i, color =(1.0,0.8,0.3))
                            cmds.setAttr("{}.operation".format(connections[0]),3)
                            cmds.inViewMessage( amg='Operation changed to <hl>Intersection</hl>.', pos='topRight', fade=True, fit=300, fst=900, fot=300 )
                            print("Boolean operation {} changed to intersection.".format(i))


    def clean_duplicated_mesh(self):

        id_not_present = False
        counter_sel = cmds.ls(sl=1, l=1)
        sel = cmds.ls(sl=1, l=1)
        n_check = []
        
        counter = 0
        for check in sel: #deselect objects that have no booelan attr
            attrExist = cmds.attributeQuery('BTnum', node=check, exists=True) 
            if not attrExist:
                print(check)
                id_not_present = True
                n_check.append(check)  
                counter +=1
        deselect = cmds.select(n_check, d=1)


        if counter == len(sel): #if no attributes on all objects in a selection instead of deselecting them select them again
            cmds.select(sel)

        sel = cmds.ls(sl=1, l=1)
        selection = cmds.ls(sl=1)
        
        tags = []
        new_id_tag_number = randrange(1, 9999)
        #id_not_present = False
        
        group_selected = False
        for i in selection:
            if self.is_group(i):
                group_selected = True
              
        
        if len(sel) == 0:
            cmds.warning("Please make a selection. If the selection has a Bool_Tag_num it will replace it with a new random one. //Important ensure you select all associated boolean meshes that have an impact on your selection.")
        elif len(sel) ==1:
            cmds.warning("Insufficient number of selected objects. Please select an object that has a pro boolean operation followed by the boolean objects that affect that object.")
        
        elif group_selected:
            cmds.warning("Selection error! Group selected. Please select an object that has a pro boolean operation followed by the boolean objects that affect that object.")
        
        elif counter == len(counter_sel):
            cmds.warning("None of your selected object have a Boolean_Tag_num attribute. Please make sure your selection include the attribute by performing a proboolean operation.")
        
        else:
            for i in sel:
                attrExist = cmds.attributeQuery('BTnum', node=i, exists=True)
                if attrExist:
                    get_btag_value = cmds.getAttr("{}.BTnum".format(i))
                    tags.append(get_btag_value)

                    

            get_tag_numbers = list(dict.fromkeys(tags))
            #print(get_tag_numbers)
            
            if len(get_tag_numbers) > 1:
                cmds.warning("Selection contains more than one Booelan_tag_num ids. Please make sure your selection shares the same number. Either delete the attribute from your selection or if it a selection error please deselect the odd one.")
            
            else:
                folder_exists = False
                if cmds.objExists('Pro_Boolean_Master'):
                    master_folder = cmds.listRelatives("Pro_Boolean_Master", ad=1, f=1, type = "transform")
                    folder_exists = True

                #set the tag id for assets outside the Master folder
                mesh_inside_master_folder = []
                for i in sel:
                    if i in master_folder:
                        mesh_inside_master_folder.append(i)
               
                for i in mesh_inside_master_folder:
                    attrExist = cmds.attributeQuery('BTnum', node=i, exists=True)
                    if attrExist:
                        cmds.setAttr("{}.BTnum".format(i), l=0)  
                        cmds.deleteAttr( i, at='Boolean_Tag_num') 
                        boolean_serial_key = cmds.addAttr(i, ln="Boolean_Tag_num", sn="BTnum", at="short", k=1, max=9999, dv=new_id_tag_number)
                        cmds.setAttr("{}.BTnum".format(i), l=1)  

                    else:
                        boolean_serial_key = cmds.addAttr(i, ln="Boolean_Tag_num", sn="BTnum", at="short", k=1, max=9999, dv=new_id_tag_number)
                        cmds.setAttr("{}.BTnum".format(i), l=1)                          

                #set the tag id for assets outside the Master folder
                mesh_outside_master_folder = []
                for i in sel:
                    if i not in master_folder:
                        mesh_outside_master_folder.append(i)
                
                    
                for i in mesh_outside_master_folder:
                    attrExist = cmds.attributeQuery('BTnum', node=i, exists=True)
                    if attrExist:
                        cmds.setAttr("{}.BTnum".format(i), l=0)  
                        cmds.deleteAttr( i, at='Boolean_Tag_num') 
                        boolean_serial_key = cmds.addAttr(i, ln="Boolean_Tag_num", sn="BTnum", at="short", k=1, max=9999, dv=new_id_tag_number)
                        cmds.setAttr("{}.BTnum".format(i), l=1)  

                    else:
                        boolean_serial_key = cmds.addAttr(i, ln="Boolean_Tag_num", sn="BTnum", at="short", k=1, max=9999, dv=new_id_tag_number)
                        cmds.setAttr("{}.BTnum".format(i), l=1)            
                #---------------------------------------------------------------------------    

                #Get the parent folders of the selected assets and rename them
                mesh_inside_master_folder = []
                for i in sel:
                    if i in master_folder:
                        mesh_inside_master_folder.append(i)                
                temp = []
                final_sel = []
                
                granparents_short = []

                if folder_exists:
                    if mesh_inside_master_folder:
                        granparents = []
                        granparents_short = []
                        master_counter = 0
                        for obj in mesh_inside_master_folder:                  
                            #get granparent
                            #print("obj is {}".format(obj))
                            obj_parent = cmds.listRelatives(obj, p=1, f=1, type = "transform")
                            #print("obj_parent is {}".format(obj_parent))
                            obj_granparent_long = cmds.listRelatives(obj_parent[0], p=1, f=1, type = "transform")
                            obj_granparent_short = cmds.listRelatives(obj_parent[0], p=1, type = "transform")
                            granparents.append(obj_granparent_long[0])
                            granparents_short.append(obj_granparent_short[0])
                        
                        filtered_grandads = list(dict.fromkeys(granparents))             
                        
                        counter = 0
                        for grandad in filtered_grandads:  
                            ran_name = self.random_name_generator()
                            split_granparent_short = granparents_short[counter].split("_")
                            #print("split_granparent_short is {}".format(split_granparent_short))
                            split_granparent_short.pop(0)
                            split_granparent_short.pop(-1)
                            
                            #print("split_granparent_short is {}".format(split_granparent_short))
                            split_granparent_short.insert(0, ran_name)
                            split_granparent_short.append(str(new_id_tag_number))
                            #print("split_granparent_short is {}".format(split_granparent_short))                
                            s = "_"
                        
                            gran_new_name = s.join(split_granparent_short)
                            #print(gran_new_name)
                            grandparent_group = cmds.rename (grandad, gran_new_name)  
                            cmds.select(grandparent_group)

                            
                            new_sel = cmds.ls(sl=1, l=1)
                            temp.extend(new_sel)
                            counter+=1
                       
                            master_counter+=1

                    #_______________________________________________________________________________________________________
                    
                    #Set the id of all children in the above parent groups to be all the same //  and rename those assets that have the tag id attribute
                    if master_counter >= 1:
                        for kid in temp:
                            allkids = cmds.listRelatives(kid, ad=1, f=1, type="transform") 
                            
                            for child in allkids:
                                #print(child)
                                attrExist = cmds.attributeQuery('BTnum', node=child, exists=True)
                                if attrExist:
                                    #print("Yes")
                                    cmds.setAttr("{}.BTnum".format(child), l=0)  
                                    cmds.setAttr("{}.Boolean_Tag_num".format(child), new_id_tag_number)
                                    cmds.setAttr("{}.BTnum".format(child), l=1) 
                                else:
                                    pass
                                    #print("NO")
                        #-----------------------------------------------------------------------------------
                        
                        #Rename process
                        for t in temp:
                            all_kids = cmds.listRelatives(t, ad=1, f=1, type="transform")
                            all_kids_short = cmds.listRelatives(t, ad=1, type="transform")
                            
                            kids_with_tag = []
                            for kid in all_kids:
                                attrExist = cmds.attributeQuery('BTnum', node=kid, exists=True)
                                #print("attrExist is {}".format(attrExist))
                                if attrExist:
                                    kids_with_tag.append(kid)
                            
                            kids_with_tag_short = []
                            for skid in all_kids_short:
                                attrExist = cmds.attributeQuery('BTnum', node=skid, exists=True)
                                if attrExist:
                                    kids_with_tag_short.append(skid)
                                       
                            rename_counter = 0
                            for i in kids_with_tag:  
                                #print(i)
                                if self.is_group(i):
                                    pass
                                else:
                                    short_name = kids_with_tag_short[rename_counter]
                                    
                                    split_i = short_name.split("_")
                                    remove_last = (split_i[:-1])
                                    remove_last.append(str(new_id_tag_number))
                                    #print(remove_last)
                                    s = "_"
                                    new_name = s.join(remove_last)
                                    #print(new_name)
                                    
                                    cmds.select(i)
                                                                        
                                    try:
                                        cmds.rename (new_name)
                                    except RuntimeError:
                                        pass
                                    
                                    n_sel = cmds.ls(sl=1, l=1)
                                    final_sel.extend(n_sel)
                                    
                                rename_counter+=1
                    
                    cmds.select(final_sel, mesh_outside_master_folder)
                    cmds.inViewMessage(amg='Boolean attribute <hl>Replaced</hl>.', pos='topCenter', fade=True, fit=300, fst=900, fot=300 ) 
                    
            if id_not_present:
                cmds.warning("New Tag_num created. Assets with no Boolean_Tag_number {} attribute were deselected.".format(n_check))
       
        
        
    def group_selection(self, number):
        result = number
        sel = cmds.ls(sl=1, l=1)
        empty = []
        for i in sel:
            if self.is_group(i):
                allkids = cmds.listRelatives(i, ad=1, f=1, type="transform")
                for kid in allkids:
                    if self.is_group(kid):
                        pass
                    else:
                        empty.append(kid)             
            else:
                empty.append(i)
        if result ==1:
            #print("PART 1")
            sel = empty
            cmds.select(sel)
            return sel
        else:
            #print("PART 2")
            new_sel = cmds.ls(sl=1)
            cmds.select(new_sel)
            return new_sel
        
    def group_selection2(self):
        sel = cmds.ls(sl=1, l=1)
        empty = []
        for i in sel:
            if self.is_group(i):
                allkids = cmds.listRelatives(i, ad=1, f=1, type="transform")
                for kid in allkids:
                    if self.is_group(kid):
                        pass
                    else:
                        empty.append(kid)             
            else:
                empty.append(i)
        if empty:
            cmds.select(empty)
        else:
            return sel

    def extrude_panel(self, sel):
        for i in sel[1:]:
            extrude = cmds.polyExtrudeFacet(i)
            cmds.setAttr("{}.thickness".format(extrude[0]), 0.001)
        cmds.select(sel)
        return sel
        
    def check_for_groups(selection):
        group_selected = False
        for i in selection:
            if self.is_group(i):
                group_selected = True
        return group_selected
        

    def clean_groups_2(self):
        if cmds.objExists('Pro_Boolean_Master'):
            master_children = cmds.listRelatives("Pro_Boolean_Master", c=1, f=1, type = "transform")
            empty_groups= []

            if master_children: 
                for child in master_children:
                    empty = []
                    allkids = cmds.listRelatives(child, ad=1, f=1, type="transform")
                    for kid in allkids:
                        nokids = cmds.listRelatives(kid, c=1, f=1, type="transform")
                        shape = cmds.listRelatives(kid, s=1, f=1)
                        if nokids == None and shape:
                            empty.append(kid)

                    if len(empty) !=2:
                        empty_groups.append(child)
            cmds.delete(empty_groups)

    def create_attribute(self):

        main_bool_id_number = randrange(1, 9999)
        sel = cmds.ls(sl=1, l=1)
        selection = cmds.ls(sl=1)
        
        if cmds.objExists('Pro_Boolean_Master'):
            master_folder = cmds.listRelatives("Pro_Boolean_Master", ad=1, f=1, type = "transform")
        
        counter =0
        for i in sel:
            attrExist = cmds.attributeQuery('BTnum', node=i, exists=True)
            if attrExist:
                cmds.setAttr("{}.BTnum".format(i), l=0)  
                cmds.deleteAttr( i, at='Boolean_Tag_num') 
                inherit_bool_id_key = cmds.addAttr(i, ln="Boolean_Tag_num", sn="BTnum", at="short", k=1, max=9999, dv=main_bool_id_number)
                cmds.setAttr("{}.BTnum".format(i), l=1)
                cmds.inViewMessage(amg='Boolean attribute <hl>Reset</hl>.', pos='topCenter', fade=True, fit=300, fst=900, fot=300 )  
            
                if i in master_folder: #rename if its master folder
                    
                    parent = cmds.listRelatives(i, p=1, f=1, type="transform")
                    granparent_long = cmds.listRelatives(parent[0], p=1, f=1, type="transform")
                    granparent_short = cmds.listRelatives(parent[0], p=1, type="transform")
                   
                    split_short = granparent_short[0].split("_")
                    granparent_short_pop = split_short.pop(-1)
                    underscore = "_"
                    join_name = underscore.join(split_short)
                    final_name = "{}_{}".format(join_name, main_bool_id_number)
                    new_grp_name = cmds.rename(granparent_long[0], final_name)
                    
                    child = cmds.listRelatives(new_grp_name, c=1, f=1, type="transform")
                    child_long = cmds.listRelatives(child[-1], c=1, f=1, type="transform")
                    child_short = cmds.listRelatives(child[-1], c=1, type="transform")
                    
                    split_child_short = child_short[0].split("_")
                    pop_child_short = split_child_short.pop(-1)
                    underscore = "_"
                    join_p_name = underscore.join(split_child_short)
                    f_name = "{}_{}".format(join_p_name, main_bool_id_number)
                    new_name = cmds.rename(child_long[0], f_name)
                    
                    counter+=1
           
            else:
                inherit_bool_id_key = cmds.addAttr(i, ln="Boolean_Tag_num", sn="BTnum", at="short", k=1, max=9999, dv=main_bool_id_number)
                cmds.setAttr("{}.BTnum".format(i), l=1) 
                cmds.inViewMessage(amg='Boolean attribute <hl>Created</hl>.', pos='topCenter', fade=True, fit=300, fst=900, fot=300 ) 

    def open_close_undo_chunk(self, func):
        cmds.undoInfo(openChunk=True)
        try:
            func()
        finally:
            cmds.undoInfo(closeChunk=True)
            
    def help_UI(self):
        if cmds.window("Help", exists=True):
            cmds.deleteUI("Help")
        window = cmds.window('Help', s=0, bgc =[0.3, 0.3, 0.3], widthHeight=(300, 330))
        #cmds.flowLayout(cs=350,w=400)
        
        
        #__________________________________________________________________________________________________________________
        #second window
        def SecondWindow(*args):  
            if cmds.window("Hotkeys", exists=True):
                cmds.deleteUI("Hotkeys")
            window = cmds.window('Hotkeys', s=0, bgc =[0.3, 0.3, 0.3], widthHeight=(300, 513))
            
            #IMAGES PATH
            bool_union = cmds.internalVar(upd=1) +"/icons/pro_boolean/boolean_union_lb.jpg"
            bool_difference = cmds.internalVar(upd=1) +"/icons/pro_boolean/boolean_difference_lb.jpg"
            bool_intersection = cmds.internalVar(upd=1) +"/icons/pro_boolean/boolean_intersection_lb.jpg"
            bool_panel = cmds.internalVar(upd=1) +"/icons/pro_boolean/boolean_panel_lb.jpg"
            bool_difference_panel = cmds.internalVar(upd=1) +"/icons/pro_boolean/boolean_difference_panel_lb.jpg"
            bool_bake = cmds.internalVar(upd=1) +"/icons/pro_boolean/boolean_bake_lb.jpg"
            
            
            cmds.columnLayout( adjustableColumn=True )
            #cmds.paneLayout()
            
            cmds.image(w=300, h=30, image=bool_union)     #boolean union hotkey
            cmds.scrollField( editable=False, wordWrap=True,  w=300, h=50, fn ="boldLabelFont", text='import Pro_Boolean\nboolean = OpenImportDialog()\nboolean.boolean_union_operations()' )

            cmds.image(w=300, h=30, image=bool_difference)     #boolean difference hotkey
            cmds.scrollField( editable=False, wordWrap=True,  w=300, h=50, fn ="boldLabelFont", text='import Pro_Boolean\nboolean = OpenImportDialog()\nboolean.boolean_difference_operations()' )

            cmds.image(w=300, h=30, image=bool_intersection)     #boolean intersection hotkey
            cmds.scrollField( editable=False, wordWrap=True,  w=300, h=50, fn ="boldLabelFont", text='import Pro_Boolean\nboolean = OpenImportDialog()\nboolean.boolean_intersection_operations()' )

            cmds.image(w=300, h=30, image=bool_panel)     #boolean panel hotkey
            cmds.scrollField( editable=False, wordWrap=True,  w=300, h=50, fn ="boldLabelFont", text='import Pro_Boolean\nboolean = OpenImportDialog()\nboolean.bool_panel()' )

            cmds.image(w=300, h=30, image=bool_difference_panel)     #boolean panel difference hotkey
            cmds.scrollField( editable=False, wordWrap=True,  w=300, h=50, fn ="boldLabelFont", text='import Pro_Boolean\nboolean = OpenImportDialog()\nboolean.boolean_panel_difference_operations(1)' )

            cmds.image(w=300, h=30, image=bool_bake)     #boolean bake hotkey
            cmds.scrollField( editable=False, wordWrap=True,  w=300, h=50, fn ="boldLabelFont", text='import Pro_Boolean\nboolean = OpenImportDialog()\nboolean.bake_options(1)' )

            #----------------------------------------------
            cmds.button( label='Close',bgc=[0.2,0.2,0.2],  w=150, h=30, command=('cmds.deleteUI(\"' + window + '\", window=True)') )
            #----------------------------------------------  

            cmds.showWindow(window)
            cmds.showWindow('Hotkeys')
        
        #_____________________________________________________________________________________________________________________
        
        
        #IMAGES PATH
        hotkeys_doc_lb_path = cmds.internalVar(upd=1) +"/icons/pro_boolean/boolean_hotkey_documentation_lb.jpg"
        hotkeys_lb_path = cmds.internalVar(upd=1) +"/icons/pro_boolean/boolean_hotkeys_lb.jpg"
        hotkeys_store = cmds.internalVar(upd=1) +"/icons/pro_boolean/store_lb.jpg"
        artstation_button_icon = cmds.internalVar(upd=1) +"/icons/pro_boolean/artstation_button_icon.jpg"
        gumroad_button_icon = cmds.internalVar(upd=1) +"\icons\pro_boolean\gumroad_button_icon.jpg"
        hotkeys_button_icon = cmds.internalVar(upd=1) +"/icons/pro_boolean/boolean_hotkey_btn.jpg"
        
        #pdf_path = cmds.internalVar(upd=1) +"\quick_circular_array\quick_circular_array.pdf"
        pdf_path = cmds.internalVar(upd=1) +"/icons/pro_boolean/Pro_Boolean_Documentation.pdf"
        pdf_button_path = cmds.internalVar(upd=1) + "/icons/pro_boolean/pdf_documentation_btn.jpg" #TODO NEEDS UPDATED PATH
        
        def artstation():
            cmds.launch( web = "https://www.artstation.com/michailisaakidis/store")
            
        def gumroad():
            cmds.launch( web = "https://mike3d.gumroad.com/")
        
        def launch_pdf(*args):
            
            cmds.launch(pdf=pdf_path)   

        cmds.columnLayout( adjustableColumn=True )

        #LABELS AND BUTTONS
        
             
        cmds.image(w=300, h=50, image=hotkeys_doc_lb_path)  
        cmds.iconTextButton(w=300, h=50, style='iconAndTextVertical', image1=hotkeys_button_icon, command=SecondWindow )  
        cmds.iconTextButton(w=300, h=50, style='iconAndTextVertical', image1=pdf_button_path, command=launch_pdf )  
        
        cmds.image(w=300, h=50, image=hotkeys_store)  
        cmds.iconTextButton(w=300, h=50, style='iconAndTextVertical', image1=artstation_button_icon,command=artstation ) 
        cmds.iconTextButton(w=300, h=50, style='iconAndTextVertical', image1=gumroad_button_icon,command=gumroad )   

        #----------------------------------------------
        cmds.button( label='Close',bgc=[0.2,0.2,0.2],  w=150, h=30, command=('cmds.deleteUI(\"' + window + '\", window=True)') )
        #----------------------------------------------        
        
        cmds.showWindow()
        cmds.showWindow('Help')
        
#_______________________________________________________________________________________________________________________________________________________________________________________________________
'''
if __name__ == "__main__":   
    try:
        probool.close() # pylintL diable=E0601
        probool.deleteLater()
    except:
        pass
    
    probool = OpenImportDialog()
    probool.show()
'''