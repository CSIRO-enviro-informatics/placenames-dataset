from .views import GNAFView
from myldapi import SourceRegister, AttributeMapping, AttributeMappingPredicate as Pred
from myldapi.sources import DBSource
from .config import GNAF, DATASET_URI
from myldapi.utils import RDF_a, RDFS

class Locality(SourceRegister):
    def __init__(self):  
        attribute_mappings = [
                # I think I would have the RDFS label 
                # AttributeMapping(varname="label", 
                #         label="Label", 
                #         predicate=Pred(RDFS.label)),
                AttributeMapping(varname="name", 
                                 label="Name", 
                                 predicate=Pred(RDFS.hasName)),
                AttributeMapping(varname="state", 
                                 label="State",
                                 predicate=Pred(GNAF.hasState)),
                AttributeMapping(varname="geometry", 
                                 label="Geometry",
                                 predicate=Pred(GNAF.hasGeometry)),
                AttributeMapping(varname="dateCreated", 
                                 label="Creation Date",
                                 predicate=Pred(GNAF.hasDateCreated)),
            ]

        source = DBSource(
            attr_map=attribute_mappings)

        super().__init__(name = "Register of GNAF Addresses",
                         path = "locality",
                         type_uri = str(GNAF.Locality),
                         type_name = "Locality",
                         base_uri = f"{DATASET_URI}/locality",
                         views=[
                             GNAFView(source)
                         ], 
                         source=source)    
