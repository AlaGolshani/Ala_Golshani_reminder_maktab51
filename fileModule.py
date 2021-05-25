import pickle


def read_from_file(filename='users.pkl'):
    data = None
    try:
        with open(filename, 'rb') as f:
            data = pickle.load(f)
    except EOFError:
        return []
    except FileNotFoundError as e:
        print('Error: ', e)
    return data


def write_to_file(data, filename='users.pkl'):
    try:
        with open(filename, 'wb') as f:
            pickle.dump(data, f)
    except FileNotFoundError as e:
        print('Error: ', e)
