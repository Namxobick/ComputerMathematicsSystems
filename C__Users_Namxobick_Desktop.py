#!/usr/bin/env python
# coding: utf-8

# # Численное вычисление интеграла
# 
# ## Юрин Андрей 3821Б1ПР1
# 
# ### Задача 3
# 
# Используя интеграл
# 
# $$ -\cfrac{4}{9} = \int_{0}^{1}\sqrt[2]{x}\ln{x}dx $$
#  
# можно найти приближение к $-\cfrac{4}{9}$. Используйте правило прямоугольников, трапеций и Симпсона с **2**, **4**,**8**,**16**,**32**,**64** и **128** узлами. Затабулируйте погрешность. Как уменьшается погрешность при удвоении числа элементарных отрезков? Почему с некоторого момента погрешность не уменьшается? Составленная программа должна выводить графики подинтегральных функций, табулированные погрешности и значения интегральных сумм с графиками.

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from scipy import integrate


# In[2]:


xx = np.linspace(1e-12, 1, 1000)
yy = np.sqrt(xx)*np.log(xx)

plt.rcParams["figure.figsize"] = 7,7
plt.title('График подынтегральной функции')
plt.plot(xx, yy, linewidth = 3)
plt.grid()
pass


# In[3]:


a = 1e-12
b = 1
numberNodes = [2, 4, 8, 16, 32, 64, 128]
ans = -4/9
x = np.linspace(0, ans , len(numberNodes))

def PrintValues(method):
    print("%-30s%-25s%-15s" % ("Количество узлов:","Значение интеграла:", "Погрешность:"))
    for i in range(len(numberNodes)):
        print("%-30d%-25f%-15f" % (numberNodes[i], method[i], abs(ans - method[i])))

def PrintGraph(function, nameFunction, titleGraph, sizeX, sizeY, drawAns = True):
    if (drawAns):
        plt.hlines(ans, numberNodes[0], numberNodes[-1], color = 'r')
    
    plt.rcParams["figure.figsize"] = (sizeX, sizeY)
    plt.xticks(numberNodes)
    for f in function:
        plt.plot(numberNodes, f)
    
    for texts in nameFunction:
            plt.text(texts[0],texts[1],texts[2])

    plt.title(titleGraph)
    plt.grid()

pass


# In[4]:


def FormulaX(nameMethod, length):
    if (nameMethod == "Right"):
        return np.arange(a + length, b + np.finfo(float).eps, length)
    if (nameMethod == "Left"):
        return np.arange(a, b, length)
    if (nameMethod == "Middle"):
        return np.arange(a + length/2, b, length)

def Integral(x, y, nameMethod):
    if (nameMethod == "Simpson"):
        return integrate.simps(y,x)
    if (nameMethod == "Trapezoidal"):
        return integrate.trapz(y, x)

def RiemannSum(nodesNumber, nameMethod):
    answers = np.array([])
    for n in nodesNumber:
        length = (b - a) / n
        x = FormulaX(nameMethod, length)
        y = np.sqrt(x) * np.log(x)                                   
        sumAreas = length * sum(y)
        answers = np.append(answers, sumAreas)
    return answers

def SimpsonAndTrapezoidal (nodesNumber, nameMethod):
    answers = np.array([])
    for n in nodesNumber:
        x = np.linspace(a, b, n + 1)
        y = np.sqrt(x)*(np.log(x))
        integral = Integral(x, y, nameMethod)
        answers = np.append(answers, integral)
    return answers


# In[16]:


RightRiemannSum = RiemannSum(numberNodes, "Right")
PrintValues(RightRiemannSum)
PrintGraph([RightRiemannSum],[], "Метод правых прямоугольников", 10, 5)


# In[6]:


LeftRiemannSum = RiemannSum(numberNodes, "Left")
PrintValues(LeftRiemannSum)
PrintGraph([LeftRiemannSum],[], "Метод левых прямоугольников", 10, 5)


# In[7]:


MiddleRiemannSum = RiemannSum(numberNodes, "Middle")
PrintValues(MiddleRiemannSum)
PrintGraph([MiddleRiemannSum],[], "Метод средних прямоугольников", 10, 5)


# In[8]:


Trapezoidal = SimpsonAndTrapezoidal(numberNodes, "Trapezoidal")
PrintValues(Trapezoidal)
PrintGraph([Trapezoidal],[], "Метод трапеций", 10, 5)


# In[9]:


Simpson = SimpsonAndTrapezoidal(numberNodes, "Simpson")
PrintValues(Simpson)
PrintGraph([Simpson],[], "Метод Симсона", 10, 5)


# In[14]:


PrintGraph([RightRiemannSum, LeftRiemannSum, MiddleRiemannSum, Trapezoidal, Simpson],
           [
            [0, 0, ""],
            [5, -0.28, "Метод правых прямоугольников"],
            [5,-0.29, "Метод левых прямоугольников"], 
            [5,-0.46,"Метод средних прямоугольников"],
            [5,-0.3, "Метод трапеций"],
            [-4,-0.42, "Метод Симпсона"]
           ], 
           "Численное интегрирование разными методами", 20, 20)


# In[11]:


PrintGraph([abs(RightRiemannSum - ans), abs(LeftRiemannSum - ans), abs(MiddleRiemannSum - ans),
            abs(Trapezoidal - ans), abs(Simpson - ans)],
           [
            [4, 0.175, "Метод правых прямоугольников"],
            [4, 0.170, "Метод левых прямоугольников"], 
            [0, 0, "Метод средних прямоугольников"],
            [4, 0.165, "Метод трапеций"],
            [-4.5, 0.03, "Метод Симпсона"]
           ], 
           "Погрешности", 20, 20, False)


# # Вывод:
#  - Погрешности изменяются по формуле: $f(x) = \cfrac{1}{x^n}$
#  
#  - Для численного вычисления $\int_{0}^{1}\sqrt[2]{x}\ln{x}dx $  **самым точным** оказался метод **средних прямоугольников**, не смотря на то, что **порядок сходимости метода Симсона - 4, а средних прямоугольников - 2**:
#  
#  $$ R_{ср} = \cfrac{b - a}{24} f^{''}(\xi)h^2 $$
#  
#  $$ R_{ср} <= \cfrac{b - a}{24} max|f^{''}(x_0)|h^2 $$
#  
#  $$ max|f^{''}(x_0)| = max|\cfrac{ln(x_0)}{4x_0 ^ {3/2}}| $$
#  
#  $$ lim_{x -> 0}{\cfrac{ln(x)}{4x ^ {3/2}}} = -\infty $$
#  
#  $$ max|f^{''}(a)| \approx 6,9 * 10^{18} $$
#  
# ------------------------------------------------------------------------------------------------------------------------------- 
#  
#  $$ R_{сим} = \cfrac{b - a}{180} f^{IV}(\xi)h^4 $$
#  
#  $$ R_{сим} <= \cfrac{b - a}{180} max|f^{IV}(x_0)|h^4 $$
#  
#  $$ max|f^{IV}(x_0)| = max|\cfrac{1 - \cfrac{15ln(x_0)}{16}}{x_0 ^ {7/2}}| $$
#  
#  $$ lim_{x -> 0}{\cfrac{1 - \cfrac{15ln(x_0)}{16}}{x_0 ^ {7/2}}} = +\infty $$
#  
#  $$ max|f^{IV}(a)| \approx 2.7 * 10^{43} $$
#  
# ------------------------------------------------------------------------------------------------------------------------------
#  $$ R_{ср} < R_{сим}  $$

# In[12]:


x = np.linspace(1e-12, 1, 1000)
y = ((1 - (15/16 * np.log(x))) / x ** (7/2)) - abs((np.log(x)) / (4 * x ** (3/2)))
plt.rcParams["figure.figsize"] = 7,5
plt.title(r'$ | f^{IV} | - | f ^ {II} | $')
plt.plot(x, y, linewidth = 3)
plt.grid()
pass


# Таким образом, $$ f^{IV} > f^{''}  $$
# 
# $$ R_{сим} > R_{ср}  $$
# 
# Из-за этого метод средних прямоугольников в данном случае показал результат лучше, чем метод Симпсон
