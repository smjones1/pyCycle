from openmdao.main.api import Component
from openmdao.lib.datatypes.api import Float, VarTree

from pycycle.flowstation import FlowStation
from pycycle.cycle_component import CycleComponent


class Splitter(CycleComponent): 
    """Takes a single incoming air stream and splits it into two separate ones"""

    BPR_des = Float(12.47, iotype="in", desc="ratio of mass flow in Fl_O2 to Fl_O1")
    MNexit1_des = Float(.4, iotype="in", 
        desc="mach number at the design condition for Fl_O1")
    MNexit2_des = Float(.4, iotype="in", 
        desc="mach number at the design condition for Fl_O2")

    Fl_I = FlowStation(iotype="in", desc="incoming air stream to splitter")
    Fl_O1 = FlowStation(iotype="out", desc="outgoing air stream 1")
    Fl_O2 = FlowStation(iotype="out", desc="outgoing air stream 2")


    def execute(self): 
        Fl_I = self.Fl_I
        Fl_O1 = self.Fl_O1
        Fl_O2 = self.Fl_O2

        Fl_O1.setTotalTP(Fl_I.Tt, Fl_I.Pt)
        Fl_O2.setTotalTP(Fl_I.Tt, Fl_I.Pt)
        Fl_O1.W = Fl_I.W/(self.BPR_des+1)
        Fl_O2.W = Fl_O1.W*self.BPR_des
        if self.run_design: 
            Fl_O1.Mach = self.MNexit1_des
            Fl_O2.Mach = self.MNexit2_des

            self._exit_area_1_des = Fl_O1.area
            self._exit_area_2_des = Fl_O2.area
        else: 
            Fl_O1.area = self._exit_area_1_des
            Fl_O2.area = self._exit_area_2_des

        super(Splitter, self).execute()


if __name__ == "__main__": 
    from openmdao.main.api import set_as_top

    c = set_as_top(Splitter())
    c.run()

