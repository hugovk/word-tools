
:loop

@date/t && time/t
@for %%x in (nixibot favibot lovihatibot) do %%x.py -t none -i M:\bin\data\%%x.ini -c C:\Users\hugovk\bin\data\%%x.csv
@date/t && time/t

@sleep 3600 REM 60 mins (sleep.exe not on all WinXP)

goto loop
