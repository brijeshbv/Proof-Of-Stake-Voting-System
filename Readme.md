# A simple implementation of a Proof of Stake based Block Chain system for a Decentralized Voting Application

## Setup of Repository

1. Create a local conda environment :
 ```conda create --name <env>```
 2. Activate environment:
```conda activate <env>```
3. Install all requirements:
``` pip install -r requirements.txt```


### Running the System:

1. Genesis Node: 
<br />
```
python main.py localhost 10001 5002 keys/genesisPrivateKey.pem
```
<br />
2. Staker Node:
<br />
```
python main.py localhost 10002 5003 keys/stakerPrivateKey.pem
```
<br />
3. Test Script :
<br />
```
python interaction.py >test_no<
```
<br />
test_no = [1,2,3,4]