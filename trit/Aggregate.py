from pprint import pprint


class Aggregate:
    
    def __init__(self):
        pass

    def get_entities(self, result):
        companies, persons = [], []
        starts = dict()

        for key, value in result.copy().items():

            if '_type' in result[key]:

                if result[key]['_type'] == 'Company':
                    mentions = [{'mention': mention['exact'],
                                 'relevance': result[key]['relevance'],
                                 'start': mention['offset'],
                                 'end': mention['offset'] + mention['length']} for mention in
                                result[key]['instances']]
                    companies += mentions
                    for mention in result[key]['instances']:
                        starts[mention['offset']] = mention['exact']

                elif result[key]['_type'] == 'Person':

                    mentions = [{'mention': mention['exact'],
                                 'name': result[key]['name'],
                                 'start': mention['offset'],
                                 'end': mention['offset'] + mention['length']} for mention in
                                result[key]['instances']]
                    persons += mentions
                    for mention in result[key]['instances']:
                        starts[mention['offset']] = result[key]['name']
        return companies, persons, starts

    def get_relations(self, starts, result):
        clean_relations, relations = [], []

        for key, value in result.copy().items():

            if '_type' in result[key]:
                if (result[key]['_typeGroup'] == 'relations'):

                    relation_type = result[key]['_type']

                    for start_offset, ent in starts.copy().items():

                        start = result[key]['instances'][0]['offset']
                        end = start + result[key]['instances'][0]['length']
                        if (start_offset >= start) and (start_offset < end):
                            involved_entity = ent
                            clean_relations.append({"relation": relation_type,
                                                    "entity": involved_entity})
                    relations += [result[key]]
        return clean_relations, relations

    def get_topics(self, result):
        topics = []

        for key, value in result.copy().items():

            if '_typeGroup' in result[key]:
                if (result[key]['_typeGroup'] == 'topics') and (result[key]['forenduserdisplay'] == 'true'):
                    topics.append((result[key]['name'], result[key]['score']))
        sort_by_confidence = sorted(topics, key=lambda x: x[1], reverse=True)
        return sort_by_confidence
