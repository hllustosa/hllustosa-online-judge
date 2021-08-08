# The Online Judge

The Online Judge is a python/django app that allows teachers to create an environment
where teachers can set up programming problems and students can try to solve them by submitting
their code.

### Set up

This project uses PDM. It requires python version 3.7 or higher.

Like Pip, PDM provides an installation script that will install PDM into an isolated environment.

**For Linux/Mac**

```
curl -sSL https://raw.githubusercontent.com/pdm-project/pdm/main/install-pdm.py | python -
```

**For Windows**

```
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/pdm-project/pdm/main/install-pdm.py -UseBasicParsing).Content | python - 
```

Once pdm is installed, you should install the dependencies

```
pdm install
```
Now you should enable PEP 852, so the python interpreter will be able to look for installed packages

**For Linux/Mac**

```bash
pdm --pep582 >> ~/.bash_profile
```

**For Windows**

```powershell
pdm --pep582
```

##
Install seccomp
```
apt install python3-seccomp
pip3 install pyseccomp    
```