import os
import sys
from asgs.meshblocks import Meshblock
from asgs.sa1 import StatisticalAreaLevel1
from asgs.sa2 import StatisticalAreaLevel2
from asgs.sa3 import StatisticalAreaLevel3
from asgs.sa4 import StatisticalAreaLevel4
from asgs.states import StateOrTerritory
import asgs.config
from myldapi import MyLDApi

myapi = MyLDApi(None, asgs.config.DATASET_NAME, asgs.config.DATASET_URI, [
        Meshblock(),
        StatisticalAreaLevel1(),
        StatisticalAreaLevel2(),
        StatisticalAreaLevel3(),
        StatisticalAreaLevel4(),
        StateOrTerritory()
    ])

if __name__ == "__main__":        
    path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(path, "export")
    myapi.export_all(path, limit=10, batch_size=10)