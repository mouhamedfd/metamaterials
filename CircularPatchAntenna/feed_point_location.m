freq=5.2; % design frequency
er=4.4; % substrate permittivity
tan_delta=0.02; % loss tan
h=0.12; % substrate height (cm)
conductivity=5.8*10^7; % sigma
t=[0:0.001:pi/2]; % for integration
rho=0.2049; % feed position (cm)

lambda_o=30.0/freq; % wavelength vaccum
ko=2.0*pi/lambda_o;
F=8.791/(freq*sqrt(er));
a=F/sqrt(1+2*h/(pi*er*F)*(log(pi*F/(2*h))+1.7726)); % radius
ae=a*sqrt(1+2*h/(pi*er*a)*(log(pi*a/(2*h))+1.7726));  % effective radius

x=ko*ae*sin(t);
j0=besselj(0,x);
j2=besselj(2,x);
j02p=j0-j2;
j02=j0+j2;
grad=(ko*ae)^2/480*sum((j02p.^2+(cos(t)).^2.*j02.^2).*sin(t).*0.001); % radiation loss
emo=1;
m=1;
mu0=4*pi*10^(-7);
k=ko*sqrt(er);
gc=emo*pi*(pi*mu0*freq*10^9)^(-3/2)*((k*ae)^2-m^2)/(4*(h/100)^2*sqrt(conductivity)); % conductance loss
gd=emo*tan_delta*((k*ae)^2-m^2)/(4*mu0*h/100*freq*10^9);
gt=grad+gc+gd;
Rin0_=1/gt;
Rin_= Rin0_*besselj(1,k*rho)^2/besselj(1,k*ae)^2;

disp("Given Feed Point: "+rho+"----> Rinput:"+Rin_)


%  =====  finding the best feed point  ========
R_Ref=50;
Delta_R=0.5;
Subdivide=20000;
format long
Rmin=ae;
R_Diff=abs(Rin0_-R_Ref);
for rho=0:ae/Subdivide:ae
    Rin_= Rin0_*besselj(1,k*rho)^2/besselj(1,k*ae)^2;
    if(Rin_ >=(R_Ref-Delta_R) &&  Rin_ <=(R_Ref+Delta_R))
        if( abs(Rin_-R_Ref)<R_Diff )
            R_Diff=abs(Rin_-R_Ref);
            rho_f=rho;
            Rin_f=Rin_;
        end
    disp("Feed Point: "+rho+"----> Rinput:"+Rin_)
    end
end
%  =====                     results                ========
disp("Frequence: "+freq+" Ghz");
disp("Radius: "+ae+" cm");
disp("Best Feed Point: rho="+rho_f+" cm  ----> Rinput:"+Rin_f+" Ohm")