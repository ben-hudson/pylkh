import tsplib95 as tsplib

from tsplib95 import transformers, distances


def exact(start, end, scale=1000):
    start_scaled = [e * scale for e in start]
    end_scaled = [e * scale for e in end]
    return distances.euclidean(start_scaled, end_scaled)


distances.TYPES.update({
    'EXACT_2D': exact,
    'EXACT_3D': exact
})


class NodeListField(tsplib.fields.TransformerField):
    default = list

    @classmethod
    def build_transformer(cls):
        depot = transformers.FuncT(func=int)
        return transformers.ListT(value=depot, terminal='-1', sep='\n')


# format according to http://webhotel4.ruc.dk/~keld/research/LKH-3/LKH-3_REPORT.pdf
class LKHProblem(tsplib.models.StandardProblem):
    # extra spec fields
    salesmen = tsplib.fields.IntegerField('SALESMEN')
    vehicles = tsplib.fields.IntegerField('VEHICLES')
    distance = tsplib.fields.NumberField('DISTANCE')
    risk_threshold = tsplib.fields.IntegerField('RISK_THRESHOLD')
    scale = tsplib.fields.IntegerField('SCALE')

    # extra data fields
    backhaul = NodeListField('BACKHAUL_SECTION')
    pickup_and_delivery = tsplib.fields.MatrixField('PICKUP_AND_DELIVERY_SECTION')
    service_time = tsplib.fields.MatrixField('SERVICE_TIME_SECTION')
    time_window = tsplib.fields.MatrixField('TIME_WINDOW_SECTION')

    depots = NodeListField('DEPOT_SECTION')  # fix for https://github.com/rhgrant10/tsplib95/pull/16

    # need to override `render` because spec fields must precede data fields according to TSPLIB format
    # adapted from https://github.com/rhgrant10/tsplib95/blob/master/tsplib95/models.py#L217
    def render(self):
        spec_part = [
            'NAME',
            'TYPE',
            'COMMENT',
            'DIMENSION',
            'CAPACITY',
            'EDGE_WEIGHT_TYPE',
            'EDGE_WEIGHT_FORMAT',
            'EDGE_DATA_FORMAT',
            'NODE_COORD_TYPE',
            'DISPLAY_DATA_TYPE',
            'SALESMEN',
            'VEHICLES',
            'DISTANCE',
            'RISK_THRESHOLD',
            'SCALE'
        ]

        data_part = [
            'NODE_COORD_SECTION',
            'DEPOT_SECTION',
            'DEMAND_SECTION',
            'EDGE_DATA_SECTION',
            'FIXED_EDGES_SECTION',
            'DISPLAY_DATA_SECTION',
            'TOUR_SECTION',
            'EDGE_WEIGHT_SECTION',
            'BACKHAUL_SECTION',
            'PICKUP_AND_DELIVERY_SECTION',
            'SERVICE_TIME_SECTION',
            'TIME_WINDOW_SECTION'
        ]

        # render each value by keyword
        rendered = self.as_name_dict()
        for name in list(rendered):
            value = rendered.pop(name)
            field = self.__class__.fields_by_name[name]
            if name in self.__dict__ or value != field.get_default_value():
                rendered[field.keyword] = field.render(value)

        # build keyword-value pairs with the separator
        # add fields from spec part, then data part
        kvpairs = []
        for keyword in spec_part + data_part:
            if keyword in rendered:
                value = rendered[keyword]
                sep = ':\n' if '\n' in value else ': '
                kvpairs.append(f'{keyword}{sep}{value}')
        kvpairs.append('EOF')

        # join and return the result
        return '\n'.join(kvpairs)
