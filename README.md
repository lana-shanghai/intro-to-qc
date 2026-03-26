### Prerequisites

Install [python](https://www.python.org/downloads/).

Clone this repository and cd into it by running these commands in the terminal:

```
git clone https://github.com/lana-shanghai/intro-to-qc.git
cd intro-to-qc
```

Create virtual environment:

```
python -m venv .venv
source .venv/bin/activate
pip install qiskit qiskit-aer
```

Clone this repository by running this command in the terminal:
git clone https://github.com/lana-shanghai/intro-to-qc.git

Run the Hadamard gate on a qubit:

```
python hadamard.py
```

There is a small TODO in `bell_state.py` for you!

After we apply the Hadamard gate on the first qubit, 
we need to apply a controlled NOT (CNOT) gate on 
the second qubit. 

Run it like so: 

```
python bell_state.py
```

