import pathlib

uri = pathlib.Path("./target_file.py").resolve()
uri = pathlib.Path("C:\prive\med2\clickable_console/target_file.py").resolve()
print(uri)
uri = uri.as_posix()
print(uri)

# Open in current ide?
print(f"""Click here: "{uri}:33" """)
print(f'File "{uri}", line 20')
print(f'File without lineno "{uri}:20')
# Open in default ide
print(f"""Click here: file:///{uri}, line 13""")
print(f"""Click here: file:///{uri}, line 13""")
