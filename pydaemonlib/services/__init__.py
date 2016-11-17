import os

current_dir = os.path.dirname(__file__)

for file_name in os.listdir(current_dir):
    if file_name.endswith('.py') and file_name != '__init__.py':
        cls_name = file_name[:-3]
        exec 'from {0} import {0}'.format(cls_name)
