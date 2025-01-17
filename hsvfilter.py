class HSVFILTER():
    def __init__(self,
                Hmin: int | None = None,
                Hmax: int | None = None,
                Smin: int | None = None,
                Smax: int | None = None,                 
                Vmin: int | None = None,
                Vmax: int | None = None
                 ):
        self.Hmin = Hmin if Hmin else 130
        self.Hmax = Hmax if Hmax else 260
        self.Smin = Smin if Smin else 50
        self.Smax = Smax if Smax else 255
        self.Vmin = Vmin if Vmin else 50
        self.Vmax = Vmax if Vmax else 255


