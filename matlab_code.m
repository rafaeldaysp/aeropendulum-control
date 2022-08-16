close;
clc;
clear;

%% Leitura de dados

dados = csvread('dados_convertidos.csv', 1);
t = dados(:, 2) ./1000;
y = dados(:, 4);
u = dados(:, 3);

%% Gera função de transferência

dt = t(2) - t(1);
data = iddata(y, u, dt);
sys = tfest(data, 2);
simulated_sys = lsim(sys, u, t);

%% Plota resultados

figure

subplot(2, 1, 1)
plot(t, u)
hold on
plot(t, y)
legend('Entrada Degrau', 'Saída')
xlabel('Tempo (s)')
ylabel('Ângulo (◦)')
title('Resultados');

subplot(2, 1, 2)
plot(t, u);
hold on
plot(t, y);
hold on
plot(t, simulated_sys);
legend('Entrada Degrau', 'Saída', 'Função Estimada')
title('Estimação')
xlabel('Tempo (s)')
ylabel('Ângulo (◦)')


%% Sistema estimado

Gs = sys;
Gz = c2d(sys, 0.5);