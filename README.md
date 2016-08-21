# RSAS Removed Steganography Application Scanner

### *Forensic Steganalysis Triage by Detecting Artifacts of Removed Applications*

University of Kent, UK (2016)

School of Computing (cs.kent.ac.uk)

Author:
   Mr Nicola Talin
   nt271@kent.ac.uk

Supervisor:
   Dr Julio C. Hernandez-Castro
   jch27@kent.ac.uk


## RSAS is a forensic software which scans the system for traces of removed applications.

RSAS uses a database of forensic artifacts which are left in the system after the removal of Steganography applications, to determine whether any of the applications in the database has ever been run in the target system. This operation is known as Forensic Steganalysis Triage and provides to the investigator in few seconds a report of which Steganography applications have been run in the system, even if such applications have been uninstalled or deleted.

DISCLAIMER:
> The software comes as it is and the authors and the University of Kent take no responsibilities for any damange or consequence of using this software.

LICENSE:
> This software and its source code are available under [GPL v.3 License](./LICENSE)



## ===== INSTRUCTIONS FOR USERS:  =====


RSAS works on Windows 7, 8 and 10.


### WHICH FILE IS THE DISTRIBUTABLE AND EXECUTABLE VERSION OF RSAS:

In most cases you will just need:

  `/dist/rsas.exe`



### DEPENDENCY ISSUES:

On Windows 8.1 or earlier, RSAS might throw this error when started:

> The program can't start because api-ms-win-crt-math-l1-1-0.dll is missing from your computer. Try reinstalling the program to fix this problem.

If this is the case, you will need to install in the target system the Windows Update Package KB2999226, which provides WinUCRT (Windows Universal C Runtime Libraries).

You can download it from the official Microsoft website: https://support.microsoft.com/en-gb/kb/2999226

or you can find it here on /redist/wincrt-redistributable/

Please select the correct installation file for your target os version:

| Version of Windows in your taget system        | Update Installation File        | 
|------------------------------------------------|---------------------------------|
| Windows Vista 32-bit (not supported by RSAS)   | `Windows6.0-KB2999226-x86.msu`  |
| Windows Vista 64-bit (not supported by RSAS)   | `Windows6.0-KB2999226-x64.msu`  |
| Windows 7 32-bit                               | `Windows6.1-KB2999226-x86.msu`  |
| Windows 7 64-bit                               | `Windows6.1-KB2999226-x64.msu`  |
| Windows 8.0 (32-bit)                           | `Windows8-RT-KB2999226-x86.msu` |
| Windows 8.0 (64-bit)                           | `Windows8-RT-KB2999226-x64.msu` |
| Windows 8.1 (32-bit)                           | `Windows8.1-KB2999226-x86.msu`  |
| Windows 8.1 (64-bit)                           | `Windows8.1-KB2999226-x64.msu`  |
| Windows 10 (any)                               | *update not needed*             |

After installing the update, you should not need to reboot the system to be able to use RSAS.



### DATABASE CUSTOMISATION:

`/dist/rsas.exe` embeds the artifacts database.

Before using the embedded database, `rsas.exe` will look in the folder where itself is currently located for a `rsas.sqlite3` file. If present, RSAS will attempt to use such external file as artifact database, instead of the embedded one.

This allows the investigators to use their customised artifacts database.

To customise your artifacts database please do as follows:

* copy `/data/rsas.sqlite3` on your favorite location. This is a copy of the same database embedded in `rsas.exe`
* open and edit your copy of `rsas.sqlite3` using a tool such as [SQLite Studio](http://sqlitestudio.pl/)
* make sure your version of `rsas.sqlite3` is located in the same folder as `rsas.exe`, if you wish `rsas.exe` to use your database. Move `rsas.sqlite3` in a different location to make `rsas.exe` use the embedded database again.



### EDITING THE DATABASE:

RSAS does not come yet with a database-editing functionality.
Please use a tools such as [SQLite Studio](http://sqlitestudio.pl/) to edit the database.
The tables you are likely to be interested in editing are `artifacts` and `apps`.


#### The `apps` table:

You will be interested in the fields `id` and `name`.
Please make sure `id` is a unique positive integer and `name` is a string without unusual characters.
Any other field in the table is not used so far by RSAS, but you might be interested in using them for your own records, as you can save author, link, and other detais for each application.


#### The `artifacts` table:

Each artifact description identifies one or more artifacts in the system which belongs to a specific application from the `apps` table.

Of course each artifact has a unique positive integer `id` field, and an `app` field where the `id` of the corresponding application from the `apps` table should be stored.

Artifacts are categorised in different types, using positive integers.

* Artifact types between 1001 and 1999 are descriptions for **filesystem artifacts**.
* Artifact types between 2001 and 2999 are descriptions for **Windows Registry artifacts**.

Specifically,

* Type `1001` identifies **installation and configuration files**;
* Type `1002` is dedicated to **Windows Prefetch files**;
* Type `2001` identifies a **Registry Key, the very presence of which is considered evdence** that the corresponding applicaton was run in the system;
* Type `2002` identifies a **Registry Key that should contain at least one value corresponding to a specified pattern** for it to be considered evidence that the application was run in the system.

For **Type-1000 artifacts (filesystem artifacts)**, the `path` field is used to describe the filepath.
The use of the wildcard `*` is allowed.
Do not start the path with the disc unit letter.
As an example, an artifact such as `C:\Windows\Prefetch\ANUBIS.EXE-8351B2F9.pf` should be described in the `path` field with the value `Windows\Prefetch\ANUBIS.EXE-*.pf`. This is because RSAS will look for that path into each connected hard drive or removable drive (discs and network drives are not included in this search).


For **Type-2000 artifacts (registry artifacts)**, the PATH field is used to describe the Registry Key path.
The use of the wildcard `*` is allowed.
Please make sure the path starts with one of the following short names for the main keys:

| Short name to be used | Main Registry Key            |
|-----------------------|------------------------------|
| `HKU`                 | `HKEY_USERS`                 |
| `HKCU`                | `HKEY_CURRENT_USER`          |
| `HKCR`                | `HKEY_CLASSES_ROOT`          |
| `HKLM`                | `HKEY_LOCAL_MACHINE`         |
| `HKPD`                | `HKEY_PERFORMANCE_DATA`      |
| `HKCC`                | `HKEY_CURRENT_CONFIG`        |
| `HKDD`                | `HKEY_DYN_DATA`              |

Usually, rather than using `HKCU\your\path`, it is preferrable to use `HKU\*\your\path`, as this will look into `\your\path` for the `HKEY\{ID}\` key of each user, while `HKCU` is a link to the `HKEY\{ID}\` key of just the current user, which might not be the user which used the application you are scanning for.

For artifact of type `2002`, please use the `val` field to describe how to match the values in the key that will constitues your artifacts. It is highly suggested to make use of keywords with the help of the wildcard `*`.

Any other field in the artifacts table is not currently used by RSAS. It might be worth using them to indicate in which versions of Windows the described artifact is expected to be found. If the DB will increase in size to the point that the scan will result too slow, future versions of RSAS might include a selective selection of artifacts from the DB, by choosing only those corresponding to the version of Windows of the target system.




## ===== INSTRUCTIONS FOR DEVELOPERS: =====


### SOURCE CODE:

RSAS is developed in [Python v3.5](https://www.python.org) using [Object-Oriented Programming](https://en.wikipedia.org/wiki/Object-oriented_programming).

The Python code is included in the folder `/src/` and the main file `/rsas.py`

The code is organised in 4 packages:

| PACKAGE   | DESCRIPTION                                       |
|-----------|---------------------------------------------------|
| `src.cli` | for the **Command Line Interface**                |
| `src.gui` | for the **Graphical User Interface**              |
| `src.lib` | contains the **main libraries**, including `CONST`, `Scanner` and all the Object Classes used by `Scanner` such as `Apps`, `ArtifactRule`, and so on |
| `src.db` | contanis libraries providing an **interface between RSAS and the chosen database** ([SQLite v.3](https://sqlite.org/)) |



### DATABASE:

RSAS uses an [SQLite v.3](https://sqlite.org/) database containing the Artifact descriptions that RSAS will use to look in the system for traces of removed applications.

The database is stored in `/data/rsas.sqlite3`



### DISTRIBUTABLE:

The distributable version of the application is a single Windows executable file generated using [PyInstaller](http://www.pyinstaller.org/) and stored in `/dist/rsas.exe`

In case you wish to modify the Python code and/or the SQLite DB, please build your new version of rsas.exe using the following command from the Windows Command Prompt:

`pyinstaller -F rsas.spec`

Plase make sure first that:
* [Python 3.5](https://www.python.org/) and [PyInstaller](http://www.pyinstaller.org/)are propertly installed and configured in your system
* your current working directory is the main directory of the *rsas* project
* you are not using the **WRONG** command `pyinstaller -F rsas.py`, as such command would re-generate the `rsas.spec` file, and the [SQLite v.3](https://sqlite.org/) database would **NOT** be embedded in your `rsas.exe`

Please note that the `/build/` folder is created and used automatically by [PyInstaller](http://www.pyinstaller.org/).


21 Aug 2016

*Nicola Talin*
nt271@kent.ac.uk
