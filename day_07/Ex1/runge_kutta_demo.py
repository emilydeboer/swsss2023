from numpy.linalg import norm
import numpy as np

def explicit_RK_stepper(f,x,t,h,a,b,c):
    """
        Implementation of generic explicit Runge-Kutta update for explicit ODEs
        
        inputs:
            x - current state 
            t - current time
            f - right-hand-side of the (explicit) ODE to be integrated (signature f(x,t))
            h - step size 
            a - coefficients of Runge-Kutta method (organized as list-of-list (or vector-of-vector))
            b - weights of Runge-Kutta method (list/vector)
            c - nodes of Runge-Kutta method (including 0 as first node) (list/vector)

        outputs: 
            x_hat - estimate of the state at time t+h
    """
    
    s_len = len(b)-1
    k = np.zeros(s_len)
    
    k[0] = f(x,t)
    x_k = np.zeros(s_len)
    
    for s in range(1, s_len):
        x_k[s] = 0
        for j in range (0, s_len-1):
            x_k[s] = x_k[s] + a[s][j]*k[j]
        
        x_k[s] = x + h*x_k[s] 
        t_k = t + c[s]*h
        
        k[s] = f(x_k[s], t_k[s])

    k = f(x_for_k, t_for_k)
     
    x_hat = x_initial + h*np.sum(b_i*k_i)# state at time t+h
    
    return x_hat  # please complete this function 

def integrate(f, x0, tspan, h, step):
    """
        Generic integrator interface

        inputs:
            f     - rhs of ODE to be integrated (signature: dx/dt = f(x,t))
            x0    - initial condition (numpy array)
            tspan - integration horizon (t0, tf) (tuple)
            h     - step size
            step   - integrator with signature: 
                        step(f,x,t,h) returns state at time t+h 
                        - f rhs of ODE to be integrated
                        - x current state
                        - t current time 
                        - h stepsize

        outputs: 
            ts - time points visited during integration (list)
            xs - trajectory of the system (list of numpy arrays)
    """
    t, tf = tspan
    x = x0
    trajectory = [x0]
    ts = [t]
    while t < tf:
        h_eff = min(h, tf-t)
        x = step(f,x,t,h_eff)
        t = min(t+h_eff, tf)
        trajectory.append(x)
        ts.append(t)
    return trajectory, ts