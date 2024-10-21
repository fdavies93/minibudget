import shutil
import subprocess
import csv
import io

def beancount(file: str, currency: str):
    # Validate bean-query is in PATH
    if shutil.which("bean-query") == None:
        raise EnvironmentError("bean-query could not be found. Please make sure it's installed in your environment and try again.")
    # Issue query to get chart of accounts
    output = subprocess.run(["bean-query",
                             file,
                             "select account, sum(position) where (account ~ 'Expenses' or account ~ 'Income' ) group by account order by account",
                             "--format",
                             "csv",
                             "-m"], 
                            capture_output=True)
    output_as_csv = csv.DictReader(io.StringIO(output.stdout.decode('utf-8')))
    print(output_as_csv.fieldnames)
    # Filter chart of accounts to the currency we care about
    # Return accounts in minibudget format
    pass
