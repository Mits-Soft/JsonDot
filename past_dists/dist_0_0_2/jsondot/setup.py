from setuptools import setup

setup(
    name='JsonDot',
    version='0.1',
    description='Load JSON files and use the data with dot notation then dump to the file',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mi_usuario/mi_libreria',
    author='Mi Nombre',
    author_email='mi_correo@ejemplo.com',
    license='MIT',
    packages=['jsondot'],
    classifiers=[
        'Development Status :: 3 - Alpha',        
        'License :: OSI Approved :: MIT License',   
        # 'Programming Language :: Python :: 3',      
        # 'Programming Language :: Python :: 3.6',    
        # 'Programming Language :: Python :: 3.7',    
        'Programming Language :: Python :: 3.10'
    ],
)