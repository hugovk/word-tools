
:loop

@date/t && time/t
@for %%x in (nixibot favibot lovihatibot) do %%x.py -t none -i M:\bin\data\%%x.ini -c M:\bin\data\%%x.csv
@date/t && time/t

@sleep 1800 REM 30 mins (sleep.exe not on all WinXP)

goto loop
