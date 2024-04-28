class MAResult():
    def __init__(self, df_crosses, symbol, params):
        self.df_crosses = df_crosses
        self.symbol = symbol
        self.params = params

    def result_ob(self):
        d = {
            'symbol' : self.symbol,
            'num_trades' : self.df_crosses.shape[0],
            'total_gain' : self.df_crosses.GAIN.sum(),
            'mean_gain' : self.df_crosses.GAIN.mean(),
            'min_gain' : self.df_crosses.GAIN.min(),
            'max_gain' : self.df_crosses.GAIN.max()
        }

        for k,v in self.params.items():
            d[k] = v

        return d