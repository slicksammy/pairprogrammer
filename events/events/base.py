class Base:
    @classmethod
    def parse_json(cls, initial_json, parse_to_json):
        parsed_json = {}
        
        for key, value in parse_to_json.items():
            if isinstance(value, dict):
                parsed_json[key] = cls.parse_json(initial_json.get(key, {}), value)
            else:
                parsed_json[key] = initial_json.get(key)
        
        return parsed_json