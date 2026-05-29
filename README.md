pip install -r requirements.txt
pytest --alluredir=allure-results
allure serve allure-results