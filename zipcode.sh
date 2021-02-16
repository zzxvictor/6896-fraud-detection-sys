for lambda in src/*; do
  root=$(pwd)
  cd "$lambda"
  zip -r code.zip *.py
  cd "$root"
done