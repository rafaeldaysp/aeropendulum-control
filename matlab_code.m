close;
clc;
clear;

%% Leitura de dados

dados = csvread('dados_convertidos.csv', 1);
t = dados(:, 2);
y = dados(:, 3);
u = dados(:, 4);

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
ylabel('Tensão (V)')
title('Coletado')

subplot(2, 1, 2)
plot(t, simulated_sys);
hold on
plot(t, y);
title('Estimação')

%% Sistema estimado

sys