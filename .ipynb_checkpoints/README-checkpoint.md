# Power analaysis for a/b testing ratios/proportions using MDE (Minimal Detectable Effect) 
Using minimal detectable effect for frequentist power calculations in a/b testing. The script can run directly in the terminal where the required arguments are: 

1. p1: The benchmark ratio 
2. min_size: lower limit of evaluation the uplift evaluation grid
3. max_size: upper limit of evaluation the uplift evaluation grid
4. volume: Number of observations (data) per unit of time (for variant)


Terminal output can look something like this: 

![output](output.png)

This output shows that your volume could result in statistical significance if you have a 0.7% uplift. For a 0.5% uplift, you would probably have to run your test for 2 days (1.92689) if your volume represents daily volume. 