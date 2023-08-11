import pandas as pd
import os
import glob

def compileExcelFiles():
    outputFileName = "compiled.xlsx"
    path = os.getcwd()
    excel_files = glob.glob(os.path.join(path, "*.xlsx"))
    df_raw = pd.DataFrame()
    df_clean = pd.DataFrame()
    
    for f in excel_files:
        try:
            print("Reading {}...".format(f))
            df_raw = pd.concat([df_raw, pd.read_excel(f, sheet_name="RAW")])
            df_clean = pd.concat([df_clean, pd.read_excel(f, sheet_name="CLEANED")])
        except Exception as e:
            print(e)
            exit()
    try:
        with pd.ExcelWriter(outputFileName) as writer:  
            df_raw.to_excel(writer, sheet_name='RAW', index=False)
            df_clean.to_excel(writer, sheet_name='CLEANED', index=False)
        print("Compiled Output Excel File name is " + outputFileName)
    except Exception as e:
        print(e)
        exit()
    return


def main():
    compileExcelFiles()
    print("Script ran successfully!")
    return


if __name__ == "__main__":
    main()