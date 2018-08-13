import importlib
import glob
import re
import logging
logger = logging.getLogger(__name__)


def makeAIList():
    aiList = []
    # list files in dir
    path = './mancala/ai/'
    files = glob.glob(path + '*.py')
    pattern = r'.*/([^_/]+\w*)\.py'
    matches = [re.match(pattern, x) for x in files]
    groups = [m.group(1) for m in matches if m is not None]
    for f in groups:
        logger.info("loading {}".format(f))
        res = {}
        # import each
        res['module'] = importlib.import_module('ai.' + f)
        # initialize
        res['ai'] = res['module'].AI()
        res['name'] = f
        res['wins'] = 0
        aiList.append(res)
    return aiList
