from cx_Freeze import setup, Executable

setup(
    name = 'analysis_wiki',
    version = '1.0',
    description = 'implementation of an introductory work LKSH-2105',
    executables = [Executable('analysis_wiki.py')]
)