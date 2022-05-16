import pulp as p
import argparse
import sys
import mt as matrix
import numpy as np
def neg(num):
        return -1*num

# Dummy function
def transform(isNormal):
        result=[]
        mt=matrix.mt
        if not isNormal:
                mt=np.transpose(np.array(mt))
        
        row=len(mt)
        col=len(mt[0])
        
        p_list=['p{}'.format(i) for i in range(1,col+1)]
        pi=[p.LpVariable(p_list[i], lowBound = 0, upBound = 1) for i in range(col) ]
        v1 = p.LpVariable(name="V1", lowBound=0)
        v2 = p.LpVariable(name="V2", lowBound=0)
        result.append(v1-v2)
        for i in range(row):
                temp_list=[]
                for j in range(len(pi)):
                        temp_list.append((pi[j],mt[i][j]))
                expression=p.LpAffineExpression(temp_list)
                if not isNormal:
                        rhs=-v1+v2<=0
                else:
                        rhs=-v1+v2>=0
                result.append(expression+rhs)
        
        return (result, row, col)

if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument("Form", help="Input the format for LP problem (S)tandard form or (D)ual form")
        args = parser.parse_args()
        isNormal=True if args.Form =='S' else False

        result=[]
        mt=matrix.mt
        if not isNormal:
                mt=np.transpose(np.array(mt))
        
        row=len(mt)
        col=len(mt[0])
        if isNormal:
                model = p.LpProblem(name="Standard-problem", sense=p.LpMaximize)
        else:
                model = p.LpProblem(name="Dual-problem", sense=p.LpMinimize)
        v1=None
        v2=None
        w1=None
        w2=None
        if isNormal:
                v1 = p.LpVariable(name="V1", lowBound=0)
                v2 = p.LpVariable(name="V2", lowBound=0)
                model+=(v1-v2)
        else:
                w1 = p.LpVariable(name="W1", lowBound=0)
                w2 = p.LpVariable(name="W2", lowBound=0)
                model+=(w1-w2)
        
        p_list=['p{}'.format(i) for i in range(1,col+1)]
        pi=[p.LpVariable(p_list[i], lowBound = 0, upBound = 1) for i in range(col) ]
        
        for i in range(row):
                temp_list=[]
                for j in range(len(pi)):
                        temp_list.append((pi[j],mt[i][j]))
                expression=p.LpAffineExpression(temp_list)
                if not isNormal:
                        rhs=-w1+w2<=0
                else:
                        rhs=-v1+v2>=0
                model+=(expression+rhs)

        if not isNormal:
                temp_list1=[]
                temp_list2=[]
                for j in range(len(pi)):
                        temp_list1.append((pi[j],1))
                        temp_list2.append((pi[j],-1))
                expression1=p.LpAffineExpression(temp_list1)
                expression2=p.LpAffineExpression(temp_list2)
                model+=(expression1<=1)
                model+=(expression2<=-1)
        else:
                temp_list1=[]
                temp_list2=[]
                for j in range(len(pi)):
                        temp_list1.append((pi[j],1))
                        temp_list2.append((pi[j],-1))
                expression1=p.LpAffineExpression(temp_list1)
                expression2=p.LpAffineExpression(temp_list2)
                model+=(expression1>=1)
                model+=(expression2>=-1)
        status = model.solve()   # Solver
        print(model)
        
        # Printing the final solution
        for i in range(len(pi)):
                print("{} = {}".format(p_list[i],p.value(pi[i])))
        value_of_game=None
        if isNormal:
                value_of_game=p.value(v1-v2)
        else:
                value_of_game=p.value(w1-w2)
        print("Value of the game is: {}".format(value_of_game))
