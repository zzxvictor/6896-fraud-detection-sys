for lambda in src/*; do
  root=$(pwd)
  cd "$lambda"

  if [ $lambda = "src/constants" ]
  then
    echo "compressing constant layer"
    zip -r constant-layer.zip *
  elif [ $lambda = "src/layers" ]
  then
    echo "skip src/layer folder"
  else
    echo "compressing lambda code"
    zip -r code.zip *.py
  fi
  cd "$root"

done