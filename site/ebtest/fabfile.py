import os

#UNCOMMENT for Beanstalk
from fabric.api import task, local
#from boulanger.fabfile import release_notes
os.environ['PROJECT_NAME'] = os.getcwd().split('/')[-1]  # Import before aws_tasks, as it is used there.
os.environ['DEFAULT_REGION'] = 'us-east-1'
os.environ['DB_HOST'] = 'PROJECT-RDS-DB-URL'  # RDS DB URL, update accordingly']
from aws_tasks import tasks as aws


from boulanger.fabfile import *

# Define Server Topology
env.server_nodes = {
    'web': {
        #'web1': ('<public server address>', '<private ip>'),
    },
    'db': {
        #'db1': ('<public server address>', '<private ip>'),
    },
}

# Auto Generated, Do Not Modify
env.project_name = os.getcwd().split('/')[-1]
env.user = env.project_name + 'team'
env.roledefs = {
    'web': [public_address for public_address, private_address in env.server_nodes['web'].values()],
    'db': [public_address for public_address, private_address in env.server_nodes['db'].values()],
}
