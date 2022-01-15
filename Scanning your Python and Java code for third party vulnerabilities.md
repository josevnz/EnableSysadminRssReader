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

Sadly, vulnerabilities in third party libraries are not an exclusive threat of Python. For example, the very useful Java logging library [log4J](https://blogs.apache.org/foundation/entry/apache-log4j-cves) made the rounds recently.

To illustrate the problem, I will download a vulnerable version of the excellent reverse engineering tool [Ghidra](https://github.com/NationalSecurityAgency/ghidra) (10.0.4):

```shell=
[josevnz@dmaf5 ~]$ curl --output ~/Downloads/hidra_10.0.4_PUBLIC_20210928.zip --location --fail https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_10.0.4_build/ghidra_10.0.4_PUBLIC_20210928.zip
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   672  100   672    0     0   8727      0 --:--:-- --:--:-- --:--:--  8842
100  359M  100  359M    0     0  11.0M      0  0:00:32  0:00:32 --:--:-- 11.1M
cd ~/Downloads
unzip hidra_10.0.4_PUBLIC_20210928.zip
```

We can then use a specific scanner for this threat, like [local-log4j-vuln-scanner](https://github.com/hillu/local-log4j-vuln-scanner) to check for this vulnerability:

```shell
[josevnz@dmaf5 Downloads]$ curl --fail --location --output ~/Downloads/local-log4j-vuln-scanner https://github.com/hillu/local-log4j-vuln-scanner/releases/download/v0.13/local-log4j-vuln-scanner
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   663    0   663    0     0   4118      0 --:--:-- --:--:-- --:--:--  4143
100 2578k  100 2578k    0     0  4730k      0 --:--:-- --:--:-- --:--:-- 4730k
[josevnz@dmaf5 Downloads]$ chmod u+x ~/Downloads/local-log4j-vuln-scanner

[josevnz@dmaf5 Downloads]$ ~/Downloads/local-log4j-vuln-scanner --quiet ~/Downloads/ghidra_10.0.4_PUBLIC/
Checking for vulnerabilities: CVE-2019-17571, CVE-2021-44228, CVE-2021-45105
indicator for vulnerable component found in /home/josevnz/Downloads/ghidra_10.0.4_PUBLIC/Ghidra/Framework/Generic/lib/log4j-core-2.12.1.jar (org/apache/logging/log4j/core/lookup/JndiLookup.class): JndiLookup.class 2.12.0-2.12.1 CVE-2021-44228, CVE-2021-45105
indicator for vulnerable component found in /home/josevnz/Downloads/ghidra_10.0.4_PUBLIC/Ghidra/Framework/Generic/lib/log4j-core-2.12.1.jar (org/apache/logging/log4j/core/net/JndiManager.class): JndiManager.class log4j 2.12.0-2.12.1 CVE-2021-44228, CVE-2021-45105
```

In this case you can see the tool found the following vulnerabilities: *CVE-2021-44228, CVE-2021-45105*

The latest version of Ghidra (Ghidra 10.1.1) fixed this issue, let's download and show that here:

```shell
[josevnz@dmaf5 Downloads]$ curl --location --fail --output ~/Downloads/ghidra_10.1.1_PUBLIC_20211221.zip https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_10.1.1_build/ghidra_10.1.1_PUBLIC_20211221.zip
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   672  100   672    0     0   8615      0 --:--:-- --:--:-- --:--:--  8615
100  332M  100  332M    0     0  10.6M      0  0:00:31  0:00:31 --:--:-- 10.8M

[josevnz@dmaf5 Downloads]$ curl --location --fail --output ~/Downloads/ghidra_10.1.1_PUBLIC_20211221.zip https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_10.1.1_build/ghidra_10.1.1_PUBLIC_20211221.zip
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   672  100   672    0     0   8615      0 --:--:-- --:--:-- --:--:--  8615
100  332M  100  332M    0     0  10.6M      0  0:00:31  0:00:31 --:--:-- 10.8M

[josevnz@dmaf5 Downloads]$ ~/Downloads/local-log4j-vuln-scanner --quiet ~/Downloads/ghidra_10.1.1_PUBLIC/
Checking for vulnerabilities: CVE-2019-17571, CVE-2021-44228, CVE-2021-45105
```

Very good, this version is not vulnerable to a log4J exploit.

But, there are any other vulnerabilities? OWASP wrote a really nice dependency analyzer you can [use](https://owasp.org/www-project-dependency-check/):

```shell
[josevnz@dmaf5 Downloads]$ curl --fail --output ~/Downloads/dependency-check-6.5.3-release.zip --location https://github.com/jeremylong/DependencyCheck/releases/download/v6.5.3/dependency-check-6.5.3-release.zip
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   669  100   669    0     0   4430      0 --:--:-- --:--:-- --:--:--  4430
100 23.0M  100 23.0M    0     0  7653k      0  0:00:03  0:00:03 --:--:-- 8899k
```

[Scanning](https://jeremylong.github.io/DependencyCheck/dependency-check-cli/index.html) one more time:

```shell
[josevnz@dmaf5 Downloads]$ ~/Downloads/dependency-check/bin/dependency-check.sh --prettyPrint --format HTML -scan /home/josevnz/Downloads/ghidra_10.0.4_PUBLIC/Ghidra/Framework/Generic/lib/
[INFO] Checking for updates
[INFO] Skipping NVD check since last check was within 4 hours.
[INFO] Skipping RetireJS update since last update was within 24 hours.
[INFO] Check for updates complete (68 ms)
[INFO] 

Dependency-Check is an open source tool performing a best effort analysis of 3rd party dependencies; false positives and false negatives may exist in the analysis performed by the tool. Use of the tool and the reporting provided constitutes acceptance for use in an AS IS condition, and there are NO warranties, implied or otherwise, with regard to the analysis or its use. Any use of the tool and the reporting provided is at the user’s risk. In no event shall the copyright holder or OWASP be held liable for any damages whatsoever arising out of or in connection with the use of this tool, the analysis performed, or the resulting report.


   About ODC: https://jeremylong.github.io/DependencyCheck/general/internals.html
   False Positives: https://jeremylong.github.io/DependencyCheck/general/suppression.html

💖 Sponsor: https://github.com/sponsors/jeremylong


[INFO] Analysis Started
[INFO] Finished Archive Analyzer (0 seconds)
[INFO] Finished File Name Analyzer (0 seconds)
[INFO] Finished Jar Analyzer (0 seconds)
[INFO] Finished Central Analyzer (0 seconds)
[INFO] Finished Dependency Merging Analyzer (0 seconds)
[INFO] Finished Version Filter Analyzer (0 seconds)
[INFO] Finished Hint Analyzer (0 seconds)
[INFO] Created CPE Index (1 seconds)
[INFO] Finished CPE Analyzer (2 seconds)
[INFO] Finished False Positive Analyzer (0 seconds)
[INFO] Finished NVD CVE Analyzer (0 seconds)
[INFO] Finished Sonatype OSS Index Analyzer (0 seconds)
[INFO] Finished Vulnerability Suppression Analyzer (0 seconds)
[INFO] Finished Dependency Bundling Analyzer (0 seconds)
[INFO] Analysis Complete (3 seconds)
[INFO] Writing report to: /home/josevnz/Downloads/./dependency-check-report.html
```

The report could generate false dependencies, there is a [way to minimize them](https://jeremylong.github.io/DependencyCheck/general/suppression.html):



# What did we learn?

This was quick and intense, so let's summarize a few things we learned:

* You can scan your python projects, for third party library [vulnerabilities](https://www.nist.gov/) using [pip-audit](https://github.com/trailofbits/pip-audit)
* Same applies to Java. There are specialized tools out there or generic ones like [OWASP Dependency-CLI](https://jeremylong.github.io/DependencyCheck/dependency-check-cli/index.html)
* As a plus, you can see how you can [quickly wrap your code](https://github.com/josevnz/EnableSysadminRssReader) using the new setuptools packaging rules (setup.cfg as opposed to setup.py)