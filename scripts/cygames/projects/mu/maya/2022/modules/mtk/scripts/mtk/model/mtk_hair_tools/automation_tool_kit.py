# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import xml.etree.ElementTree as ET
from xml.dom import minidom
import os
import sys
import subprocess

import maya.api.OpenMaya as om2
import maya.cmds as cmds

from pysbs import context, batchtools, substance, sbsenum

from . import AUTOMATION_TOOL_KIT
from . import RESOLUTIONS_DICT

RESOLUTIONS_DICT_REV = {v: k for k, v in RESOLUTIONS_DICT.items()}



template_path = "Z:/mtk/tools/maya/2022/modules/mtk/scripts/mtk/render/arnold_baker/sbs_tmplate/converter.sbs"
gsplit_template_path = "Z:/mtk/tools/maya/2022/modules/mtk/scripts/mtk/render/arnold_baker/sbs_tmplate/converter_gsplit.sbs"
bsplit_template_path = "Z:/mtk/tools/maya/2022/modules/mtk/scripts/mtk/render/arnold_baker/sbs_tmplate/converter_bsplit.sbs"
gray_template_path = "Z:/mtk/tools/maya/2022/modules/mtk/scripts/mtk/render/arnold_baker/sbs_tmplate/converter_gray.sbs"

irda_color_template_path = "Z:/mtk/tools/maya/2022/modules/mtk/scripts/mtk/render/arnold_baker/sbs_tmplate/HairColorCreatorExporter.sbs"


def xml_edit(sbs_path, _target, text):
    if not os.path.exists(sbs_path) or not text:
        return

    _enum = 0
    treeRef = ET.parse(sbs_path)
    root = treeRef.getroot()
    _target_flag = False

    for i, child in enumerate(root.iter()):
        for key, value in child.items():
            if value == _target:
                _target_flag = True
                _enum = i
            if _target_flag and _enum and _enum != i:
                _target_flag = False
                child.set(key, text)
                break

    treeRef.write(sbs_path)



class AutomationToolKit(object):

    aContext = context.Context()
    context.Context.setAutomationToolkitInstallPath(automationToolkitInstallPath = AUTOMATION_TOOL_KIT)

    def __init__(self, image_path, output_name, output_path, output_size):
        self.errors = []

        if output_name.endswith("root"):
            self.template_path = gsplit_template_path
        elif output_name.endswith("depth"):
            self.template_path = bsplit_template_path
        elif output_name.endswith("vcolor"):
            self.template_path = gray_template_path
        else:
            self.template_path = template_path

        self.output_name = output_name
        self.output_path =output_path
        self.base_color_image_connect = 'input@path@' + image_path + '@format@JPEG'
        self.output_size = output_size

        # self.create_sbs()
        # self.create_sbsar()
        # self.create_image()


    def create_sbs(self):
        errors = ""
        proc = batchtools.sbsmutator_edit(
            input = self.template_path,
            presets_path = self.aContext.getDefaultPackagePath(),
            output_name = self.output_name,
            output_path = self.output_path,
            # output_path = CACHE_DIR,
            connect_image = self.base_color_image_connect + '@format@RAW',
            stderr = subprocess.PIPE
            # set_value = ('$outputsize@%s,%s' % (self.output_size, self.output_size))
            )
        (out, err) = proc.communicate()
        proc.wait()
        if err:
            errors = err
            # print(err)
            sys.exit(1)
        return errors


    def create_sbsar(self):
        errors = ""
        proc = batchtools.sbscooker(
            # inputs = os.path.join(CACHE_DIR, self.output_name) + '.sbs',
            inputs = os.path.join(self.output_path, self.output_name) + '.sbs',
            includes = self.aContext.getDefaultPackagePath(),
            size_limit = 13,
            output_path = self.output_path,
            # output_path = CACHE_DIR
            )
        (out, err) = proc.communicate()
        proc.wait()

        if err:
            errors = err
            # print(err)
            sys.exit(1)
        return errors


    def create_image(self):
        errors = ""
        proc = batchtools.sbsrender_render(
            # inputs = os.path.join(self.output_path, self.output_name) + '.sbsar',
            inputs = os.path.join(self.output_path, self.output_name) + '.sbsar',
            output_name = '{inputName}',
            output_path = self.output_path,
            output_format = 'tga',
            set_value = ('$outputsize@%s,%s' % (self.output_size, self.output_size))
            )
        (out, err) = proc.communicate()
        proc.wait()
        if err:
            errors = err
            # print(err)
            sys.exit(1)
        return errors



class IrdaMapConverter(object):

    aContext = context.Context()
    context.Context.setAutomationToolkitInstallPath(automationToolkitInstallPath = AUTOMATION_TOOL_KIT)

    def __init__(self, image_path, output_name, output_path, output_size):
        self.errors = []

        self.template_path = irda_color_template_path

        self.output_name = output_name
        self.output_path =output_path
        self.base_color_image_connect = 'input@path@' + image_path + '@format@JPEG'
        self.output_size = output_size

        # self.create_sbs()
        # self.create_sbsar()
        # self.create_image()


    def create_sbs(self):
        errors = ""
        proc = batchtools.sbsmutator_edit(
            input = self.template_path,
            presets_path = self.aContext.getDefaultPackagePath(),
            output_name = self.output_name,
            output_path = self.output_path,
            # output_path = CACHE_DIR,
            connect_image = self.base_color_image_connect + '@format@RAW',
            stderr = subprocess.PIPE,
            # set_value = ('$outputsize@%s,%s' % (self.output_size, self.output_size))
            )
        (out, err) = proc.communicate()
        proc.wait()
        # self.modify_sbs()
        if err:
            errors = err
            # print(err)
            sys.exit(1)
        return errors

    def modify_sbs(self):
        output_name = self.output_name
        output_path = self.output_path
        sbs_path = "{}/{}.sbs".format(output_path, output_name)

        out_size = "sbsenum.OutputSizeEnum.SIZE_{}".format(RESOLUTIONS_DICT_REV[self.output_size])

        ctx = context.Context()
        sbs_doc = substance.SBSDocument(ctx, sbs_path)
        sbs_doc.parseDoc()

        graph = sbs_doc.getSBSGraphList()[0]

        graph.setBaseParameterValue(
            aParameter=sbsenum.CompNodeParamEnum.OUTPUT_SIZE,
            aParamValue=[eval(out_size), eval(out_size)],
            aRelativeTo=sbsenum.ParamInheritanceEnum.ABSOLUTE
        )

        # graph.setBaseParameterValue(
        #     aParameter=sbsenum.CompNodeParamEnum.OUTPUT_SIZE,
        #     aParamValue=[sbsenum.OutputSizeEnum.SIZE_4096,
        #                 sbsenum.OutputSizeEnum.SIZE_4096],
        #     aRelativeTo=sbsenum.ParamInheritanceEnum.ABSOLUTE
        # )

        # Save pkg.
        sbs_doc.writeDoc()
        return

        output_name = self.output_name
        output_path = self.output_path

        _command = 'sbsmutator edit '
        _command += '--input {}/{}.sbs '.format(output_path, output_name)
        _command += '--connect-image "input1"@path@"/an/image/to/connect/bar.png"'
        _command += ' --output-path {inputPath'


    def create_sbsar(self):
        errors = ""
        proc = batchtools.sbscooker(
            # inputs = os.path.join(CACHE_DIR, self.output_name) + '.sbs',
            inputs = os.path.join(self.output_path, self.output_name) + '.sbs',
            includes = self.aContext.getDefaultPackagePath(),
            size_limit = 13,
            output_path = self.output_path,
            # output_path = CACHE_DIR
            )
        (out, err) = proc.communicate()
        proc.wait()

        if err:
            errors = err
            # print(err)
            sys.exit(1)
        return errors

    def create_image(self):
        errors = ""
        proc = batchtools.sbsrender_render(
            # inputs = os.path.join(CACHE_DIR, self.output_name) + '.sbsar',
            inputs = os.path.join(self.output_path, self.output_name) + '.sbsar',
            output_name = '{inputName}',
            output_path = self.output_path,
            output_format = 'psd',
            set_value = ('$outputsize@%s,%s' % (self.output_size, self.output_size))
            )
        (out, err) = proc.communicate()
        proc.wait()
        if err:
            errors = err
            # print(err)
            sys.exit(1)
        return errors





"""
sbs_path = r"Z:\mtk\work\noshipping\characters\wolf_furtest\texture\test\tex_cre22_000_hair_irda.sbs"

_target = "export/fromGraph/destination"
_path = r"Z:\mtk\work\noshipping\characters\wolf_furtest\texture\test"

_target = "export/fromGraph/pattern"
_path = "$(graph)_$(identifier)"

_pattern_flag = False

_target_flag = False
_enum = 0

treeRef = ET.parse(sbs_path)
root = treeRef.getroot()
sbsString = ET.tostring(root, encoding="utf-8", method="xml")
#strRef  = ET.tostring(root)
reparsed = minidom.parseString(sbsString)
sbsString = reparsed.toprettyxml(indent=' ').encode('utf-8')
print sbsString
#for x in dir(root.attrib):
#    print x
for i, _tree in enumerate(root.iter()):
    #print _tree
    #if _tree.tag == "name" and _target in _tree.attrib.values():
    #    print _tree.tag, _tree.attrib, "==="
    for _i,(key, value) in enumerate(_tree.items()):
        if value == _target:
            _target_flag = True
            _enum = i
        if _target_flag and _enum != i:
            _target_flag = False
            print key, value, i, _i
            print _tree.set(key, _path)
#treeRef.write(sbs_path)
"""


