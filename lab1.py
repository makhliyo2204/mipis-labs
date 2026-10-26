import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# 1. Параметры эксперимента
N = 10000
lam = 2
seed = 42

# 2. Генератор псевдослучайных чисел
rng = np.random.default_rng(seed)

# 3. Равномерные случайные числа U ∈ [0, 1)
u = rng.random(N)

# 4. Экспоненциальное распределение методом обратной функции
x = - np.log(1 - u) / lam

# 5. Первые элементы
print("Первые 10 случайных чисел:")
print(x[:10])

# 6. Характеристики выборки
sample_mean = np.mean(x)
sample_var = np.var(x)
theoretical_mean = 1 / lam
theoretical_var = 1 / lam**2
print("\nХарактеристики распределения")
print("Выборочное среднее:", sample_mean)
print("Теоретическое среднее:", theoretical_mean)
print("Эмпирическая дисперсия:", sample_var)
print("Теоретическая дисперсия:", theoretical_var)

# 7. Теоретическая плотность
x_line = np.linspace(0, np.max(x), 500)
pdf = lam * np.exp(- lam * x_line)

# 8. Гистограмма
plt.hist(x, bins=40, density=True, alpha=0.6,
         label="Смоделированные значения")
plt.plot(x_line, pdf, linewidth=2,
         label="Теоретическая плотность")
plt.title("Моделирование экспоненциального распределения")
plt.xlabel("x")
plt.ylabel("Плотность вероятности")
plt.grid()
plt.legend()
plt.show()

# 9. Критерий Колмогорова–Смирнова
D, p_value = stats.kstest(x, "expon", args=(0, 1 / lam))
print("\nКритерий Колмогорова–Смирнова")
print("D =", D)
print("p- value =", p_value)
alpha = 0.05
if p_value > alpha:
    print("Гипотеза о соответствии экспоненциальному распределению не отвергается.")
else:
    print("Гипотеза о соответствии экспоненциальному распределению отвергается.")
