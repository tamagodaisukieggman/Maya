import os, dotenv, re
import traceback
envs = dotenv.dotenv_values(os.path.join(os.path.dirname(__file__), '.env'))
for envname in envs.keys():
    if envname == 'WORKMAN_PACKAGE_VERSIONS':
        if 'WORKMAN_PACKAGE_VERSIONS' in os.environ.keys():
            try:
                already_exists = [x for x in os.environ['WORKMAN_PACKAGE_VERSIONS'].split(';') if x.startswith(envs[envname].split('=')[0]+'=')]
            except:
                print(traceback.format_exc())
                print('ERROR: Failed in getting a package version in', __file__)

            if len(already_exists) == 0:
                os.environ[envname] += ';' + envs[envname]
        else:
            os.environ[envname] = envs[envname]
    else:
        # Override
        os.environ[envname] = envs[envname]


