import math
import tsplib95 as tsplib

from tsplib95 import transformers, distances

distances.TYPES.update({
    'EXACT_2D': math.dist,
    'EXACT_3D': math.dist,
    'FLOOR_2D': distances.euclidean,
    'FLOOR_3D': distances.euclidean,
})


# nodes separated by \n and terminated with -1
class NodeListField(tsplib.fields.TransformerField):
    default = list

    @classmethod
    def build_transformer(cls):
        node = transformers.FuncT(func=int)
        return transformers.ListT(value=node, sep='\n', terminal='-1')

# salesman followed by a list of nodes separated by -1\n and terminated with nothing
class CTSPSetField(tsplib.fields.TransformerField):
    default = dict

    @classmethod
    def build_transformer(cls):
        key = transformers.FuncT(func=int)
        value = transformers.ListT(value=transformers.FuncT(func=int), terminal='-1')
        return transformers.MapT(key=key, value=value, sep='\n')


# format according to http://webhotel4.ruc.dk/~keld/research/LKH-3/LKH-3_REPORT.pdf
class LKHProblem(tsplib.models.StandardProblem):
    # extra spec fields
    demand_dimension = tsplib.fields.IntegerField('DEMAND_DIMENSION')
    distance = tsplib.fields.NumberField('DISTANCE')
    risk_threshold = tsplib.fields.IntegerField('RISK_THRESHOLD')
    salesmen = tsplib.fields.IntegerField('SALESMEN')
    scale = tsplib.fields.IntegerField('SCALE')
    service_time = tsplib.fields.IntegerField('SERVICE_TIME')
    vehicles = tsplib.fields.IntegerField('VEHICLES')

    # extra data fields
    backhaul_section = NodeListField('BACKHAUL_SECTION')
    ctsp_set_section = CTSPSetField('CTSP_SET_SECTION')
    draft_limit_section = tsplib.fields.DemandsField('DRAFT_LIMIT_SECTION') # draft limit has same unit as demand
    pickup_and_delivery_section = tsplib.fields.MatrixField('PICKUP_AND_DELIVERY_SECTION')
    required_nodes_section = NodeListField('REQUIRED_NODES_SECTION')
    service_time_section = tsplib.fields.MatrixField('SERVICE_TIME_SECTION')
    time_window_section = tsplib.fields.MatrixField('TIME_WINDOW_SECTION')

    depots = NodeListField('DEPOT_SECTION')  # fix for https://github.com/rhgrant10/tsplib95/pull/16

    # need to override `render` because spec fields must precede data fields according to TSPLIB format
    # we assume that data fields end with _SECTION, and we sort those to the end of the field list
    # adapted from https://github.com/rhgrant10/tsplib95/blob/master/tsplib95/models.py#L217
    def render(self):
        # render each value by keyword
        rendered = self.as_name_dict()
        for name in list(rendered):
            value = rendered.pop(name)
            field = self.__class__.fields_by_name[name]
            if name in self.__dict__ or value != field.get_default_value():
                rendered[field.keyword] = field.render(value)

        # build keyword-value pairs with the separator
        kvpairs = []
        for keyword, value in sorted(rendered.items(), key=lambda item: item[0].endswith('_SECTION')):
            sep = ':\n' if '\n' in value else ': '
            kvpairs.append(f'{keyword}{sep}{value}')
        kvpairs.append('EOF')

        # join and return the result
        return '\n'.join(kvpairs)
