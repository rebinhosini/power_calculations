import pandas as pd 
import numpy as np 


class sample_size_calculator():
    
    
    def __init__(
        self, 
        p1, 
        ratio = 1,
        volume = None,
        uplift = None,
        min_size = None,
        max_size = None
    ): 
        
        """
           :param float p1: The control rate.
           :param float uplift: The relative expected change against the control.
           :param float ratio: The ratio between variant and control sample size. 
           :type priority: integer or None
           :return: The expected number of observations the variant needs for statistical significance. 
        """
        
        self.volume = volume
        self.p1 = p1 
        self.p2 = None 
        self.ratio = ratio 
        self.uplift = uplift 
        self.min = min_size
        self.max = max_size 
        
    def get_sample_size(self):
        
        assert self.uplift is not None, 'Need to specify uplift'
    
        self.p2 = self.p1*(self.uplift+1)

        if self.uplift < 0:
            self.p2 = self.p1*(self.uplift-1)

        nom = ((1.96+0.84)**2)*(self.p1*(1-self.p1)+self.p2*(1-self.p2)*self.ratio)**0.5
        denom = (self.p1-self.p2)**2

        return int(nom/denom) 
    
    
    def simulate(self): 
        
        assert self.min is not None, 'Need to specify grid sizes'
        assert self.max is not None, 'Need to specify grid sizes'
    
        grid = np.arange(self.min, self.max, 0.005)

        df = pd.DataFrame(columns=['Uplift - %', 'Samples', 'Current Volume'])

        for i, u in enumerate(grid): 
            self.uplift = u
            df.at[i, 'Uplift - %'] = u*100
            df.at[i, 'Samples'] = self.get_sample_size()
            df.at[i, 'Current Volume'] = self.volume

        if self.volume is None: 
            return df.drop('Current Volume', axis=1)
        else: 
            df['Additional Units of Time To Significance'] = np.where(df['Samples']<df['Current Volume'], 'No Units', df['Samples']/df['Current Volume'])
            df['Expected Significance'] = np.where(df['Current Volume'] > df['Samples'], 'Yes', 'No')
            return df 
    
    
    
def run():

    import sys
    
    init = sample_size_calculator(
        p1 = sys.argv[0],
        min_size = sys.argv[1],
        max_size = sys.argv[2],
        volume = sys.argv[3]
    )
    
    init.simulate()    

if __name__ == "__main__":
    run()