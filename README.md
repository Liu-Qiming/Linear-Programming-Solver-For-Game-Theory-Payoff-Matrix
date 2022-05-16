# Linear Programming Solver with Matrix

By [Qiming Liu](https://www.linkedin.com/in/qliu0831)
```
This Solver uses package pulp: https://github.com/coin-or/pulp
```

## Prequisite
1. Requires Python 2.7 or Python >= 3.4 
2. Run the following command to install necessary packages:
    pip install pulp
    pip install numpy
3. run python3 lp.py --help to check manual:
    positional arguments:
    Form        Input the format for LP problem (S)tandard form or (D)ual form.

## Usage
### Update mt.py
```
Modify matrix mt under mt.py to the matrix you want to solve
```
### Solve Standard Form:
```
python3 lp.py S
```

### Solve Dual Form:
```
python3 lp.py D
```
