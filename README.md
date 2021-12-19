# brackend

install `docker` and `docker-compose`

run `docker-compose build`

run  `docker-compose up` in the same directory as `docker-compose.yml`, and then in another tab or process `curl localhost:8000/api/hello/`

you should get a token back, which shows you have the api up locally

make sure to do `docker-compose down` and `docker-compose build` when you're making changes

### Setting up PyCharm
- install `poetry`
- `poetry config --local virtualenvs.in-project true`
- run `poetry install`
- set PyCharm Python interpreter from `Preferences > Project > Python Interpreter` 
