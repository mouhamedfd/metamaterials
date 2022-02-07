freq=5.2e9;
c0=3e8;
a=7.723e-3
er=4.4;
rho=2.049e-3;
lambda0=c0/(freq);
eta0=120*pi;
ko=2*pi/lambda0;
k=ko*sqrt(er);
Rr=(1/2)*(eta0*lambda0^2)/( (pi^3*a^2)*(4/3-(8/15)*(ko*a)^2+(11/105)*(ko*a)^4))
Rin= (Rr*besselj(1,k*rho)^2/besselj(1,1.84118)^2)