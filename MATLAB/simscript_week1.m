clc;
clear all;
% Define Laplace s variable
s = zpk('s');
%s=tf('s');

% Define Transfer Function
%G(s) = X(s)/F(s) = Position/Force
G = 2.3/(s^2+4.2*s+5.3);

% Define time domain space
Ts= 1.0; %(sec)
po= 4.33; % (%)

%convert to frequency specs
zeta= (-log(po/100.0)/pi)/((1+(log(po/100.0)/pi)^2)^0.5);
wn= 4/(Ts*zeta);

% Set up desired CLTF
Td= wn^2/(s^2+(2*zeta*wn)*s+wn^2);

% Calculate the Controller
KGc = minreal(Td/(G*(1-Td)));

% CLTF
y = minreal(KGc*G/(1+KGc*G));

% Simulate the system for 20(sec)
sim('shell',20);

%Plot results
clf;
x1 = figure(1);
plot(x);
set(x1, 'position', [3 300 560 420]);
grid minor;
xlabel('Time (sec)');
ylabel('(m)');
commandwindow;
shg;

f1 = figure;
plot(F);
set(f1, 'position', [3 43 560 420]);
grid minor;
xlabel('Time (sec)');
ylabel('Force (N)');
commandwindow;
shg;

x2 = figure(1);
plot(x_dis);
set(x2, 'position', [3 300 560 420]);
grid minor;
xlabel('Time (sec)');
ylabel('(m)');
commandwindow;
shg;

% deliverables
result = getsampleusingtime(x,20);
SSE = result.Data;
pOS = ((max(x)-2)/2.0)*100.00;
Umax = max(F);
%%
% Tustin transformation
format long;
Tsamp = 0.01; %(sec)
z = zpk('z',Tsamp);
KGcz= tf(c2d(KGc,Tsamp, 'tustin')) % conversion to discrete time
forceterms = KGcz.Den{1};
errorterms = KGcz.Num{1};
%f = -1*(forceterms(2)*old2_f + forceterms(3)*old_f) + errorterms(1)*e + errorterms(2)*old_e + errorterms(3)*old2_e;
%f= .9802*old_f + (1.629*e)-(1.628*old_e); % f= force and e= error. We are compounding error to increase our force
%If error Coe's are close extend the sig figs to ensure the error isnt
%canceled out

% get above equation by Kgc(z)=F(z)/E(z)=(1.629*z-1.628)/(z-.9802)
%mult by z^-(highest power) on both sides so we need the current error(z)
%and previous errors(z^-1) or (z^-2)
