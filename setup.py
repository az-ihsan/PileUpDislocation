from setuptools import setup

setup(name='pile-up discrete dislocation dynamics',
      version='0.1',
      description='A simple dislocation pile-up simulation',
      url='',
      author='Ahmad Z. Ihsan',
      author_email='',
      license='',
      packages=['pileup_ddd'],
      install_requires=[
            'matplotlib',
            'numpy',
            'attr',
            'pytest',
            'tqdm'
      ],
      include_package_data=True,
      setup_requires=["pytest-runner"],
      test_suite='nose.collector',
      tests_require=['pytest'],
      zip_safe=False)
