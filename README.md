Þarf:
* Python 3.4 eða 3.5 (fleiri?)
* python-pip
* python-dev
* python3-venv

Sækjum kóðann, förum inn í vinnuskráarsafnið (eldar), setjum upp sýndarumhverfi og setjum upp hugbúnaðinn sem til þarf.
```bash
git clone https://github.com/ZmjbS/eldar.git
cd eldar
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
Þegar nauðsynlegur hugbúnaður er kominn upp setjum við upp sjálfan kóðann:
```bash
./manage.py migrate
./manage.py loaddata fixtures/timabil_starfsstodvar_og_tegundir.xml
./manage.py loaddata fixtures/vaktir.xml
```
... og þá áttu að vera komin(n) með kerfið. Keyrir þróunarvefþjóninn með:
```bash
./manage.py runserver
```
