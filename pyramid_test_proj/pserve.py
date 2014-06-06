# copy of pserve for simpler integration tests
# could be a problem when changing pyramid versions
__requires__ = 'pyramid==1.5.1'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('pyramid==1.5.1', 'console_scripts', 'pserve')()
    )

