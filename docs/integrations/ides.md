# IDEs

The package can be directly consumed in some Integrated Development
Environments, such as [PyCharm](https://www.jetbrains.com/pycharm/).

## PyCharm

1.  Install `ydata-profiling` via
    `../getting_started/installation`{.interpreted-text role="doc"}
2.  Locate your `ydata-profiling` executable.

 On macOS / Linux / BSD:

 ``` console
 $ which ydata_profiling
 (example) /usr/local/bin/ydata_profiling
 ```

 On Windows:

 ``` console
 $ where ydata_profiling
 (example) C:\ProgramData\Anaconda3\Scripts\ydata_profiling.exe
 ```

3.  In PyCharm, go to *Settings* (or *Preferences* on macOS) \ *Tools*
    \ *External tools*
4.  Click the **+** icon to add a new external tool
5.  Insert the following values

 -   Name: `Data Profiling`
     -   Program: *The location obtained in step 2*
     -   Arguments:
         `"$FilePath$" "$FileDir$/$FileNameWithoutAllExtensions$_report.html"`
     -   Working Directory: `$ProjectFileDir$`

![PyCharm Integration](https://ydata-profiling.ydata.ai/docs/assets/pycharm-integration.png%20##change%20this%20image){.align-center
width="400px"}

To use the PyCharm Integration, right click on any dataset file and
*External Tools* \ *Data Profiling*.

<img referrerpolicy="no-referrer-when-downgrade" src="https://static.scarf.sh/a.png?x-pxid=baa0e45f-0c03-4190-9646-9d8ea2640ba2" />