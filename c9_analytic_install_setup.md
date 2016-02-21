how to install scikitlearn on cloud 9

problem
numpy.distutils.system_info.NotFoundError: no lapack/blas resources found


use virtualenv

Install linear algebra libraries from repository (dependencies for numpy)
sudo apt-get install gfortran libopenblas-dev liblapack-dev

pip install numpy
pip install -U scipy
pip install -U scikit-learn

test install
>>>import sklearn
shouln't throw an error

<!--(maybe need to edit path?-->
<!--export PYTHONPATH=$HOME/opt/lib/python2.7/site-packages)-->
<!--virtualenv VIRTUALENV_DIR --system-site-packages-->