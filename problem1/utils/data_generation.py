from faker import Faker

def generate_sample_data(spec, num_records=10):
    faker = Faker()
    data = []
    for _ in range(num_records):
        record = [
            faker.random_int(min=10000, max=99999),  # f1
            faker.word().ljust(12),  # f2
            faker.random_int(min=100, max=999),  # f3
            faker.random_letter().upper() + faker.random_letter().upper(),  # f4
            faker.address().replace('\n', ' ')[:13].ljust(13),  # f5
            str(faker.random_int(min=1000000, max=9999999)),  # f6
            faker.phone_number()[:10],  # f7
            faker.word()[:10].ljust(10),  # f8
            faker.address().replace('\n', ' ')[:20].ljust(20),  # f9
            faker.word()[:13].ljust(13),  # f10
        ]
        data.append(record)
    return data
