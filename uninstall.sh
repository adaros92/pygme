# First try with python
{
  pip uninstall pygme
} ||
{ # If python fails, try with python3
  pip3 uninstall pygme
}
rm -rf ./.eggs ./build ./dist ./.pytest_cache ./.coverage ./test_dir* feature_data_* features *.egg* .tox
