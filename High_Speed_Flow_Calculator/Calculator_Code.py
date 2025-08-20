import pandas as pd;
import numpy as np;
from scipy.optimize import fsolve;

class calculator:
    def __init__(self):
        self.gamma = 1.4;
        self.R = 287;
    
    def plot(self):
        data = [["Mach Number", self.M], ["p/p0", self.p_p0], ["T/T0", self.t_t0], ["Rho/Rho0", self.rho_rho0], ["A/A*", self.a_astar], ["p/p*", self.p_pstar], ["T/T*", self.t_tstar], ["rho/rho*", self.rho_rhostar], ["Mach Angle", self.mu], ["P.M. Angle", self.nu]];
        df = pd.DataFrame(data, columns=["Parameter", "Value"]);
        print(df);
    
    def plot2 (self):
        data = [["M1", self.M1], ["M2", self.M2], ["T2/T1", self.t2_t1], ["P2/P1", self.p2_p1], ["Rho2/Rho1", self.r2_r1], ["P02/P01", self.p02_p01], ["P1/P02", self.p1_p02]];
        df = pd.DataFrame(data, columns=["Parameter", "Value"]);
        print(df);
        
    def plot3 (self):
        data = [["M1", self.M1], ["M2", self.M2], ["M1n", self.M1n], ["M2n", self.M2n], ["Wave Angle", (180/np.pi)*self.B], ["Turn Angle", (180/np.pi)*self.delta], ["T2/T1", self.t2_t1], ["P2/P1", self.p2_p1], ["Rho2/Rho1", self.r2_r1], ["P02/P01", self.p02_p01]];
        df = pd.DataFrame(data, columns=["Parameter", "Value"]);
        print(df);
    
    # ISENTROPIC FLOW
    def isentropic_Mach(self, M):
        if (M <= 0):
            print("Invalid Input. Mach number must be greater than 0.");
            return;
        self.M = M;
        self.t_t0 = (1 + 0.5*(self.gamma - 1)*(self.M ** 2)) ** (-1);
        self.p_p0 = (self.t_t0) ** (self.gamma / (self.gamma - 1));
        self.rho_rho0 = (self.t_t0) ** (1 / (self.gamma - 1));
        self.a_astar = (1/M)*((2/(self.gamma+1))*(1 + 0.5*(self.gamma-1)*self.M*self.M))**(0.5*(self.gamma + 1)/(self.gamma-1));
        self.p_pstar = self.p_p0 * ((self.gamma + 1)*0.5)**(self.gamma/(self.gamma - 1));
        self.t_tstar = self.t_t0 * ((self.gamma + 1)/2);
        self.rho_rhostar = self.rho_rho0 * ((self.gamma + 1)/2) ** (1/(self.gamma - 1));
        if (self.M >= 1):
            k = 180/np.pi;
            self.mu = k*np.arcsin(1/self.M);
            A = np.sqrt((self.gamma + 1)/(self.gamma - 1));
            x = np.sqrt(self.M**2 - 1);
            self.nu = k*(A*np.arctan(x/A) - np.arctan(x));
        else:
            self.mu = "-";
            self.nu = "-";
        self.plot();
    
    def isentropic_pp0 (self, pp0):
        M = np.sqrt((2/(self.gamma-1))*((pp0)**((1-self.gamma)/self.gamma) - 1));
        self.isentropic_Mach(M);
    
    def isentropic_TT0 (self, tt0):
        M = np.sqrt((2/(self.gamma-1))*((tt0)**(-1) - 1));
        self.isentropic_Mach(M);
        
    def isentropic_RhoRho0 (self, rr0):
        M = np.sqrt((2/(self.gamma-1))*((rr0)**(1 - self.gamma) - 1));
        self.isentropic_Mach(M);
        
    def isentropic_MachAngle (self, mu):
        k = np.pi/180;
        M = 1/np.sin(k*mu);
        self.isentropic_Mach(M);
    
    def f(self, M):
        A = np.sqrt((self.gamma + 1)/(self.gamma - 1));
        x = np.sqrt(M*M - 1);
        y = A*np.arctan(x/A) - np.arctan(x) - self.nu;
        return y;
    
    def isentropic_PMAngle (self, nu):
        self.nu = (np.pi/180)*nu;
        M = fsolve(self.f, 3);
        self.isentropic_Mach (M);
        
    def f2 (self, M):
        power = 0.5*(self.gamma + 1)/(self.gamma - 1);
        base = (1 + 0.5*(self.gamma - 1)*M*M)*(2/(self.gamma + 1));
        return (base ** power)/M - self.a_astar;
    
    def isentropic_AAstar_subsonic (self, aastar):
        self.a_astar = aastar;
        M = fsolve(self.f2, 0.3);
        self.isentropic_Mach (M);
    
    def isentropic_AAstar_supersonic (self, aastar):
        self.a_astar = aastar;
        M = fsolve(self.f2, 3);
        self.isentropic_Mach(M);
        
    #NORMAL SHOCK
    def normalShock_M1 (self, M1):
        if (M1 <= 1):
            print("Invalid Input. M1 should be greater than 1");
            return;
        self.M1 = M1;
        #M2
        self.M2 = np.sqrt(((self.gamma - 1)*(M1**2) + 2)/(2*self.gamma*(M1**2) - (self.gamma - 1)));
        #T2/T1
        self.t2_t1 = ((2*self.gamma*M1*M1 - (self.gamma - 1))*(2 + (self.gamma - 1)*M1*M1))/(((self.gamma + 1)*M1)**2);
        #P2/P1
        self.p2_p1 = (2*self.gamma*M1*M1 - (self.gamma - 1))/(self.gamma + 1);
        #rho2/rho1
        self.r2_r1 = ((self.gamma + 1)*(M1**2))/(2 + (self.gamma - 1)*(M1**2));
        #P02/P01
        temp1 = (0.5*(self.gamma + 1)*((M1**2)/(1 + 0.5*(self.gamma - 1)*(M1**2))))**(self.gamma/(self.gamma - 1));
        temp2 = ((2*self.gamma/(self.gamma + 1))*(M1**2) - ((self.gamma - 1)/(self.gamma + 1)))**(-1/(self.gamma - 1));
        self.p02_p01 = temp1*temp2;
        #P1/P02
        temp3 = (0.5*(self.gamma + 1)*(M1**2))**(self.gamma/(self.gamma - 1));
        temp4 = (((2*self.gamma*(M1**2))/(self.gamma + 1)) - ((self.gamma - 1)/(self.gamma + 1)))**(1/(self.gamma - 1));
        self.p1_p02 = temp4/temp3;
        #Plot
        self.plot2();
        
    def normalShock_M2 (self, M2):
        if (M2 < 0.37796447 or M2 >= 1):
            print("Invalid Input. M2 should be between 0.37796447 and 1");
            return;
        M1 = np.sqrt((2 + (M2**2)*(self.gamma - 1))/(2*self.gamma*(M2**2) - (self.gamma - 1)));
        self.normalShock_M1(M1);
        
    def normalShock_P2P1 (self, p2p1):
        if (p2p1 <= 1):
            print("Invalid Input. P2/P1 must be greater than 1.");
            return;
        M1 = np.sqrt(0.5*(self.gamma + 1)*p2p1/self.gamma + (self.gamma - 1)/(2*self.gamma));
        self.normalShock_M1(M1);
    
    def normalShock_Rho2Rho1 (self, r2r1):
        if (r2r1 <= 1 or r2r1 > 6):
            print("Invalid Input. Rho2/Rho1 must be between 1 and 6");
            return;
        M1 = np.sqrt((2*r2r1)/((self.gamma + 1) - (self.gamma - 1)*r2r1));
        self.normalShock_M1(M1);
            
    def g1 (self, M1):
        y = (2*self.gamma*(M1**2) - (self.gamma - 1))*(2 + (self.gamma - 1)*(M1**2))/(((self.gamma + 1)*(M1))**2);
        return y - self.t2_t1;
    
    def g2 (self, M1):
        temp1 = (0.5*(self.gamma + 1)*((M1**2)/(1 + 0.5*(self.gamma - 1)*(M1**2))))**(self.gamma/(self.gamma - 1));
        temp2 = ((2*self.gamma/(self.gamma + 1))*(M1**2) - ((self.gamma - 1)/(self.gamma + 1)))**(-1/(self.gamma - 1));
        y = temp1*temp2;
        return y - self.p02_p01;

    def g3 (self, M1):
        temp3 = (0.5*(self.gamma + 1)*(M1**2))**(self.gamma/(self.gamma - 1));
        temp4 = (((2*self.gamma*(M1**2))/(self.gamma + 1)) - ((self.gamma - 1)/(self.gamma + 1)))**(1/(self.gamma - 1));
        y = temp4/temp3;
        return y - self.p1_p02;
    
    def normalShock_T2T1 (self, t2t1):
        if (t2t1 <= 1):
            print("Invalid Input. T2/T1 should be greater than 1.");
            return;
        self.t2_t1 = t2t1;
        M1 = fsolve(self.g1, 3);
        self.normalShock_M1(M1);
    
    def normalShock_P02P01 (self, p02p01):
        if (p02p01 <= 0 or p02p01 >= 1):
            print("Invalid Input. P02/P01 should be between 0 and 1.");
            return;
        self.p02_p01 = p02p01;
        M1 = fsolve(self.g2, 3);
        self.normalShock_M1(M1);
    
    def normalShock_P1P02 (self, p1p02):
        if (p1p02 <= 0 or p1p02 >  0.52828178):
            print("Invalid Input. P1/P02 must be between 0 and  0.52828178.");
            return;
        self.p1_p02 = p1p02;
        M1 = fsolve(self.g3, 3);
        self.normalShock_M1(M1);
    
    #OBLIQUE SHOCK
    def obliqueShock_WaveAngle (self, M1, B):
        B = (np.pi/180)*B;
        self.B = B;
        M1n = M1*np.sin(B);
        if (M1n <= 1):
            print("Invalid Input. M1n should be greater than 1");
            return;
        self.M1 = M1;
        self.M1n = M1n;
        #Turn Angle
        self.delta = np.arctan((2*(1/np.tan(B))*(M1n**2 - 1))/((M1**2)*(self.gamma + np.cos(2*B)) + 2));
        #M2
        self.M2n = np.sqrt(((self.gamma - 1)*(M1n**2) + 2)/(2*self.gamma*(M1n**2) - (self.gamma - 1)));
        self.M2 = self.M2n/np.sin(B-self.delta);
        #T2/T1
        self.t2_t1 = ((2*self.gamma*(M1n**2) - (self.gamma - 1))*(2 + (self.gamma - 1)*(M1n**2)))/(((self.gamma + 1)*M1n)**2);
        #P2/P1
        self.p2_p1 = (2*self.gamma*(M1n**2) - (self.gamma - 1))/(self.gamma + 1);
        #rho2/rho1
        self.r2_r1 = ((self.gamma + 1)*(M1n**2))/(2 + (self.gamma - 1)*(M1n**2));
        #P02/P01
        temp1 = (0.5*(self.gamma + 1)*((M1n**2)/(1 + 0.5*(self.gamma - 1)*(M1n**2))))**(self.gamma/(self.gamma - 1));
        temp2 = ((2*self.gamma/(self.gamma + 1))*(M1n**2) - ((self.gamma - 1)/(self.gamma + 1)))**(-1/(self.gamma - 1));
        self.p02_p01 = temp1*temp2;
        
        #Plot
        self.plot3();
        
    def obliqueShock_M1n (self, M1, M1n):
        self.B = np.arcsin(M1n/M1);
        if (M1n <= 1):
            print("Invalid Input. M1n should be greater than 1");
            return;
        self.M1 = M1;
        self.M1n = M1n;
        #Turn Angle
        self.delta = np.arctan((2*(1/np.tan(B))*(M1n**2 - 1))/((M1**2)*(self.gamma + np.cos(2*B)) + 2));
        #M2
        self.M2n = np.sqrt(((self.gamma - 1)*(M1n**2) + 2)/(2*self.gamma*(M1n**2) - (self.gamma - 1)));
        self.M2 = self.M2n/np.sin(B-self.delta);
        #T2/T1
        self.t2_t1 = ((2*self.gamma*(M1n**2) - (self.gamma - 1))*(2 + (self.gamma - 1)*(M1n**2)))/(((self.gamma + 1)*M1n)**2);
        #P2/P1
        self.p2_p1 = (2*self.gamma*(M1n**2) - (self.gamma - 1))/(self.gamma + 1);
        #rho2/rho1
        self.r2_r1 = ((self.gamma + 1)*(M1n**2))/(2 + (self.gamma - 1)*(M1n**2));
        #P02/P01
        temp1 = (0.5*(self.gamma + 1)*((M1n**2)/(1 + 0.5*(self.gamma - 1)*(M1n**2))))**(self.gamma/(self.gamma - 1));
        temp2 = ((2*self.gamma/(self.gamma + 1))*(M1n**2) - ((self.gamma - 1)/(self.gamma + 1)))**(-1/(self.gamma - 1));
        self.p02_p01 = temp1*temp2;
        
        #Plot
        self.plot3();
        
    def h1 (self, B):
        y = np.arctan((2*(1/np.tan(B))*((self.M1*np.sin(B))**2 - 1))/((self.M1**2)*(self.gamma + np.cos(2*B)) + 2));
        return y - self.delta;
    
    def obliqueShock_TurnAngle_weak (self, M1, delta):
        self.delta = delta;
        self.M1 = M1;
        self.B = fsolve(self.h1, (np.pi/180)*10);
        print(180*self.B/np.pi);
        self.obliqueShock_WaveAngle(M1, self.B);
        
    def obliqueShock_TurnAngle_strong (self, M1, delta):
        self.delta = delta;
        self.M1 = M1;
        self.B = fsolve(self.h1, 1);
        self.obliqueShock_WaveAngle(M1, B);
    
x = calculator();
x.isentropic_Mach(3);