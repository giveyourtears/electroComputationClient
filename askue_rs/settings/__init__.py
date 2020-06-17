import os

if os.environ.get('DEV_PG_HOST') is None:
    from askue_rs.settings.prod import *
else:
    from askue_rs.settings.dev import *
