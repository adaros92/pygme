{
  python setup.py sdist bdist_wheel
} ||
{
  python3 setup.py sdist bdist_wheel
}
twine upload dist/*
rm -rf ./test_dir* .pytest_cache *.egg*