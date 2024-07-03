# Example Notebook for Conversion

This notebook demonstrates simple outputs for testing the conversion process. It includes:

- Markdown cells
- Code cells with outputs
- A matplotlib plot



```python
# Basic print statement
print("Hello, Notebookify!")
```

    Hello, Notebookify!
    

## A Simple Calculation


```python
# Basic math
2 + 2 * 3
```




    8



## Matplotlib Plot


```python
import matplotlib.pyplot as plt

# A simple plot
x = [1, 2, 3, 4, 5]
y = [10, 20, 25, 30, 40]

plt.figure()
plt.plot(x, y, marker="o", linestyle="-", color="b")
plt.title("Simple Line Plot")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.show()
```


    
![png](output_5_0.png)
    

