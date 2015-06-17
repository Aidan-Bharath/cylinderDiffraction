import numpy as np
import cythontest as cy



if __name__ == "__main__":

    x = np.linspace(1,10,10)
    y = np.linspace(1,10,10)
    print type(x[2])
    print cy.test(x,y)
