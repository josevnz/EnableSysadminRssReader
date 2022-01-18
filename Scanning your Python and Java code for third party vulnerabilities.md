# Scanning your Python and Java code for third party vulnerabilities

On this short tutorial I want to show you how you can make your Python applications more secure by correlating modules installed with PIP and CVE security advisories.

Say that you keep your third party dependencies well stated in your [requirements.txt](https://www.jetbrains.com/help/pycharm/managing-dependencies.html#create-requirements) file:

```
module1==x.y.z
module2==x.y.z
module1==x.y.z
```

This is correct as you want to make sure development environment is reproducible. But that also leaves you exposed to keep old versions which eventually become vulnerable to exploits.

Think about your versions as a garden: They need watering, trimming and attention. A good project keeps versions up to date when a vulnerability is found, and tools like [pip-audit](https://github.com/trailofbits/pip-audit) make this job easier.

# What you will learn on this article
* How to scan your Python projects and check if your third party libraries have a known vulnerability, using the CVE identifiers.


## Installation

Use PIP to get the latest version installed

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

![EnableSysadminRssReader](https://raw.githubusercontent.com/josevnz/EnableSysadminRssReader/main/rssenablesysadminreader.png)

Let's now analyze a project, [EnableSysadminRSSReader](https://github.com/josevnz/EnableSysadminRssReader), that uses a package where a recent vulnerability has been found (the project is secure, but will downgrade one of the libraries on purpose):

Install it first as [explained here](https://github.com/josevnz/EnableSysadminRssReader/blob/main/README.md).:

```shell=
(pip-audit) [josevnz@dmaf5 ~] git clone git@github.com:josevnz/EnableSysadminRssReader.git
(pip-audit) [josevnz@dmaf5 ~] cd EnableSysadminRssReader
(pip-audit) [josevnz@dmaf5 ~] sed -i 's#4.7.1#4.6.0#' requirements.txt
```

I downgraded the version of lxml from 4.7.1 to 4.6.0. Let's see what happens when we scan it:

```shell=
(pip-audit) [josevnz@dmaf5 ~]$ pip-audit  --requirement requirements.txt 
Found 3 known vulnerabilities in 1 packages        
Name Version ID             Fix Versions
---- ------- -------------- ------------
lxml 4.6.0   PYSEC-2021-19  4.6.3
lxml 4.6.0   PYSEC-2020-62  4.6.2
lxml 4.6.0   PYSEC-2021-852 4.6.5
```

[lxml is a good library](https://www.python101.pythonlibrary.org/chapter31_lxml.html) to parse XML files with ease. Software is complex and this particular library had a bug that could be exploited; If you go to the NIST database and search for lxml you will see more details on the advisory [CVE-2021-43818](https://nvd.nist.gov/vuln/detail/CVE-2021-43818). Let's take a look at our requirements.txt file:

```txt
requests==2.27.1
rich==11.0.0
lxml==4.6.0
```

So *the easiest fix* is to **upgrade to the recommended version of lxml** (4.6.5) as is a minor upgrade that contains the bug-fix and guarantees the API changes will be minimal. After checking the lastest version at the time of this writting (4.7.1) I decided to go with a higher version:

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

# So other languages are safe, right?

Sadly, vulnerabilities in third party libraries are not an exclusive threat of Python. To illustrate the problem, I will download a vulnerable version of the well known Open Source applicaion server

```shell=
[josevnz@dmaf5 EnableSysadmin]$ curl --location --fail --output ~/Downloads/XXXX-A.B.C-zzzz.zip https://XXX.ZZZZ.org/dist/XXX/server/A.B.C/XXXX-A.B.C-zzzz.zip
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 88.8M  100 88.8M    0     0  5142k      0  0:00:17  0:00:17 --:--:-- 1194k

cd ~/Downloads
unzip XXXX-A.B.C-zzzz.zip
```

OWASP wrote a really nice dependency analyzer you can [use](https://owasp.org/www-project-dependency-check/). 

```shell
[josevnz@dmaf5 Downloads]$ curl --fail --output ~/Downloads/dependency-check-6.5.3-release.zip --location https://github.com/jeremylong/DependencyCheck/releases/download/v6.5.3/dependency-check-6.5.3-release.zip
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   669  100   669    0     0   4430      0 --:--:-- --:--:-- --:--:--  4430
100 23.0M  100 23.0M    0     0  7653k      0  0:00:03  0:00:03 --:--:-- 8899k
```

Let's use it to scan vulnerabilities for this application:

```shell
[josevnz@dmaf5 Downloads]$ ~/Downloads/dependency-check/bin/dependency-check.sh --prettyPrint --format HTML -scan /home/josevnz/Downloads/XXXX-A.B.C-zzzz/lib/
[INFO] Checking for updates
[INFO] Download Started for NVD CVE - Modified
[INFO] Download Complete for NVD CVE - Modified  (278 ms)
[INFO] Processing Started for NVD CVE - Modified
WARNING: An illegal reflective access operation has occurred
WARNING: Illegal reflective access by com.fasterxml.jackson.module.afterburner.util.MyClassLoader (file:/home/josevnz/Downloads/dependency-check/lib/jackson-module-afterburner-2.13.1.jar) to method java.lang.ClassLoader.findLoadedClass(java.lang.String)
WARNING: Please consider reporting this to the maintainers of com.fasterxml.jackson.module.afterburner.util.MyClassLoader
WARNING: Use --illegal-access=warn to enable warnings of further illegal reflective access operations
WARNING: All illegal access operations will be denied in a future release
[INFO] Processing Complete for NVD CVE - Modified  (5150 ms)
[INFO] Begin database maintenance
[INFO] Updated the CPE ecosystem on 116793 NVD records
[INFO] Cleaned up 2 orphaned NVD records
[INFO] End database maintenance (24739 ms)
[INFO] Begin database defrag
[INFO] End database defrag (4660 ms)
[INFO] Check for updates complete (39967 ms)
[INFO] 

Dependency-Check is an open source tool performing a best effort analysis of 3rd party dependencies; false positives and false negatives may exist in the analysis performed by the tool. Use of the tool and the reporting provided constitutes acceptance for use in an AS IS condition, and there are NO warranties, implied or otherwise, with regard to the analysis or its use. Any use of the tool and the reporting provided is at the user’s risk. In no event shall the copyright holder or OWASP be held liable for any damages whatsoever arising out of or in connection with the use of this tool, the analysis performed, or the resulting report.


   About ODC: https://jeremylong.github.io/DependencyCheck/general/internals.html
   False Positives: https://jeremylong.github.io/DependencyCheck/general/suppression.html

💖 Sponsor: https://github.com/sponsors/jeremylong


[INFO] Analysis Started
[INFO] Finished Archive Analyzer (1 seconds)
[INFO] Finished File Name Analyzer (0 seconds)
[INFO] Finished Jar Analyzer (1 seconds)
[INFO] Finished Central Analyzer (9 seconds)
[ERROR] ----------------------------------------------------
[ERROR] .NET Assembly Analyzer could not be initialized and at least one 'exe' or 'dll' was scanned. The 'dotnet' executable could not be found on the path; either disable the Assembly Analyzer or add the path to dotnet core in the configuration.
[ERROR] ----------------------------------------------------
[INFO] Finished Dependency Merging Analyzer (0 seconds)
[INFO] Finished Version Filter Analyzer (0 seconds)
[INFO] Finished Hint Analyzer (0 seconds)
[INFO] Created CPE Index (2 seconds)
[INFO] Finished CPE Analyzer (6 seconds)
[INFO] Finished False Positive Analyzer (0 seconds)
[INFO] Finished NVD CVE Analyzer (0 seconds)
[INFO] Finished Sonatype OSS Index Analyzer (3 seconds)
[INFO] Finished Vulnerability Suppression Analyzer (0 seconds)
[INFO] Finished Dependency Bundling Analyzer (0 seconds)
[INFO] Analysis Complete (23 seconds)
[INFO] Writing report to: /home/josevnz/Downloads/./dependency-check-report.html
```

![Scan results for XXXX](https://github.com/josevnz/EnableSysadminRssReader/raw/main/owasp_scan.png)

The report shows than it has lots of issues (the Open Source vendor fixed all of them on the next release). But I think you will appreciate now why it is important to keep tabs on your software and their dependencies!

Not everything is perfect, and the tool [could generate false positives](https://jeremylong.github.io/DependencyCheck/general/suppression.html);  even with that the value of this tool is great, as it can be added to your continuous integration pipelines.

# What did we learn?

This was quick and intense, so let's summarize a few things we learned:

* You can scan your python projects, for third party library [vulnerabilities](https://www.nist.gov/) using [pip-audit](https://github.com/trailofbits/pip-audit)
* Same applies to Java. There are specialized tools out there or generic ones like [OWASP Dependency-CLI](https://jeremylong.github.io/DependencyCheck/dependency-check-cli/index.html)
* As a plus, you can see how you can [quickly wrap your Python code](https://github.com/josevnz/EnableSysadminRssReader) using the new setuptools packaging rules (setup.cfg as opposed to setup.py)