from setuptools import setup

setup(
    name='spam_llm',
    version='0.1',
    description='Framework to use HuggingFace-style models to create a spam detector on a set of Thunderbird mbox files.',
    author='Jon Downs',
    author_email='jon@jondowns.net',
    packages=['spam_llm'],
    install_requires=['wheel']
)
