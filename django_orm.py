# setup sys.path first if needed
import sys
sys.path.insert(0, path_to_django_project)

# tell django which settings module to use
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_project.settings'
