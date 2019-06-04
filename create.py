import json
import os


class DB():

    def create(self):
        self.data = []
        for tag in os.listdir('FILES'):
            path_to_json = 'FILES/' + tag
            json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
            for j in json_files:
                with open(path_to_json + '/' + j, 'r') as f:
                    try:
                        self.data.extend(json.load(f))
                    except:
                        pass
        return self.data


def main():
    db_1 = DB()
    data = db_1.create()
    with open('data_base.json', 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    main()
