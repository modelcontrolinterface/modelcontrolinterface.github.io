import yaml
import sys

def transform(data):
    if isinstance(data, dict):
        is_schema = 'type' in data

        # Recurse first
        for key in list(data.keys()):
            transform(data.get(key))

        example_val = None
        has_example = False

        if 'example' in data:
            example_val = data.pop('example')
            has_example = True
        elif 'examples' in data:
            # We will be rebuilding this, so pop it.
            example_val = data.pop('examples')
            has_example = True

        if has_example:
            # --- Start of normalization ---
            # 1. If it's a map like {'default': {'value': 'foo'}}, extract the value
            if isinstance(example_val, dict) and 'default' in example_val and 'value' in example_val.get('default', {}):
                example_val = example_val['default']['value']
            
            # 2. If it's a list of {'value':...}, extract values
            if isinstance(example_val, list) and example_val and isinstance(example_val[0], dict) and 'value' in example_val[0]:
                example_val = [d.get('value') for d in example_val]

            # 3. Unwrap single-item lists
            while isinstance(example_val, list) and len(example_val) == 1:
                example_val = example_val[0]

            # 4. Merge list of dicts for object examples
            if isinstance(example_val, list) and all(isinstance(i, dict) for i in example_val):
                merged = {}
                for item in example_val: merged.update(item)
                example_val = merged
            # --- End of normalization ---

            # Now, format it correctly based on context.
            if is_schema:
                if not isinstance(example_val, list):
                    data['examples'] = [example_val]
                else:
                    data['examples'] = example_val
            else: # Parameter, response, etc.
                data['examples'] = {'default': {'value': example_val}}

    elif isinstance(data, list):
        for item in data:
            transform(item)

if __name__ == '__main__':
    filepath = 'docs/openapi.yaml'
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = yaml.safe_load(f)
        
        transform(content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(content, f, sort_keys=False, indent=2, allow_unicode=True)
            
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
