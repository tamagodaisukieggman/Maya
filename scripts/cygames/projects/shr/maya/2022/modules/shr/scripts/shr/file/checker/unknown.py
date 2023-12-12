# -*- coding: utf-8 -*-

import os
import re
import codecs
import json
from datetime import datetime

import maya.cmds as cmds

# from mtku.maya.mtklog import MtkLog
from mtku.maya.utils.bat import MtkBat
from mtku.maya.utils.decoration import timer


# logger = MtkLog(__name__)


class Unknown(object):

    latest_result = u'D:/check/latest'
    log_root = u'D:/check'
    log_csv = u'{}/{}.csv'.format(log_root, datetime.now().strftime("%Y%m%d"))

    node_white_list = (
        # UE4のサンプルに入っていたもの
        'SkeletonSettings_Cache',
        # 廃止されたVector Render
        'vectorRenderGlobals',
        # 旧バージョンのTurtle
        'TurtleDefaultBakeLayer',
        'TurtleBakeLayerManager',
        'TurtleRenderOptions',
        'TurtleUIOptions',
        # mentalray
        'mentalrayGlobals',
        'mentalrayItemsList',
        'miDefaultFramebuffer',
        'miDefaultOptions',
        'surfaceSamplingMiOptionsNode',
        # 2016以降
        'trackInfoManager',
        'MayaNodeEditorSavedTabsInfo',
        'hyperShadePrimaryNodeEditorSavedTabsInfo',
        'poseInterpolatorManager',
        'shapeEditorManager',
        'hyperShadePrimaryNodeEditorSavedTabsInfo',
        'nodeGraphEditorBookmarkInfo1',
        'renderSetup',
        'COLLADA',
        # 2017のArnold
        'defaultArnoldDisplayDriver',
        'defaultArnoldDriver',
        'defaultArnoldRenderOptions',
        'defaultArnoldFilter',
        'aiStandIn',
        'aiVolume',
        'SphereLocator',
        'aiOptions',
        'aiAOV',
        'aiAOVDriver',
        'aiAOVFilter',
        'aiSkyDomeLight',
        'aiCurveCollector',
        'aiAreaLight',
        'aiLightPortal',
        'aiPhotometricLight',
        'aiMeshLight',
        'aiLightBlocker',
        'aiSky',
        'aiRaySwitch',
        'aiImage',
        'aiLightDecay',
        'aiNoise',
        'aiUtility',
        'aiMotionVector',
        'aiWireframe',
        'aiDensity',
        'aiBarndoor',
        'aiGobo',
        'aiStandard',
        'aiHair',
        'aiAmbientOcclusion',
        'aiBump2d',
        'aiBump3d',
        'aiPhysicalSky',
        'aiVolumeScattering',
        'aiFog',
        'aiUserDataString',
        'aiVolumeSampleFloat',
        'aiVolumeCollector',
        'aiUserDataInt',
        'aiWriteColor',
        'aiWriteFloat',
        'aiUserDataFloat',
        'aiComplexIor',
        'aiUserDataBool',
        'aiUserDataVector',
        'aiUserDataColor',
        'aiShadowCatcher',
        'aiUserDataPnt2',
        'aiSkin',
        'aiVolumeSampleRgb',
        'aiCurvature',
        'aiThinFilm',
        'mtoa',
    )

    # Mayaの付属プラグイン(拡張子なし)がなぜか引っかかるときがあるので除外
    plugin_white_list = (
        # UE4
        'TitanDDS',
        # Maya
        'AbcBullet',
        'AbcExport',
        'AbcImport',
        'animImportExport',
        'ArubaTessellator',
        'atomImportExport',
        'AutodeskPacketFile',
        'autoLoader',
        'bullet',
        'cgfxShader',
        'cleanPerFaceAssignment',
        'clearcoat',
        'CloudImportExport',
        'COLLADA',
        'ddsFloatReader',
        'dgProfiler',
        'DirectConnect',
        'dx11Shader',
        'fltTranslator',
        'Forge_Maya',
        'Fur',
        'gameFbxExporter',
        'GamePipeline',
        'ge2Export',
        'gpuCache',
        'hlslShader',
        'ik2Bsolver',
        'ikSpringSolver',
        'matrixNodes',
        'mayaCharacterization',
        'mayaHIK',
        'MayaMuscle',
        'melProfiler',
        'modelingToolkit',
        'modelingToolkitExt',
        'modelingToolkitStd',
        'nearestPointOnMesh',
        'objExport',
        'OneClick',
        'OpenEXRLoader',
        'openInventor',
        'P4GT-Maya-2015_x64',
        'quatNodes',
        'retargeterNodes',
        'rotateHelper',
        'rtgExport',
        'sceneAssembly',
        'shaderFXPlugin',
        'stereoCamera',
        'studioImport',
        'tiffFloatReader',
        'Turtle',
        'Unfold3D',
        'VectorRender',
        'vrml2Export',
        'Vue_xStream',
        'xNormalSBM_Maya2k15_x64',
        'MayaClothSolver',
        'ForgeInstallLoc',
        'IMFAlias',
        'IMFAVI',
        'IMFBMP',
        'IMFDDS',
        'IMFGIF',
        'IMFJPEG',
        'IMFKodakCineon',
        'IMFMaya',
        'IMFPNG',
        'IMFPostScriptEPS',
        'IMFQuantelYUV',
        'IMFSiliconGraphics',
        'IMFSoftimage',
        'IMFSonyPSX',
        'IMFTarga',
        'IMFTIFF',
        'IMFWavefrontRLA',
        'IMFxpm',
        'RadiancePicture',
        'BifrostMain',
        'bifrostshellnode',
        'bifrostvisplugin',
        'fbxmaya',
        'Substance',
        'xgenMR',
        'xgenToolkit',
        'Mayatomr',
        # Bonus Tools
        '3dsImport',
        'audioWave',
        'closestPointOnCurve',
        'corrosionTexture',
        'cvColorShader',
        'denimTexture',
        'diffractionShader',
        'drawReduceTool',
        'drawSplitTool',
        'frecklesTexture',
        'gameInputDevice',
        'hwColorPerVertexShader',
        'hwManagedTextureShader',
        'measure',
        'nodeCreatedCBCmd',
        'pointOnMeshInfo',
        'polyNurbsProjection',
        'PolyTools',
        'polyVariance',
        'randomizerDevice',
        'ringsTexture',
        'scallopTexture',
        'skinShader',
        'splatterTexture',
        'streaksTexture',
        'stringFormatNode',
        'sun',
        'treeBarkTexture',
        'udpDevice',
        'veiningTexture',
        'woodGrainTexture',
        'renderSetup.py',
        # PullDownIt3
        'pdiMaya3xFlt',
        'mtoa',
    )

    @classmethod
    def _is_white_node(cls, node):
        for white_list in cls.node_white_list:
            if re.search(white_list, node):
                return True
        return False

    @classmethod
    def get_unknown_nodes(cls):
        u"""unknownNodeの取得"""
        nodes = cmds.ls(typ='unknown')
        if not nodes:
            return []
        else:
            # unknown_nodes = [node for node in nodes if node not in cls.node_white_list]
            unknown_nodes = []
            for node in nodes:
                if not cls._is_white_node(node):
                    unknown_nodes.append(node)
            return unknown_nodes

    @classmethod
    def get_unknown_plugins(cls):
        u"""unknownPluginの取得"""
        plugins = cmds.unknownPlugin(q=True, list=True)
        if not plugins:
            return []
        else:
            unknown_plugins = [plugin for plugin in plugins if plugin not in cls.plugin_white_list]
            return unknown_plugins

    @classmethod
    def get_unknown(cls):
        u"""不明ノード、不明プラグインの取得"""
        nodes = cls.get_unknown_nodes()
        plugins = cls.get_unknown_plugins()
        if nodes or plugins:
            return {'nodes': nodes, 'plugins': plugins}
        else:
            return {}

    @classmethod
    @timer
    def main(cls, root_path):
        u"""指定したフォルダ以下を全チェック"""

        counter = 0
        open_error = []
        results = []

        for maya_file_path in MtkBat.get_maya_file_path(root_path):

            # ファイルオープン
            if not MtkBat.open_file(maya_file_path):
                open_error.append(maya_file_path)
                results.append((maya_file_path, {'openError': maya_file_path}))
                continue

            # データチェック
            # logger.info(u'チェック開始: {}\n'.format(maya_file_path))
            result = cls.get_unknown()
            if result:
                results.append((maya_file_path, result))
                # logger.error(u'{}'.format(maya_file_path))

            # logger.info(u'チェック終了: {}\n'.format(maya_file_path))
            counter += 1

        latest_summary = {
            'result': False if results else True,
            'total': counter,
            'open_error': len(open_error),
            'error': len(results),
        }

        # logger.info('')
        # logger.info(('{0:=<79}'.format('')))
        # logger.info(u'チェック総数: {}'.format(counter))
        # logger.info(u'ファイルオープンエラー数: {}'.format(len(open_error)))
        # logger.info(u'エラー数: {}'.format(len(results)))

        if results:
            if not os.path.exists(cls.log_root):
                os.makedirs(cls.log_root)
            with codecs.open(cls.log_csv, 'w', 'utf-8') as f:
                for result in results:
                    # logger.info(result)
                    f.write(u'{},{}\r\n'.format(result[0], result[1]))

        with codecs.open(cls.latest_result, 'w', 'utf8') as f:
            json.dump(latest_summary, f, indent=4)
