# -*- coding: utf-8 -*-

from cylibassetdbutils import assetdbutils
from maya import cmds
import os

db = assetdbutils.DB.get_instance()

class Task:
    def execute(self, outfilename, threshold=0.001, ids=None):
        #outfilename = 'C:/Users/S05231/Documents/invalid_cog_jnt_list.csv'
        q = 'select * from sharedasset_version_master_02 where task="animation" and assetgroup="character" ' + \
            ' and subcategory="ply" and variant="default" and assetname="male00" and subgroup="all" ' + \
            ' and path not like "%~" and (omit is NULL or omit = 0)'

        db.cs.execute(q)
        buf = db.cs.fetchall()
        print('num: ', len(buf))

        latests = {}

        for item in buf:
            if ids is not None:
                for _id in ids: 
                    if item['asset_id'] in ids:
                        break
                else:
                    continue
                
            path = item['path']
            dotindex = path.rindex('.')
            ts = path[:dotindex]
            fmt = path[dotindex+1:]
            ver = item['version']
            #print path, ver
            base = ts[:-4] + '__' + fmt
            #print 'base: ', base
            if base in latests:
                filename, latest_ver, _ = latests[base]
                if ver <= latest_ver:
                    #print 'old version: ', path
                    continue
                    
            latests[base] = (path, ver, item)
            #print 'new version: ', path

        print('unique item num: ', len(list(latests.keys())))

        from cylibassetdbutils import assetutils, assetvar
        with open(outfilename, 'w') as hd:
            line = 'Threshold, %f\nStatus, Detail, Filename, AssetURL, Flags, Create Date\n' % (threshold)
            hd.write(line)

            for i, base in enumerate(latests.keys()):
                filename, ver, item = latests[base]
                asset = assetvar.ShareAsset()
                for k in asset.get_dict():
                    setattr(asset, k, item[k])
                tags = db.get_assigned_tags(asset)
                buf = [x['name'] for x in tags if x['name']=='omit' or x['name']=='pending' or x['name']=='sample']
                print('%d/%d filename: ' % (i, len(list(latests.keys()))), filename)

                flag = ''
                if len(buf) > 0:
                    print('--> not target.')
                    print(' tags: ', [x['name'] for x in tags])
                    buf = list(set(buf))
                    buf = sorted(buf)
                    flag = ', '.join(buf)
                    print('flag: ', flag)
                
                if not os.path.exists(filename):
                    continue

                cmds.file(filename, o=True, f=True)
                healthy, node_exists, has_keys = is_healthy(threshold=threshold)

                if healthy:
                    print('--> OK')
                else:
                    print('--> NG')

                url = asset.get_url(filename)
                url = url[url.index('<'):url.index('>')+1]
                print('url: ', url)

                status = 'cog_jnt not found' if not node_exists else 'Has keys' if has_keys else u'No keys'
                line = u'%s, %s, %s, %s, %s, %s\n' % ('OK' if healthy else 'NG', status, filename, url, flag, item['create_date'])
                hd.write(line)

def is_healthy(threshold):
    def is_all_zero(buf, threshold):
        for v in buf:
            if abs(v) >= 0.001:
                print('Non-zero exists: ', buf)
                return False

        print('value all zero: ', buf)
        return True

    node_exists = False
    has_keys = False
    healthy = None

    node = 'cog_jnt'
    if not cmds.objExists(node):
        print('%s not exists.' % node)
        healthy = True
    else:
        node_exists = True
        values = cmds.keyframe(node, q=True, at=('r'), vc=True, t=())
        if values is None:
            print('%s doesnt have keys.' % node)
            values = cmds.getAttr(node+'.r')[0]
        else:
            has_keys = True
        
        healthy = True if is_all_zero(values, threshold) else False

    return healthy, node_exists, has_keys
    
