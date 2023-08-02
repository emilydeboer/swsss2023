from numpy.linalg import norm

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
    
    k = [f(x, t)]
    s = len(c)
    
    # evaluation of slopes
    
    for i in range(s-1):
        x_tilde = [x + h*sum(a[i][j]*k[j]) for j in range(len(k))]
        k.append(f(x_tilde, t + c[i+1]*h))
    
    x_hat = x + h*sum(b[i]*k[i] for i in range(len(k)))
    
    return x_hat # please complete this function 

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

a = [[1/5],
     [3/40, 9/40], 
     [44/45, -56/15, 32/9], 
     [19372/6561, -25360/2187, 64448/6561, -212/729],  
     [9017/3168, -355/33, 46732/5247, 49/176, -5103/18656], 
     [35/384, 0, 500/1113, 125/192, -2187/6784, 11/84]]
b = [35/384, 0, 500/1113, 125/192, -2187/6784, 11/84, 0]
c = [0, 1/5, 3/10, 4/5, 8/9, 1, 1]
b_control = [5179/57600, 0, 7571/16695, 393/640, -92097/339200, 187/2100, 1/40]

test = explicit_RK_stepper(f,x,t,h,a,b,c)

