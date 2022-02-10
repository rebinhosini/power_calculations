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
           :param int volume: The current volume of observerations you are expected to have. 
           :param float p1: The control rate.
           :param float p2: The variant rate. 
           :param float ratio: The ratio between variant and control sample size. 

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
        
        #80% power and two tailed 95% signifigiance level returns z_(1-b) = 0.84 and z_(1-a/2) = 1.96 
        nom = ((1.96+0.84)**2)*(self.p1*(1-self.p1)+self.p2*(1-self.p2)*self.ratio)**0.5
        denom = (self.p1-self.p2)**2

        return int(nom/denom) 
    
    
    def simulate(self): 
        
        assert self.min is not None, 'Need to specify grid sizes'
        assert self.max is not None, 'Need to specify grid sizes'
    
        grid = np.arange(self.min, self.max, 0.001)
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
    pd.set_option('display.max_rows', 1000)
    
    init = sample_size_calculator(
        p1 = np.float(sys.argv[1]),
        min_size = np.float(sys.argv[2]),
        max_size = np.float(sys.argv[3]),
        volume = np.float(sys.argv[4])
    )
    print(init.simulate())

if __name__ == "__main__":
    run()