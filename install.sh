# First try with python
{
  pip freeze > requirements.txt && tox && pip install -e .
} ||
{ # If python fails, try with python3
  pip3 freeze > requirements.txt && tox && pip3 install -e .
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
bash <(curl -s https://codecov.io/bash)
rm -rf ./test_dir*
