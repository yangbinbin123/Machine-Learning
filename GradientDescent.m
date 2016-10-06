clear;clc;
data = load('ex1data1.txt');
x = data(:,1);
y = data(:,2);
m = size(data,1);
plot(x,y,'rx','MarkerSize',10);
ylabel('Profit in $10,000s');
xlabel('Population of City in 10,000s');
x = [ones(m,1),data(:,1)];
y = data(:,2);
theta = zeros(2,1);
alpha = 0.01;
iterations = 1500;
J = computeCost(x,y,theta);
theta = gradientDescent(x, y, theta, alpha, iterations);
hold on;
plot(x(:,2), x*theta, '-');
legend('Training data', 'Linear regression',2)
hold off


