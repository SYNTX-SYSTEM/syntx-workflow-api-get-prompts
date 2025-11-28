def get_resonance():
    return {"drift": "STABIL", "status": "OK"}
    
if __name__ == "__main__":
    import json
    print(json.dumps(get_resonance(), indent=2))
