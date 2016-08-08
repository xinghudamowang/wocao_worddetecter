from distutils.core import setup  
setup(name='wocao',
      version='0.0.1.beta',  
      keywords=('word', 'detection', 'keyword', 'summerize'),
      description='Chinese Words detection Utilities',
      license = 'MIT License',
      author='Wiekian,',  
      author_email=' wiekian@live.com',  
      url=' ',  
      packages=['wocao'],  
      package_dir={'wocao':'wocao'},
      package_data={'wocao':['*.*','wocao/*']}
)
