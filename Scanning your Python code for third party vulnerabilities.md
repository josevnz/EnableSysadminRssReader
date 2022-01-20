# Scanning your Python code for third party vulnerabilities

On this short tutorial I want to show you how you can make your Python applications more secure by correlating modules installed with PIP and CVE security advisories.

Say that you keep your third party dependencies well stated in your [requirements.txt](https://www.jetbrains.com/help/pycharm/managing-dependencies.html#create-requirements) file:

```
module1==x.y.z
module2==x.y.z
module1==x.y.z
```

This is correct as you want to make sure development environment is reproducible. But that also leaves you exposed to use old versions which eventually become vulnerable to exploits.

Think about your versions as a garden: They need watering, trimming and attention. A good project keeps versions up to date when a vulnerability is found, and tools like [pip-audit](https://github.com/trailofbits/pip-audit) make this job easier.

# What you will learn on this article
* How to scan your Python projects and check if your third party libraries have a known vulnerability, using the CVE identifiers and pip-audit.

## Installation

Use PIP to get the latest version of pip-audit installed

```shell=
python3 -m venv ~/virtualenv/pip-audit
[josevnz@dmaf5 ~]$ . ~/virtualenv/pip-audit/bin/activate
(pip-audit) [josevnz@dmaf5 ~]$
(pip-audit) [josevnz@dmaf5 ~]$ pip install --upgrade pip pip-audit
```

## Analyzing projects

### Detour: What if your project doesn't have a requirements.txt file
_Note_: pip-audit expects a requirements.txt project to be available. If your project doesn't have one (for example, uses a single setup.py), you can generate one yourself like this:

```shell=
. ~/virtualenv/myprojectvirtualenv/bin/activate
# Install your project as usual, like python setup.py develop
pip freeze > requirements.txt
```

And you should be good to go.

### First example: A project with no vulnerabilities

We will analyze [Vision2](https://github.com/CoolerVoid/Vision2), a nice script that correlates the output of an NMap scan XML file with the [CVE NIST](https://nvd.nist.gov/vuln) vulenrability database:

```shell=
(pip-audit) [josevnz@dmaf5 ~]$ git clone https://github.com/CoolerVoid/Vision2.git
Cloning into 'Vision2'...
remote: Enumerating objects: 107, done.
remote: Counting objects: 100% (53/53), done.
remote: Compressing objects: 100% (42/42), done.
remote: Total 107 (delta 27), reused 23 (delta 9), pack-reused 54
Receiving objects: 100% (107/107), 30.92 KiB | 2.21 MiB/s, done.
Resolving deltas: 100% (52/52), done.
(pip-audit) [josevnz@dmaf5 ~]$ pip-audit  --requirement Vision2/re
requirements.txt  result_nmap.xml   
(pip-audit) [josevnz@dmaf5 ~]$ pip-audit  --requirement Vision2/requirements.txt 
\ Installing package in isolated environment                                  Processing /tmp/tmpyqd6k_6g/termcolor-1.1.0.tar.gz
  Preparing metadata (setup.py) ... done
Building wheels for collected packages: termcolor
  Building wheel for termcolor (setup.py) ... done
  Created wheel for termcolor: filename=termcolor-1.1.0-py3-none-any.whl size=4830 sha256=651435a861c5185b1cfb66655fb1da82488f5fa8b97d7ed859576d61af89f616
  Stored in directory: /home/josevnz/.cache/pip/wheels/74/35/a1/85d77e2de196f09e73917aa5b91c278b29efc72d4a800b2ae7
Successfully built termcolor
Installing collected packages: termcolor
Successfully installed termcolor-1.1.0
No known vulnerabilities found                                                
```

Good, the project is not using any vulnerable libraries.


### Second example: An RSS reader with a vulnerability

Let's now analyze a project, [EnableSysadminRSSReader](https://github.com/josevnz/EnableSysadminRssReader), that uses a package where a recent vulnerability has been found (the project is secure, but will downgrade one of the libraries on purpose):

![EnableSysadminRssReader](https://raw.githubusercontent.com/josevnz/EnableSysadminRssReader/main/rssenablesysadminreader.png)

Install it first as [explained here](https://github.com/josevnz/EnableSysadminRssReader/blob/main/README.md).:

```shell=
(pip-audit) [josevnz@dmaf5 ~] git clone git@github.com:josevnz/EnableSysadminRssReader.git
(pip-audit) [josevnz@dmaf5 ~] cd EnableSysadminRssReader
(pip-audit) [josevnz@dmaf5 ~] sed -i 's#4.7.1#4.6.0#' requirements.txt
```

I downgraded the version of lxml from 4.7.1 to 4.6.0 (note the sed -i command). Let's see what happens when we scan it:

```shell=
(pip-audit) [josevnz@dmaf5 ~]$ pip-audit  --requirement requirements.txt 
Found 3 known vulnerabilities in 1 packages        
Name Version ID             Fix Versions
---- ------- -------------- ------------
lxml 4.6.0   PYSEC-2021-19  4.6.3
lxml 4.6.0   PYSEC-2020-62  4.6.2
lxml 4.6.0   PYSEC-2021-852 4.6.5
```

So there are warnings for lxml 4.6.0.

[lxml is a good library](https://www.python101.pythonlibrary.org/chapter31_lxml.html) to parse XML files with ease. Software is complex and this particular library had a bug that could be exploited; If you go to the NIST database and search for lxml you will see more details on the advisory [CVE-2021-43818](https://nvd.nist.gov/vuln/detail/CVE-2021-43818). Let's take a look at our requirements.txt file:

```txt
requests==2.27.1
rich==11.0.0
lxml==4.6.0
```

So *the easiest fix* is to **upgrade to the recommended version of lxml** (4.6.5) as is a minor upgrade that contains the bug-fix and guarantees the API changes will be minimal. After checking the lastest version at the time of this writting (4.7.1) I decided to go with a higher version, as my code doesn't need further modifications:

```txt
requests==2.27.1
rich==11.0.0
# lxml==4.6.0 <- Vulnerable to CVE-2021-43818
lxml==4.7.1
```

If we scan the project again we get this:

```shell=
(pip-audit) [josevnz@dmaf5 ~]$ pip-audit  --requirement /home/josevnz/EnableSysadmin/EnableSysadminRssReader/requirements.txt 
No known vulnerabilities found
```

My favorite quote from [Poltergeist](https://www.imdb.com/title/tt0084516/?ref_=ttqt_qt_tt) movie, after fixing this:

> Tangina: [This house is clean.](https://www.imdb.com/title/tt0084516/quotes/qt0304381)

# What did we learn?

Let's summarize a few things we learned:

* You can scan your python projects, for third party library [vulnerabilities](https://www.nist.gov/) using [pip-audit](https://github.com/trailofbits/pip-audit)
* As a plus, you can see how you can [quickly wrap your Python code](https://github.com/josevnz/EnableSysadminRssReader) using the new setuptools packaging rules (setup.cfg as opposed to setup.py)

One more thing: Third party vulnerabilities is issue is not exclusive from Python; other languages like Java suffer from the same issue, in a follow-up article I will show you what you can do to check your code. 