 ![image](https://github.com/user-attachments/assets/f0d75bc0-c7c9-4341-8dd7-468b25079fba)


# U.S.-National-Debt-Clock
This project is a Python-based implementation of the U.S. National Debt Clock, a real-time display of the current national debt of the United States. The clock provides an up-to-date visual representation of the national debt, along with other relevant financial metrics.
API: https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny

#
#tkinter:
import tkinter as tk: This module is used for creating graphical user interfaces (GUIs) in Python.
#
#requests:
import requests: This module is used for making HTTP requests to fetch data from APIs.
#
logging:
#import logging: This module is used for logging messages to track events that happen while software runs.
#
datetime:
#from datetime import datetime, timedelta: This module supplies classes for manipulating dates and times.
#
io:
#from io import StringIO: This module implements the classes for in-memory stream handling.

The error message you are seeing is a `PSSecurityException` from PowerShell, indicating that the script execution is blocked due to security settings. This is likely because the PowerShell execution policy is set to restrict running scripts.

To resolve this issue, you can change the PowerShell execution policy to allow script execution. Here are the steps to do this:

1. **Open PowerShell as Administrator**:
   - Right-click on the Start menu and select "Windows PowerShell (Admin)" or "Command Prompt (Admin)".

2. **Set the Execution Policy**:
   - In the PowerShell window, run the following command to set the execution policy to `RemoteSigned` (which allows running scripts that are created locally and those that are signed by a trusted publisher):

     ```powershell
     Set-ExecutionPolicy RemoteSigned
     ```

   - You may be prompted to confirm the change. Type `Y` and press Enter.

3. **Run Your Script Again**:
   - After changing the execution policy, try running your Python script again.

### Example Command to Change Execution Policy:
```powershell
Set-ExecutionPolicy RemoteSigned
```

### Explanation:
- **Execution Policy**: PowerShell's execution policy is a safety feature that controls the conditions under which PowerShell loads configuration files and runs scripts.
- **RemoteSigned**: This policy requires that all scripts and configuration files downloaded from the internet be signed by a trusted publisher. Scripts created locally do not need to be signed.

### Note:
- Be cautious when changing the execution policy, especially on production systems. The `RemoteSigned` policy is generally safe for development purposes.

After changing the execution policy, you should be able to run your Python script without encountering the `PSSecurityException`.

To re-enable the security execution policy in PowerShell, you can set the execution policy back to its default value. The default execution policy for Windows is Restricted, which prevents any scripts from running.

Here are the steps to set the execution policy back to Restricted:

Open PowerShell as Administrator:

Right-click on the Start menu and select "Windows PowerShell (Admin)" or "Command Prompt (Admin)".
Set the Execution Policy:

In the PowerShell window, run the following command to set the execution policy to Restricted:
```powershell
Set-ExecutionPolicy Restricted
```
