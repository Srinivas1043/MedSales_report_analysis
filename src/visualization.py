import os 
filename=input("kindly enter the file name with proper spelling: ")
os.system(f'cmd /k "streamlit run src/{filename}.py"')