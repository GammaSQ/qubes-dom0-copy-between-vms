#DISCLAIMER: DO NOT USE! RISK OF COMPROMISING dom0!
I am no expert, neither did anybody audit the code, nor are there tests. If you want to use this, please read the code carefully and make sure you understand the rist. I DO NOT recommand usage in production systems.

# Copy between two (App)VMs in qubesOS

To copy a file from VM A to VM B by dom0-commands would usually require calling qvm-copy-to-vm from within A, so the command in dom0 looks like this:
 qvm-run A 'qvm-copy-to-vm B /path/to/file'
This directs VM A to ask dom0 to transfere some bytes to VM B. Appart from overhead, this requires the user to confirm this action.

However, since dom0 already approved this transfere, it should be possible to directly copy the file. This is exactly what this project is supposed to do: run command in VM A, get the bytestream and pass it along to VM B. The main difficulty is handling the response of B correctly, which in theory tell VM A weather the file-transfere was successful. Since this bytstream is actually interpreted at runtime, bugs could allow VM B to infect VM A, or allow VM B to communicate with VM A if both are infected. Therfore, the back-stream is sanitised with a python-script. This part is still in development and I haven't cought all "bad VM B"-scenarios yet.
