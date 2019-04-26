from Aggregate import Aggregate


class Aggregator:

    def __init__(self, results):
        self.results = results
        self.aggregate = Aggregate()
        agg = self.combine()
        self.companies = agg[0]
        self.persons = agg[1]
        self.topics = agg[2]
        self.relations = agg[3]

    def combine(self):
        all_companies, all_persons, all_topics, all_relations = [], [], [], []
        for result in self.results:
            
            entities = self.aggregate.get_entities(result)
            companies = entities[0]
            persons = entities[1]
            entity_offsets = entities[2]
            all_relation_types = self.aggregate.get_relations(entity_offsets, result)
            relations = all_relation_types[0]
            unsorted_topics = self.aggregate.get_topics(result)
            topics = sorted(unsorted_topics, key=lambda x: x[1], reverse=True)
            
            all_companies += companies
            all_persons += persons
            all_topics += topics
            all_relations += relations
        
        return all_companies, all_persons, all_topics, all_relations

