import os

PROJECT_NAME = 'my-rag-app'

STRUCTURE = {
    'app' : {
        '__init__.py':None,
        'main.py':None,
        'api':{
            '__init__.py':None,
            'routes.py' : None,
        },
         
        'core': {
            '__init__.py' : None,
            'config.py': None,
            'security.py': None

        },
        'servicrs': {
            '__init__.py': None,
            'rag_service.py':None,
            'cache_service.py':None,
            'Mongo_service.py':None,

        },
        'utils':{
            'ingest_data.py':None,
            'rebuild_index.py':None,

        },
    },

    'scripts':{
        'ingest_data.py': None,
        'rebuild_index.py':None,
    },
    
        'test' : {
            'test_rag.py': None
        },
    },


def create_structure(base_path, structure):
    for name ,content in structure.items():
        path = os.path.join(base_path,name)

        if content is None:
            if not os.path.exists(path):
                open(path, 'w').close()
                print('created')
            else:
                print('already exists')
        else:
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)
                print('Crreated directory')
            else:
                print('Directory already exists')

            create_structure(path, content)

def main():
    if not os.path.exists(PROJECT_NAME):
        os.makedirs(PROJECT_NAME,exist_ok=True)
        print('Created project root')
    else:
        print('Project root already exists')
    create_structure(PROJECT_NAME,STRUCTURE)
    print('Setup complete')

if __name__ == '__main__':
    main()
    