set PYTHON=C:\Python39\python.exe
set DROPBOX_BIN=E:\Users\hugovk\Dropbox\bin
set DROPBOX_DATA=E:\Users\hugovk\Dropbox\bin\data
set TEE=%DROPBOX_BIN%\UnxUtils\tee

:loop

@date/t && time/t
@for %%x in (nixibot favibot lovihatibot) do @%PYTHON% %DROPBOX_BIN%\%%x.py -t none -i M:\bin\data\%%x.ini -c C:\Users\hugovk\bin\data\%%x.csv
@date/t && time/t

@%PYTHON% %DROPBOX_BIN%\sleep.py 3600 REM 60 mins (sleep.exe not on all WinXP)

goto loop
