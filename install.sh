# First try with python
{
  pip freeze > requirements.txt && python setup.py test && pip install -e .
} ||
{ # If python fails, try with python3
  pip3 freeze > requirements.txt && python3 setup.py test && pip3 install -e .
}
{
  source ~/.bash_profile
} ||
{
  source ~/.zprofile
} ||
{
  source ~/.bashrc
}
rm -rf ./test_dir*
