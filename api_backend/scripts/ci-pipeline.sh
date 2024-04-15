red=`tput setaf 1`
green=`tput setaf 2`
bold=$(tput bold)
reset=`tput sgr0`
source configs/secretTest.sh
source configs/secretIpfsTest.sh
# source scripts/create-role.sh

python app/db/drop_db.py
python app/db/create_db.py
python app/db/setup_test.py

echo "-------------------------------------------------------------"
echo "${bold}Static Analysis${reset}"
echo
echo ">> MyPy:" 
mypy --namespace-packages app/
echo
echo ">> flake8:"
if [[ $(flake8 --max-line-length=120 --per-file-ignores="__init__.py:F401" app/) ]]; then
    echo "${red}${bold}Failed!!${reset}"
    flake8 --max-line-length=120 --per-file-ignores="__init__.py:F401" app/
else
    echo "${green}${bold}Success: no issues found${reset}"
fi
echo
echo "-------------------------------------------------------------"
echo "${bold}Unit Tests${reset}"
echo
echo ">> pytest:"
pytest --cov=app tests/
source configs/secret.sh
