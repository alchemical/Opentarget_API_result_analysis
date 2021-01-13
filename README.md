# Opentarget_API_result_analysis

### To run this script you need to have **python3** installed in your computer. The code was written and tested on the linux machine.
#### To use the script first you need install all the dependencies listed in requirements.txt 
pip install -r requirements.txt 
#### After installing just run the script
There are two scripts, one which directly uses the RESTAPI (**OTP_Bio_API.py**) while the other uses the python client (**OTP_Bio_pythonAPI.py**) for API. 
Both the script should give the same result/output and both the script should be run in the same way.

python3 OTP_Bio_API.py -t/--target target_id (for example: ENSG00000197386)

python3 OTP_Bio_API.py -d/--disease disease_id (for example: Orphanet_399)
### or
python3 OTP_Bio_pythonAPI.py -t/--target target_id (for example: ENSG00000197386)

python3 OTP_Bio_pythonAPI.py -d/--disease disease_id (for example: Orphanet_399)

Results/output will be provided directly on the terminal window. If you would like to save the result you can use '>' operator and desired filename.

python3 OTP_Bio_API.py -t/--target target_id > filename.dat
